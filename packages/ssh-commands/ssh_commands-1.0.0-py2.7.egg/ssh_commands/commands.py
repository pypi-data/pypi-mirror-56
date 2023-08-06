"""
Helper commands for cryptography, secrets and installers.

Defined all needed functions for keys generate, ssh connection
and run ssh command.
"""
import datetime
import re
from os import getenv
from os.path import join, abspath, dirname, exists
from random import choice
from subprocess import check_call, check_output, CalledProcessError
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from gitlab import Gitlab
from yaml import load
from ssh_commands.Singleton import Singleton

key_pass = ""

if exists("./id_rsa.pass"):
    key_pass = open("./id_rsa.pass").read().strip()

key = "./id_rsa"

projects = []


def prepare_ssh(host, ssh_command="ssh", user=None, pass_phrase=None, private_key=None, local_path=None):
    """
    Prepare ssh command.
    Switch host, user, private_key, passphrase if need and return bash statement.

    :param host: SSH host.
    :type host: str
    :param ssh_command: Command type. `scp` or `ssh`
    :type ssh_command: str
    :param user: Username
    :type user: None|str
    :param pass_phrase: Passphrase for private key.
    :type pass_phrase: str
    :param private_key: Private key path.
    :type private_key: str
    :param local_path: Local path for scp.
    :type local_path: str

    :return: str
    """
    global key_pass, key

    SSHCommand(key, key_pass, "10.118.48.30")
    private_key = SSHCommand().private_key if private_key is None else private_key
    pass_phrase = SSHCommand().passphrase if pass_phrase is None else pass_phrase
    user = SSHCommand().user if user is None else user

    SSHCommand().change_host(host).change_passphrase(pass_phrase) \
        .change_user(user).change_private_key(private_key)

    cmd = SSHCommand().get_ssh_command(ssh_command, local_path)

    return cmd.replace("\n", " ").replace("\r", " ")


def generate_password(count_symbols=15):
    """
    Generate password.

    :param count_symbols: Count symbols
    :type count_symbols: int

    :return: str
    """
    chars = '1234567890qwertyuiopasdfghjklzxcvbnm'
    password = ""
    for num in range(count_symbols):
        password += choice(chars)

    return password


def generate_key(bits, dns="Ministra Middleware", passphrase=None):
    """
    Generate public key, signed certificate and public key

    :param bits: Count bits (key size)
    :type bits: int
    :param dns: Certificate CN record
    :type dns: str
    :param passphrase: Passphrase for private key
    :type passphrase: str|None

    :return:
    """
    # generate private/public key pair
    private_key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=bits)

    # get public key in OpenSSH format
    public_key = private_key.public_key()
    public_key_bytes = public_key.public_bytes(serialization.Encoding.OpenSSH,
                                               serialization.PublicFormat.OpenSSH)

    # get private key in PEM container format

    enc = serialization.NoEncryption()
    if passphrase is not None:
        enc = serialization.BestAvailableEncryption(passphrase)

    pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                                    encryption_algorithm=enc)

    # decode to echoable strings
    private_key_str = pem.decode('utf-8')
    public_key_str = public_key_bytes.decode('utf-8')

    builder = x509.CertificateBuilder()
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u"{0}".format(dns)),
    ]))
    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u"{0} CA".format(dns)),
    ]))

    one_day = datetime.timedelta(1, 0, 0)
    builder = builder.not_valid_before(datetime.datetime.today() - one_day)
    builder = builder.not_valid_after(datetime.datetime.today() + (one_day * 2))
    builder = builder.public_key(public_key)
    builder = builder.add_extension(
        x509.SubjectAlternativeName(
            [x509.DNSName(u"{0}".format(dns))]
        ),
        critical=False
    ).serial_number(
        x509.random_serial_number()
    )
    builder = builder.add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True,
    )
    certificate = builder.sign(
        private_key=private_key, algorithm=hashes.SHA256(),
        backend=default_backend()
    )

    return [private_key_str, public_key_str, certificate.public_bytes(serialization.Encoding.PEM)]


def run_commands_on_nodes(commands, servers, check_command=None, get_output=False, user=None):
    """
    | Run command on each nodes from ``servers``.
    If before run you must check command execution, set it as ``check_command``
    argument. Before run commands list for node, script check command and
    run needed command only if check_command raised exception.

    :param commands: Commands list
    :type commands: str|list
    :param servers: Nodes list
    :type servers: list
    :param check_command: Check command. Use for run operation only if check command raised exception
    :type check_command: str
    :param get_output: Return output after run. Output would be concatenated from all command run without delimiter
    :type get_output: bool
    :param user: User for run command
    :type user: str

    :return: str

    :raises: Exception if command run fails
    """
    global key
    output = ""
    for server in servers:
        if check_command is not None:
            try:
                check_output(
                    prepare_ssh(host=server, user=user) + " {cmd}".format(cmd=check_command), shell=True
                )
                continue
            except CalledProcessError:
                pass
        for command in commands:
            # echo("\n\n{0}\n\n".format(command))
            command = prepare_ssh(host=server, user=user) + " {cmd}".format(cmd=command)
            echo(command)
            if get_output:
                output += check_output(command, shell=True).decode("utf-8")
            else:
                check_call(command, shell=True)

    return output.strip()


def check_gluster_volume_exists(node, vol_name):
    """
    Check gluster volume exists on node.

    :param node: Volume name
    :type node: str
    :param vol_name: Volume name
    :type vol_name: str

    :return: bool

    :raises:
        Exception if command run fails
    """
    try:
        run_commands_on_nodes(["gluster volume status " + vol_name], [node], "gluster volume status " + vol_name)
        return True
    except:
        return False


def __get_node_name_from_out(out):
    """
    Match hostname from command.

    :param out: Console output.
    :type out: str

    :return: str
    """
    matches = re.findall(r"Enter passphrase for key", str(out))
    if matches is not None:
        out = out.decode("utf-8") if isinstance(out, bytes) else out
        out_dict = out.split(":")
        hostname = out_dict[len(out_dict) - 1].strip()
        return hostname

    return out


def get_nodes_hostname_by_ip(nodes):
    """
    Get nodes hostname by ip for node. Using in swarm mode for get node name in swarm cluster.

    :param nodes: Nodes list
    :param nodes: str|list

    :returns str: If nodes list is once
    :returns list: If nodes list is multiple
    """
    if isinstance(nodes, str):
        command = prepare_ssh(nodes) + " {cmd}".format(cmd="hostname")
        out = check_output(command, shell=True).strip()
        return __get_node_name_from_out(out)

    hosts = []

    for node in nodes:
        command = prepare_ssh(node) + " {cmd}".format(cmd="hostname")
        hosts.append(__get_node_name_from_out(check_output(command, shell=True).strip()))

    return hosts


def create_gluster_main_volume(
        master_node,
        vol_name,
        path,
        remote_path,
        nodes_replicas):
    """
    Create glusterfs volume in cluster.

    :param master_node: Master node ip.
    :param master_node: str
    :param vol_name: Volume name
    :param vol_name: str
    :param path: Volume path on glusterfs
    :param path: str
    :param remote_path: Volume replication path
    :param remote_path: str
    :param nodes_replicas: Replication nodes list
    :param nodes_replicas: list

    :return: None

    :raises:
        Exception if command run fails
    """
    node_replicas_config = [
        "{0}:{1}".format(get_nodes_hostname_by_ip(master_node), path)
    ]

    for node in nodes_replicas:
        node_replicas_config.append("{0}:{1}".format(get_nodes_hostname_by_ip(node), path))

    run_commands_on_nodes([
        "\"mkdir -p " + path + " || true\""
    ], [master_node])

    run_commands_on_nodes([
        "\"mkdir -p " + remote_path + " || true\""
    ], [master_node])

    for node, node_repl_path in nodes_replicas.items():
        run_commands_on_nodes([
            "\"mkdir -p " + path + " || true\""
        ], [node])

        run_commands_on_nodes([
            "\"mkdir -p " + node_repl_path + " || true\""
        ], [node])

    run_commands_on_nodes([
        "gluster volume create {0} replica {1} {2} force".format(
            vol_name,
            len(nodes_replicas) + 1,
            " ".join(node_replicas_config)
        )
    ], [master_node])
    run_commands_on_nodes([
        "gluster volume set {vol_name} auth.allow 127.0.0.1".format(vol_name=vol_name)
    ], [master_node])
    run_commands_on_nodes([
        "gluster volume start {vol_name}".format(vol_name=vol_name)
    ], [master_node])
    run_commands_on_nodes([
        "mount -t glusterfs localhost:/{vol_name} {r_path}".format(vol_name=vol_name, r_path=remote_path)
    ], [master_node])
    for node, node_repl_path in nodes_replicas.items():
        run_commands_on_nodes([
            "mount -t glusterfs localhost:/{vol_name} {r_path}".format(vol_name=vol_name, r_path=remote_path)
        ], [node])


def get_config():
    """
    Get yaml config for deployment.

    :return: dict
    """
    filename = join(abspath("./"), "config.yaml")
    return load(open(filename))


def copy_remote(local_path, remote_dir, ip, bkp_path=None, user=None):
    """
    Copy files on remote with backup old content.

    :param local_path: Local path
    :type local_path: str
    :param remote_dir: Remote dir
    :type remote_dir: str
    :param ip: Node ip
    :type ip: str|list
    :param bkp_path: Backup path
    :type bkp_path: str
    :param user: Remote user name
    :type user: str

    :return:
    """
    global key

    run_commands_on_nodes(
        commands=[
            "mkdir -p {dest}".format(dest=bkp_path),
        ],
        servers=ip if isinstance(ip, list) else [ip],
        check_command="ls {dest}".format(dest=bkp_path),
        user=user,
    )
    run_commands_on_nodes(
        commands=[
            "cp -r {orig} {dest}".format(dest=bkp_path, orig=remote_dir),
        ],
        servers=ip if isinstance(ip, list) else [ip],
        user=user
    )

    if bkp_path is not None:
        if isinstance(ip, list):
            for remote in ip:
                copy_remote(local_path, remote_dir, remote, bkp_path, user)

    if isinstance(ip, list):
        for remote in ip:
            copy_remote(local_path, remote_dir, remote, bkp_path, user)
    else:
        prepare_ssh(host=ip, user=user)
        check_call(
            SSHCommand().get_rsync_command(local_path, "{user}@{host}:" + remote_dir),
            shell=True
        )


def restore_remote(remote_dir, bkp_path, ip, user=None):
    """
    Restore remote content from backup.

    :param remote_dir: Remote dir
    :type remote_dir: str
    :param bkp_path: Backup path
    :type bkp_path: str
    :param ip: Node ip
    :type ip: str
    :param user: Change user
    :type user: str

    :return: None

    :raises:
        Exception if command run fails
    """
    if isinstance(ip, list):
        for remote in ip:
            restore_remote(remote_dir, bkp_path, remote, user)
    else:
        run_commands_on_nodes(
            commands=[
                "cp -r {orig} {dest}".format(orig=bkp_path, dest=remote_dir),
                "rm -rf {dest}".format(dest=bkp_path),
            ],
            servers=[ip],
            user=user
        )


def get_projects(config):
    """
    Get gitlab projects list.

    :param config: Config
    :type config: dict

    :returns: :py:class:`gitlab.v4.objects.ProjectManager`
    """
    global projects

    if projects is not None and len(projects) > 0:
        return projects

    gitlab = Gitlab(
        url=config.get("gitlab_url"),
        private_token=getenv("GITLAB_PRIVATE_TOKEN")
    )

    projects = gitlab.projects.list()
    groups = gitlab.groups
    for group in groups.list():
        for project in group.projects.list():
            project = gitlab.projects.get(project.id)
            projects.append(project)

    return projects


def vars_and_ids(vars):
    """
    Find vars and ids projects from gitlab.

    :param vars: Variables from config.
    :type vars: dict

    :return: list
    """
    out_vars = {}

    for project in get_projects(get_config()):
        variables = project.variables.list()
        for variable in variables:
            result = find_var(variable, vars)

            if result:
                if out_vars.get(result) is None:
                    out_vars[result] = []

                out_vars[result].append(variable)

    return out_vars


def find_var(variable, vars, ret_origin=False):
    """
    Find secrets variables in variables list from project.
    | Format for `vars` argument:

   ``{"variable_name": ["ALIAS_1", "ALIAS_2", ..., "ALIAS_N"]}``

   Alias list compared with secret variables name in gitlab and return true if variable was found.

    :param variable: Environment variable object.
    :type variable: :py:class:`gitlab.v4.objects.ProjectVariable`
    :param vars: Replaced vars config.
    :type vars: dict
    :param ret_origin: Return origin variable
    :type ret_origin: bool

    :returns:
        Variable name if variable was found.

        If variable does not found, returned ``False``
    """
    for var_name, names in vars.items():
        for name in names:
            if variable.key == name:
                return var_name if not ret_origin else name

    return False


def replace_secret_vars_projects(vars, content):
    """
    | Replace secrets variables in gitlab projects.
    | How it works:
    | You must stored in environment variable `GITLAB_PRIVATE_TOKEN` your token from gitlab
    | https://gitlab.infomir.com.ua/profile/personal_access_tokens
    | Now you can replace secret variables for projects.
    | Format:

       ``{"variable_name": ["ALIAS_1", "ALIAS_2", ..., "ALIAS_N"]}``

    | It is dictionary with variables aliases in gitlab.
    | Script search all variables in projects and filter needed.
    | After find script search value for variable in `content` dictionary.
    | IF content founded, script replaced variable value and save them.

    :param vars: Variables list
    :type vars: dict
    :param content: New content
    :type content: dict

    :return:
    """
    out_vars = vars_and_ids(vars)

    for name, variables in out_vars.items():
        echo(name, "\n")
        if name not in content:
            continue

        edited_content = content[name] if not exists(content[name]) else open(content[name]).read()

        for variable in variables:
            variable.value = edited_content
            echo(variable.save())


def echo(*args):
    """
    echo text with Popen.

    :param args: Text
    :type args: list(str)

    :return:
    """
    for item in args:
        text = "echo \"{text}\"".format(text=str(item).replace("\"", "\\\""))
        check_call(text, shell=True)


def get_key_pass():
    """
    Get private key passphrase.

    :return: str
    """
    global key_pass
    return key_pass


def change_key_pass(password):
    """
    Change private key passphrase for next usages after change.

    :param password: Password.
    :type password: str

    :return:
    """
    global key_pass
    key_pass = password


class SSHCommand(Singleton):
    """
    Arguments:
          passphrase(str): Private key passphrase
          private_key(str): Private key full path

    Properties:
          passphrase(str): Private key passphrase
          private_key(str): Private key full path
          inited(bool): Init flag. If constructor called, return without set
    """

    def __init__(self, private_key=None, passphrase="", host=None):
        self.config = get_config()
        self.host = host if host is not None else self.config.get("master")
        self.passphrase = passphrase
        if len(passphrase) == 0 and exists("./id_rsa.pass"):
            self.passphrase = open("./id_rsa.pass").read()

        self.private_key = private_key if private_key is not None else "./id_rsa"
        self.user = "root"

    @property
    def private_key(self):
        return self.__private_key

    @private_key.setter
    def private_key(self, new_path):
        """
        Change private path

        :param new_path: Full path to new private file.
        :type new_path: str

        :return:
        """
        if new_path is None or not isinstance(new_path, str) or not exists(new_path):
            raise RuntimeWarning("New private file does not find")

        self.__private_key = new_path

    @property
    def passphrase(self):
        return self.__passphrase

    @passphrase.setter
    def passphrase(self, passphrase):
        """
        Change private path

        :param passphrase: Private key passphrase
        :type passphrase: str

        :return:
        """
        self.__passphrase = passphrase

    @property
    def user(self):
        return self.__username

    @user.setter
    def user(self, user):
        if len(user) == 0 or not isinstance(user, str):
            raise AttributeError("Invalid username value")

        self.__username = user

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, hostname):
        self.__host = hostname

    def change_user(self, username):
        """
        Change ssh username.

        :param username: Username
        :type username: str

        :return: :class:`SSHCommand`
        """
        self.user = username

        return self

    def change_passphrase(self, passphrase):
        """
        Change ssh private key passphrase.

        :param passphrase: Username
        :type passphrase: str

        :return: :class:`SSHCommand`
        """
        self.__passphrase = passphrase

        return self

    def change_host(self, host):
        """
        Change ssh host.

        :param host: SSH host
        :type host: str

        :return: :class:`SSHCommand`
        """
        self.__host = host

        return self

    def change_private_key(self, private_key):
        """
        Change private key file path.

        :param private_key: Private key path
        :type private_key: str

        :return: :class:`SSHCommand`
        """
        self.__private_key = private_key

        return self

    def get_rsync_command(self, local_path=None, destination=None):
        """
        Get rsync command with private key adding and entering password if needed.

        :param local_path: Local path for scp
        :type local_path: str|None
        :param destination: Destination path for scp
        :type destination: str|None

        :return:
        """
        if self.host is None or not isinstance(self.host, str):
            raise AttributeError("Host is empty")

        if self.user is None or not isinstance(self.user, str):
            raise AttributeError("Username is empty")

        command = "rsync --chmod=o-r --rsh=ssh -e \"ssh -i {priv_key}\" {local} {dest}"
        if len(self.__passphrase) > 0:
            command = "{exp_path} {password} " + command

        destination = destination if destination is not None else "{user}@{host}"
        destination = destination.format(
            user=self.user,
            host=self.host
        )
        local_path = local_path if local_path is not None else ""

        if command == "scp" and len(local_path) == 0:
            raise AttributeError("Local path is empty for scp")

        cmd = command.format(
            exp_path=join("./", dirname(__file__), "exp"),
            password=self.passphrase,
            priv_key=self.private_key,
            local=local_path,
            dest=destination,
            user=self.user,
        )

        echo("Destination ", destination)
        echo("Command ", cmd)

        return cmd.replace("\n", " ")

    def get_ssh_command(self, command="ssh", local_path=None, destination=None):
            """
            Get ssh command with private key adding and entering password if needed.

            :param command: Command name. `ssh` or `scp`
            :type command: str
            :param local_path: Local path for scp
            :type local_path: str|None
            :param destination: Destination path for scp
            :type destination: str|None

            :return:
            """
            if self.host is None or not isinstance(self.host, str):
                raise AttributeError("Host is empty")

            if self.user is None or not isinstance(self.user, str):
                raise AttributeError("Username is empty")

            command = command + " -i {priv_key} {local} {dest}"
            if len(self.__passphrase) > 0:
                command = "{exp_path} {password} " + command

            destination = destination if destination is not None else "{user}@{host}".format(
                user=self.user,
                host=self.host
            )
            local_path = local_path if local_path is not None else ""

            if command == "scp" and len(local_path) == 0:
                raise AttributeError("Local path is empty for scp")

            command = command.format(
                exp_path=join("./", dirname(__file__), "exp"),
                password=self.passphrase,
                priv_key=self.private_key,
                local=local_path,
                dest=destination
            )

            return command.replace("\n", " ")


if __name__ == "__main__":
    # ssh = SSHCommand("./id_rsa_root", open("./id_rsa_root.pass").read(), "10.118.48.30")
    # echo(ssh.get_ssh_command("ssh"))
    # SSHCommand().user = "user"
    # SSHCommand().change_host("10.118.48.31")\
    #     .change_user("user")\
    #     .change_passphrase("123")
    # echo(SSHCommand().get_ssh_command())
    # echo(ssh.user)
    # projects = get_projects(config=get_config())
    # variables = vars_and_ids({
    #     "private_key_var_names": ["DEPLOYMENT_DEPLOY_SSH_PRIVATE_KEY"]
    # })
    # variables.get("private_key_var_names")[0].value = 123
    # variables.get("private_key_var_names")[0].save()
    # echo(variables.get("private_key_var_names"))
    exit(1)
