#!/usr/bin/python3

# Copyright (C) 2019-2019, Josef Hahn
#
# This file is part of pish.
#
# pish is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pish is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pish.  If not, see <http://www.gnu.org/licenses/>.

"""
Versatile tools for connecting to ssh, local shell, and/or su(do) in order to execute shell commands there,
to manage ssh identity and host keys, and more.

Start with `pish.localhost` (instance of pish.Connection).

Note: It is possible to stack connections, but not all combinations are guaranteed to work at runtime.

Note: Many operations require bash.
"""

from typing import *
import base64
import datetime
import io
import json
import logging
import os
import shlex
import socket
import subprocess
import sys
import threading
import time


class GeneralError(Exception):
    """
    Base Exception for any error from pish.
    """

    def __call__(self, *args):
        return self.__class__(*(self.args + args))


class TimeoutExpiredError(GeneralError):
    """
    Exception for timeout on action executions.
    """

    def __init__(self):
        super().__init__(f"timeout")


class GeneralConnectionError(GeneralError):
    """
    Exception for errors on connecting.
    """

    def __init__(self, conn, errortext):
        GeneralError.__init__(self, f"unable to connect '{conn}': '{errortext}'")
        self.conn = conn
        self.errortext = errortext


class SshConnectionError(GeneralConnectionError):
    """
    Exception for errors on connecting to an ssh host.
    """

    def __init__(self, conn, errortext):
        super().__init__(conn, errortext)


class Connection:
    """
    Those objects allow to execute various actions, from bare command execution to various key management things.
    Connections can be stacked, so you can connect from one host to another.

    Do not construct them directly. Some `pish.localhost` methods (type pish.Connection) allow new
    connections.
    """

    def __init__(self, *, parentconn, defaulttimeout=60*5.0, basetimeout=2):
        self.parentconn: 'Connection' = parentconn
        self.defaulttimeout = defaulttimeout
        self.basetimeout = basetimeout
        self.cmdlinebuilder: 'CommandLineBuilder' = CommandLineBuilder(conn=self)

    def ssh(self, host: str, *, username: str, port: Optional[int] = None, password: Optional[str] = None,
            idfile: Optional[str] = None) -> 'SshConnection':
        """
        Connects to another host via ssh. It chooses an authentication method depending on the given parameters.

        :param host: The host.
        :param username: The username.
        :param port: The port.
        :param password: The login password. Specify `True` for manual password prompt on stdin.
        :param idfile: The login identity file.
        :return: A new connection.
        """
        if password is not None:
            return SshPasswordConnection(parentconn=self, host=host, port=port, username=username, password=password)
        elif idfile:
            return SshIdfileConnection(parentconn=self, host=host, port=port, username=username, idfile=idfile)
        else:
            return SshConnection(parentconn=self, host=host, port=port, username=username)

    def elevate_su(self, username: Optional[str] = None, password: Optional[str] = None) -> 'ElevateSuConnection':
        """
        Elevates this connection via su.

        :param username: The username (default: 'root').
        :param password: The password. Specify `None` for manual password prompt on stdin.
        :return: A new elevated connection.
        """
        return ElevateSuConnection(parentconn=self, username=username, password=password)

    def elevate_sudo(self, username: Optional[str] = None, password: Optional[str] = None,
                     direct: Optional[bool] = None) -> 'ElevateSudoConnection':
        """
        Elevates this connection via sudo.

        :param username: The username (default: 'root').
        :param password: The password. Specify `None` for manual password prompt on stdin.
        :param direct: If to call the commands directly (instead of via bash). If so, by-command sudo permissions can
                       be used better, but environment can't be passed on the other hand.
        :return: A new elevated connection.
        """
        return ElevateSudoConnection(parentconn=self, username=username, password=password, direct=direct)

    def allow_ssh_identitykey(self, key: str, *, username: Optional[str] = None, timeout: Optional[int] = None) -> None:
        """
        Deploys an identity key to the local authorized_keys keychain for a user.

        :param key: The identity key's public part.
        :param username: The user name to deploy the key to (default: own).
        :param timeout: Timeout in seconds (default: auto).
        """
        qfssh = f"~{username or ''}/.ssh"
        qfsshak = f"{qfssh}/authorized_keys"
        fchown = f"chown -R {shlex.quote(username)} {qfssh};" if username else ''
        pk = get_unique(tiny=True)
        xe = io.BytesIO()
        r = self.bash(
            f'mkdir -p {qfssh};touch {qfsshak};chmod -R g=,o= {qfssh};{fchown}echo "${pk}">>{qfsshak}',
            stderr=xe, env={pk: key}, timeout=timeout)
        if r != 0:
            raise GeneralError("unable to deploy identitykey: " + xe.getvalue().decode())

    def get_ssh_identitykey(self, *, username: Optional[str] = None, timeout: Optional[int] = None) -> str:
        """
        Fetches the identity key's public part for a user.

        :param username: The user name to deploy the key to (default: own).
        :param timeout: Timeout in seconds (default: auto).
        :return: The identity key's public part.
        """
        xo = io.BytesIO()
        r = self.bash(f"cat ~{username or ''}/.ssh/id_rsa.pub", stdout=xo, timeout=timeout)
        if r == 0:
            return xo.getvalue().decode().strip()

    def reset_ssh_hostkey(self, host: str, *, port: Optional[int] = None, username: Optional[str] = None,
                          timeout: Optional[int] = None) -> None:
        """
        Resets the key of a host/port in the local known_hosts keychain for a user.

        :param host: The host (to reset the key for).
        :param port: The port.
        :param username: The user name to reset the key for (default: own).
        :param timeout: Timeout in seconds (default: auto).
        """
        qfssh = f"~{username or ''}/.ssh"
        qfshf = f"{qfssh}/known_hosts"
        oshs = f"[{host}]:{port}" if (port and port != 22) else host
        fchown = f"chown -R {shlex.quote(username)} {qfssh};" if username else ''
        pk = get_unique(tiny=True)
        bcrem = f"ssh-keygen -f {qfshf} -R {oshs}"
        bc = f'mkdir -p {qfssh}&&touch {qfshf}&&echo "${pk}">>{qfshf}&&({bcrem};{fchown}chmod -R g=,o= {qfssh};true)'
        self.bash(bc, timeout=timeout)

    def get_ssh_hostkey(self, host: str, *, port: Optional[int] = None, timeout: Optional[int] = None) -> str:
        """
        Fetches current the host key from a host.

        :param host: The host (to get the key for).
        :param port: The port.
        :param timeout: Timeout in seconds (default: auto).
        :return: The host key.
        """
        jcmd = ["ssh-keyscan"]
        if port:
            jcmd.append(f"-p{port}")
        jcmd.append(host)
        xo, xe = io.BytesIO(), io.BytesIO()
        r = self.execute(*jcmd, stdout=xo, stderr=xe, timeout=timeout)
        so = xo.getvalue().decode().strip()
        if (r != 0) or not so:
            raise GeneralError("unable to get hostkey: " + xe.getvalue().decode())
        res = [y for y in [x.strip() for x in so.split("\n")] if (y and not y.startswith("#"))]
        res.sort()
        return "\n".join(res)

    def authorize_ssh_hostkey(self, key: str, *, username: Optional[str] = None, timeout: Optional[int] = None) -> None:
        """
        Adds a host key to the local known_hosts keychain for a user.

        :param key: The host key.
        :param username: The user name to add the key for (default: own).
        :param timeout: Timeout in seconds (default: auto).
        """
        qfssh = f"~{username or ''}/.ssh"
        qfshf = f"{qfssh}/known_hosts"
        fchown = f"chown -R {shlex.quote(username)} {qfssh};" if username else ''
        pk = get_unique(tiny=True)
        bchash = f"ssh-keygen -H -f {qfshf};rm {qfshf}.old"
        bc = f'mkdir -p {qfssh}&&touch {qfshf}&&echo "${pk}">>{qfshf}&&({bchash};{fchown}chmod -R g=,o= {qfssh};true)'
        xe = io.BytesIO()
        r = self.bash(bc, stderr=xe, env={pk: key}, timeout=timeout)
        if r != 0:
            raise GeneralError("unable to authorize hostkey: " + xe.getvalue().decode())

    def check_ssh_host_authorized(self, host: str, *, port: Optional[int] = None,
                                  timeout: Optional[int] = None) -> bool:
        """
        Checks if a host is allowed from the local known_hosts keychain for a user.

        :param host: The host to check.
        :param port: The port.
        :param timeout: Timeout in seconds (default: auto).
        """
        port = port or 22
        xo = io.BytesIO()
        self.bash(f"ssh -o BatchMode=yes -p{port} {host} true 2>&1",
                  env={"LC_ALL": "C"}, stdout=xo, timeout=timeout)
        lo = [x.strip() for x in xo.getvalue().decode().strip().split("\n")]
        if len(lo) == 0:
            return True
        else:
            return lo[-1] != "Host key verification failed."

    def create_ssh_identityfile(self, *, passphrase: Optional[str] = None, username: Optional[str] = None,
                                comment: Optional[str] = None, timeout: Optional[int] = None) -> None:
        """
        Creates an ssh identity keypair for a local user (only if it doesn't exist before!) for doing remote logins.

        :param passphrase: The passphrase for the keypair.
        :param username: The user name to create the keypair for (default: own).
        :param comment: The keypair comment text.
        :param timeout: Timeout in seconds (default: auto).
        """
        if comment is None:
            snow = datetime.datetime.now().strftime("%Y-%m-%d")
            comment = f"pish {snow}"
        qcomment = shlex.quote(comment)
        if isinstance(passphrase, str):
            sopassphrase = f"-N {shlex.quote(passphrase)}"
        else:
            sopassphrase = ""
        hdn = f"~{username}" if username else "~"
        qfidir = f"{hdn}/.ssh"
        qfifile = f"{qfidir}/id_rsa"
        fchown = f";chown -R {shlex.quote(username)} {qfidir}" if username else ''
        bc = self.cmdlinebuilder.with_pre_and_post(
            f"if [ ! -e {qfifile} ];then mkdir -p {qfidir};ssh-keygen -t rsa -b 4096 -C {qcomment}"
            f" -f {qfifile} {sopassphrase};else true;fi", post=f"chmod -R g=,o= {qfidir}{fchown}")
        xe = io.BytesIO()
        r = self.bash(bc, stderr=xe, timeout=timeout)
        if r != 0:
            raise GeneralError("unable to create ssh identityfile: " + xe.getvalue().decode())

    def load_ssh_identityfile_into_agent(self, *, idfile: Optional[str] = None, username: Optional[str] = None,
                                         passphrase: Optional[str] = None, timeout: Optional[int] = None) -> None:
        """
        Loads a local ssh identity file into the ssh agent.

        :param idfile: The identity file path.
        :param username: The user name to load the key from (default: own).
        :param passphrase: The unlock passphrase.
        :param timeout: Timeout in seconds (default: auto).
        """
        if idfile:
            qidfile = shlex.quote(idfile)
        else:
            qidfile = f"~{username or ''}/.ssh/id_rsa"
        bc = f"ssh-add {qidfile}"
        env = {}
        bc = self.cmdlinebuilder.run__askpass(bc, env=env, askpassfct=self.cmdlinebuilder.ssh_askpass,
                                              password=passphrase, onpasswordcmdpre="echo x|")
        bc = (f'_pysshman_fp="$(ssh-keygen -l -f {qidfile})";if [ "$_pysshman_fp" == "" ];then exit 1;fi;'
              f'if [ $(ssh-add -l|grep "$_pysshman_fp"|wc -l) == 0 ];then {bc};else true;fi')
        xe = io.BytesIO()
        r = self.bash(bc, stderr=xe, timeout=timeout, env=env)
        if r != 0:
            raise GeneralError("unable to load ssh identityfile into agent: " + xe.getvalue().decode())

    def execute(self, *cmd: str, stdin=b"", stdout=None, stderr=None, env: Optional[Dict[AnyStr, AnyStr]] = None,
                timeout: Optional[int] = None) -> int:
        """
        Executes a command line.

        :param cmd: The command line to execute (parameter by parameter).
        :param stdin: The content to pass as stdin as either a string, a file stream, or `None` for passthrough.
        :param stdout: The file stream or io.BytesIO to feed with stdout, or `None` for passthrough.
        :param stderr: The file stream or io.BytesIO to feed with stderr, or `None` for passthrough.
        :param env: Additional environment variables.
        :param timeout: Timeout in seconds (default: auto).
        :return: The return code.
        """
        raise NotImplementedError()

    def bash(self, cmd: str, **b) -> int:
        """
        Executes a shell command, allowing full bash syntax.
        See execute() for more parameters and infos.

        :param cmd: The command to execute (as string).
        :return: The return code.
        """
        return self.execute("bash", "-c", f"true;{cmd}", **b)

    def conninfo_to_json(self) -> str:
        """
        Returns serialized json string for this connection. Restore it later with from_conninfo_json().
        """
        return json.dumps(self.conninfo_to_plainobjs())

    def conninfo_to_plainobjs(self) -> Dict[str, Any]:
        """
        Returns pieces for serialization.
        """
        return {'type': type(self).__name__, 'defaulttimeout': self.defaulttimeout, 'basetimeout': self.basetimeout,
                'parentconn': self.parentconn.conninfo_to_plainobjs() if self.parentconn else None}

    @staticmethod
    def from_conninfo_plainobjs(o):
        """
        Returns a Connection from serialized pieces.
        """
        if o is None:
            return localhost
        stype = o.pop("type")
        joparentconn = o.pop("parentconn", None)
        ttype = globals()[stype]
        return ttype(parentconn=Connection.from_conninfo_plainobjs(joparentconn), **o)

    @staticmethod
    def from_conninfo_json(s):
        """
        Returns a Connection from a serialized json string. See conninfo_to_json().
        """
        return Connection.from_conninfo_plainobjs(json.loads(s))

    def _get_istream(self, *istreams):
        """
        Only used internally. Makes a valid stdin by concatenating some input sources.
        """
        if len([x for x in istreams if x is not None]) == 0:
            return None
        res = None
        for p in istreams:
            if p is None:
                if res is not None:
                    raise NotImplementedError()
                res = sys.stdin.buffer
            elif isinstance(p, str) or isinstance(p, bytes):
                if isinstance(p, str):
                    p = p.encode()
                if res is None:
                    res = b""
                if not isinstance(res, bytes):
                    raise NotImplementedError()
                res += p
            elif hasattr(p, "fileno"):
                if res is not None:
                    raise NotImplementedError()
                res = p
            else:
                raise NotImplementedError()
        return res

    def _get_cmd(self, cmd) -> List[str]:
        """
        Only used internally. Normalized command lines.
        """
        if len(cmd) == 1 and not isinstance(cmd[0], str):
            return list(cmd[0])
        else:
            return list(cmd)

    def _get_effective_timeout(self, ti: Optional[float] = None) -> int:
        """
        Only used internally. Computes the complete effective timeout for an operation.
        """
        ti = ti or self.defaulttimeout
        ti += self.basetimeout
        if self.parentconn:
            ti += self.parentconn._get_effective_timeout(0.5)
        return int(ti)

    def _str_pieces(self) -> List[Tuple[str, Any]]:
        """
        Only used internally. Returns pieces for the __str__ representation.
        """
        return []

    def __str__(self):
        stype = type(self).__name__
        lop = self._str_pieces()
        if self.parentconn and not isinstance(self.parentconn, LocalhostConnection):
            lop.append(("parent", self.parentconn))
        sopts = ", ".join([f"{ko}: {vo}" for ko, vo in lop])
        if sopts:
            sopts = " " + sopts
        return stype + sopts


class LocalhostConnection(Connection):
    """
    A connection to your local machine.

    Do not construct them directly. Some `pish.localhost` methods (type pish.Connection) allow new
    connections.
    """

    def __init__(self, **b):
        super().__init__(parentconn=None, **b)

    def conninfo_to_plainobjs(self):
        return None

    def execute(self, *cmd, stdin=b"", stdout=None, stderr=None, env=None, timeout=None):
        cmd = self._get_cmd(cmd)
        timeout = self._get_effective_timeout(timeout)
        stdin = self._get_istream(stdin)
        bcms, pstdin = (stdin, subprocess.PIPE) if isinstance(stdin, bytes) else (None, stdin)
        def _out(o):
            t = None
            if o:
                try:
                    o.fileno()
                    supp = True
                except io.UnsupportedOperation:
                    supp = False
                if not supp:
                    t = o
                    o = subprocess.PIPE
            return o, t
        pstdout, txtout = _out(stdout)
        pstderr, txterr = _out(stderr)
        penv = dict(os.environb)
        for ke, ve in (env or {}).items():
            ke = ke.encode() if isinstance(ke, str) else ke
            ve = ve.encode() if isinstance(ve, str) else ve
            penv[ke] = ve
        logging.debug(f"pish execute cmd: {cmd}")
        with subprocess.Popen(cmd, stdin=pstdin, stdout=pstdout, stderr=pstderr, env=penv) as p:
            try:
                to, te = p.communicate(bcms, timeout=timeout)
            except subprocess.TimeoutExpired as e:
                raise TimeoutExpiredError() from e
            retcode = p.returncode
        if txtout:
            txtout.write(to)
        if txterr:
            txterr.write(te)
        return retcode


class SshConnection(Connection):
    """
    See pish.Connection.
    """

    def __init__(self, *, host, port, username, sshoptions=None, **b):
        b["basetimeout"] = b.get("basetimeout", 60 * 1.0)
        super().__init__(**b)
        self.host = host
        self.port = int(port or 22)
        self.username = username
        self.sshoptions = sshoptions if (sshoptions is not None) else \
            {"PreferredAuthentications": "publickey", "ServerAliveInterval": 17, "ServerAliveCountMax": 4}

    def conninfo_to_plainobjs(self):
        res = super().conninfo_to_plainobjs()
        res["host"] = self.host
        res["port"] = self.port
        res["username"] = self.username
        res["sshoptions"] = self.sshoptions
        return res

    def _str_pieces(self):
        return [("host", self.host), ("port", self.port), ("username", self.username)]

    def _get_cmdprep(self, bc, penv):
        return bc

    def _mod_sshcmd(self, sshargs, sshopts):
        pass

    def execute(self, *cmd, stdin=b"", stdout=None, stderr=None, env=None, timeout=None):
        cmd = self._get_cmd(cmd)
        timeout = self._get_effective_timeout(timeout)
        qcmds = " ".join(shlex.quote(x) for x in cmd)
        qcmds += ";if [ $? != 0 ];then exit 85; else exit 0; fi"
        sdest = f"{self.username}@{self.host}" if self.username else self.host
        sport = f"-p{self.port}"
        sshopts = dict(self.sshoptions)
        if "ConnectTimeout" not in sshopts:
            sshopts["ConnectTimeout"] = timeout + 5  # little more, so error behavior doesnt depend on that race
        sshargs = []
        self._mod_sshcmd(sshargs, sshopts)
        scaux = " ".join(shlex.quote(x) for x in sshargs)
        scops = " ".join(f"-o {kx}={shlex.quote(str(vx))}" for kx, vx in sshopts.items())
        penv = {}
        for ke, ve in (env or {}).items():
            ke = ke.decode() if isinstance(ke, bytes) else ke
            penv[f"LC_{ke}"] = ve
            qcmds = f'export {ke}="$LC_{ke}";{qcmds}'
        bc = self._get_cmdprep(f"ssh -qt {sdest} {sport} {scops} {scaux} {shlex.quote(qcmds)}", penv)
        retval = self.parentconn.bash(bc, stdin=stdin, stdout=stdout, stderr=stderr, env=penv, timeout=timeout)
        if retval == 0:
            return 0
        elif retval == 85:
            return 1
        else:
            raise SshConnectionError(self, f"error #{retval}")


class SshPasswordConnection(SshConnection):
    """
    See pish.SshConnection.
    """

    def __init__(self, *, password, **b):
        super().__init__(**b)
        self.password = password

    def conninfo_to_plainobjs(self):
        res = super().conninfo_to_plainobjs()
        res["password"] = self.password
        return res

    def _get_cmdprep(self, bc, penv):
        bc = super()._get_cmdprep(bc, penv)
        return self.cmdlinebuilder.run__askpass(bc, env=penv, askpassfct=self.cmdlinebuilder.ssh_askpass,
                                                password=self.password)

    def _mod_sshcmd(self, sshargs, sshopts):
        super()._mod_sshcmd(sshargs, sshopts)
        sshopts["PreferredAuthentications"] = "password"
        if isinstance(self.password, str):
            sshopts["NumberOfPasswordPrompts"] = "1"


class SshIdfileConnection(SshConnection):
    """
    See pish.SshConnection.
    """

    def __init__(self, *, idfile, **b):
        super().__init__(**b)
        self.idfile = idfile

    def conninfo_to_plainobjs(self):
        res = super().conninfo_to_plainobjs()
        res["idfile"] = self.idfile
        return res

    def _mod_sshcmd(self, sshargs, sshopts):
        super()._mod_sshcmd(sshargs, sshopts)
        sshargs += ["-i", self.idfile]

    def _str_pieces(self):
        r = super()._str_pieces()
        r.insert(len(r)-2, ("idfile", self.idfile))
        return r


class ElevateSuConnection(Connection):
    """
    See pish.Connection.
    """

    def __init__(self, *, username, password, **b):
        b["basetimeout"] = b.get("basetimeout", 3)
        super().__init__(**b)
        self.username = username or "root"
        self.password = password if isinstance(password, str) else None
        self.basetimeout = 10

    def _str_pieces(self):
        return [("username", self.username)]

    def conninfo_to_plainobjs(self):
        res = super().conninfo_to_plainobjs()
        res["username"] = self.username
        res["password"] = self.password
        return res

    def execute(self, *cmd, stdin=b"", stdout=None, stderr=None, env=None, timeout=None):
        cmd = self._get_cmd(cmd)
        timeout = self._get_effective_timeout(timeout)
        qcmds = " ".join(shlex.quote(x) for x in cmd)
        if self.password:
            stdin = self._get_istream(self.password+"\n", stdin)
        if stderr:
            origstderr = stderr
            stderr = io.BytesIO()
        else:
            origstderr = None
        bc = f"su -c {shlex.quote(qcmds)} {shlex.quote(self.username)} -"
        try:
            return self.parentconn.bash(bc, stdin=stdin, stdout=stdout, stderr=stderr, env=env, timeout=timeout)
        finally:
            if origstderr:
                data = stderr.getvalue()
                ifl = data.find(b"\n")
                if ifl > -1:
                    ifl = len(data)
                icl = data.find(b":", 0, ifl)
                if icl > -1:
                    data = data[icl+1:].lstrip()
                origstderr.write(data)


class ElevateSudoConnection(Connection):
    """
    See pish.Connection.
    """

    def __init__(self, *, username, password, direct, **b):
        b["basetimeout"] = b.get("basetimeout", 3)
        super().__init__(**b)
        self.username = username or "root"
        self.password = password if isinstance(password, str) else None
        self.direct = direct
        self.basetimeout = 10

    def _str_pieces(self):
        return [("username", self.username)]

    def conninfo_to_plainobjs(self):
        res = super().conninfo_to_plainobjs()
        res["username"] = self.username
        res["password"] = self.password
        res["direct"] = self.direct
        return res

    def execute(self, *cmd, stdin=b"", stdout=None, stderr=None, env=None, timeout=None):
        cmd = self._get_cmd(cmd)
        timeout = self._get_effective_timeout(timeout)
        qcmds = " ".join(shlex.quote(x) for x in cmd)
        direct = (not bool(env)) if (self.direct is None) else self.direct
        penv = {}
        for ke, kv in (env or {}).items():
            ke = ke.decode() if isinstance(ke, bytes) else ke
            kv = kv.encode() if isinstance(kv, str) else kv
            penv["LC_" + ke] = base64.b32encode(kv)  # sudo drops the variable when some chars (/, %) are in it
            if not direct:
                qcmds = f'export {ke}="$(echo $LC_{ke}|base32 -d)";{qcmds}'
        bc = qcmds if direct else f"bash -c {shlex.quote(qcmds)}"
        bc = f" --user={self.username} {bc}"
        bc = self.cmdlinebuilder.run__askpass(bc, env=penv, askpassfct=self.cmdlinebuilder.sudo_askpass,
                                              password=self.password, onpasswordcmdpre="sudo -AH",
                                              onnopasswordcmdpre="sudo -H")
        return self.parentconn.bash(bc, stdin=stdin, stdout=stdout, stderr=stderr, env=penv, timeout=timeout)


_i_uniqid, _uniqid_lock = 0, threading.Lock()


def get_unique(*, tiny=False) -> str:
    """
    Only used internally. Creates a unique id.
    """
    global _i_uniqid
    with _uniqid_lock:
        _i_uniqid += 1
        res = f"_pysshman_{_i_uniqid}"
        if not tiny:
            res += f"_{os.getpid()}_{socket.getfqdn()}_{time.time()}"
        return res


class CommandLineBuilder:
    """
    Used internally for command line creation.
    """

    def __init__(self, *, conn=None):
        self.conn = conn

    def with_pre_and_post(self, cmd, *, pre="", post="",
                          prein="&-", preout="/dev/null", preerr="/dev/null",
                          postin="&-", postout="/dev/null", posterr="/dev/null"):
        if preerr == preout:
            preerr = "&1"
        if posterr == postout:
            posterr = "&1"
        if pre:
            spre = f"({pre})<{prein} >{preout} 2>{preerr};"
        else:
            spre = ""
        if post:
            spost = f"({post})<{postin} >{postout} 2>{posterr};"
        else:
            spost = ""
        return f"({spre}({cmd});_pysshman_r=$?;{spost}exit $_pysshman_r)"

    def askpass(self, cmd, pk_passwd):
        qaskp = shlex.quote(f'#!/bin/bash\necho "${pk_passwd}"')
        qfaskp, faskpcmd = self.file_with_content(qcontent=qaskp, qlocation="~/.", chmod="+x")
        return self.with_pre_and_post(f"export _pysshman_askpass={qfaskp};{cmd}", pre=faskpcmd, post=f"rm {qfaskp}")

    def file_with_content(self, *, qcontent, qlocation="/tmp/", chmod="", defltchmod="g=,o="):
        qff = f"{qlocation}{shlex.quote(get_unique())}"
        qmod = shlex.quote(f"{defltchmod},{chmod}".strip(","))
        return qff, f"(touch {qff};chmod {qmod} {qff};echo {qcontent} >{qff})<&-"

    def ssh_askpass(self, cmd, pk_passwd):
        return self.askpass(f'export SSH_ASKPASS="$_pysshman_askpass";export DISPLAY=:;setsid {cmd}', pk_passwd)

    def sudo_askpass(self, cmd, pk_passwd):
        return self.askpass(f'export SUDO_ASKPASS="$_pysshman_askpass";{cmd}', pk_passwd)

    def run__askpass(self, cmd, *, env, askpassfct, password, onpasswordcmdpre=None, onnopasswordcmdpre=None):
        if isinstance(password, str):
            if onpasswordcmdpre:
                cmd = f"{onpasswordcmdpre}{cmd}"
            pk_passwd = get_unique(tiny=True)
            env[pk_passwd] = password
            cmd = askpassfct(cmd, pk_passwd)
        else:
            if onnopasswordcmdpre:
                cmd = f"{onnopasswordcmdpre}{cmd}"
        return cmd


localhost: LocalhostConnection = LocalhostConnection()

#TODO# better pypi
