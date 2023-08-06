#!/usr/bin/env python3

"""
Daka
A very small PaaS to do git push deployments to your own servers.
"""

try:
    from sys import version_info
    assert version_info >= (3, 5)
except AssertionError:
    exit("Daka requires Python >= 3.5")

import sys
import click
import json
import configparser
from click import secho as echo
from collections import defaultdict, deque
from datetime import datetime
from fcntl import fcntl, F_SETFL, F_GETFL
from glob import glob
from hashlib import md5
from multiprocessing import cpu_count
from os import chmod, getgid, getuid, symlink, unlink, remove, stat, listdir, environ, makedirs, O_NONBLOCK
from os.path import abspath, basename, dirname, exists, getmtime, join, realpath, splitext
from re import sub
from shutil import copyfile, rmtree, which
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv, stdin, stdout, stderr, version_info, exit
from stat import S_IRUSR, S_IWUSR, S_IXUSR
from subprocess import call, check_output, Popen, STDOUT, PIPE
from tempfile import NamedTemporaryFile
from traceback import format_exc
from time import sleep
import urllib.request
from urllib.request import urlopen
from pwd import getpwuid
from grp import getgrgid

# -----------------------------------------------------------------------------

NAME = "Daka"
VERSION = "0.1.0"
VALID_RUNTIME = ["python", "node", "static", "shell"]


DAKA_SCRIPT = realpath(__file__)
DAKA_ROOT = environ.get('DAKA_ROOT', environ['HOME'])
DAKA_BIN = join(environ['HOME'], 'bin')
APP_ROOT = abspath(join(DAKA_ROOT, "apps"))
DOT_ROOT = abspath(join(DAKA_ROOT, ".daka"))
ENV_ROOT = abspath(join(DOT_ROOT, "envs"))
GIT_ROOT = abspath(join(DOT_ROOT, "repos"))
LOG_ROOT = abspath(join(DOT_ROOT, "logs"))
NGINX_ROOT = abspath(join(DOT_ROOT, "nginx"))
METRICS_ROOT = abspath(join(DOT_ROOT, "metrics"))
SETTINGS_ROOT = abspath(join(DOT_ROOT, "settings"))
UWSGI_AVAILABLE = abspath(join(DOT_ROOT, "uwsgi-available"))
UWSGI_ENABLED = abspath(join(DOT_ROOT, "uwsgi-enabled"))
UWSGI_ROOT = abspath(join(DOT_ROOT, "uwsgi"))

ACME_ROOT = environ.get('ACME_ROOT', join(environ['HOME'], '.acme.sh'))
ACME_WWW = abspath(join(DOT_ROOT, "acme"))
UWSGI_LOG_MAXSIZE = '1048576'

if 'sbin' not in environ['PATH']:
    environ['PATH'] = "/usr/local/sbin:/usr/sbin:/sbin:" + environ['PATH']

if DAKA_BIN not in environ['PATH']:
    environ['PATH'] = DAKA_BIN + ":" + environ['PATH']

# -----------------------------------------------------------------------------
# NGINX
NGINX_TEMPLATE = """
upstream $APP {
  server $NGINX_SOCKET;
}
server {
  listen              $NGINX_IPV6_ADDRESS:80;
  listen              $NGINX_IPV4_ADDRESS:80;

  location ^~ /.well-known/acme-challenge {
    allow all;
    root ${ACME_WWW};
  }

$INTERNAL_NGINX_COMMON
}
"""

NGINX_HTTPS_ONLY_TEMPLATE = """
upstream $APP {
  server $NGINX_SOCKET;
}
server {
  listen              $NGINX_IPV6_ADDRESS:80;
  listen              $NGINX_IPV4_ADDRESS:80;
  server_name         $NGINX_SERVER_NAME;

  location ^~ /.well-known/acme-challenge {
    allow all;
    root ${ACME_WWW};
  }

  location / {
    return 301 https://$server_name$request_uri;
  }
}

server {
$INTERNAL_NGINX_COMMON
}
"""

NGINX_COMMON_FRAGMENT = """
  listen              $NGINX_IPV6_ADDRESS:$NGINX_SSL;
  listen              $NGINX_IPV4_ADDRESS:$NGINX_SSL;
  ssl                 on;
  ssl_certificate     $NGINX_ROOT/$APP.crt;
  ssl_certificate_key $NGINX_ROOT/$APP.key;
  server_name         $NGINX_SERVER_NAME;

  # These are not required under systemd - enable for debugging only
  # access_log        $LOG_ROOT/$APP/access.log;
  # error_log         $LOG_ROOT/$APP/error.log;
  
  # Enable gzip compression
  gzip on;
  gzip_proxied any;
  gzip_types text/plain text/xml text/css application/x-javascript text/javascript application/xml+rss application/atom+xml;
  gzip_comp_level 7;
  gzip_min_length 2048;
  gzip_vary on;
  gzip_disable "MSIE [1-6]\.(?!.*SV1)";

  $INTERNAL_NGINX_CUSTOM_CLAUSES

  $INTERNAL_NGINX_STATIC_CLAUSES

  $INTERNAL_NGINX_STATIC_MAPPINGS

  $INTERNAL_NGINX_PORTMAP
"""

NGINX_PORTMAP_FRAGMENT = """
  location    / {
    $INTERNAL_NGINX_UWSGI_SETTINGS
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $http_host;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_set_header X-Forwarded-Port $server_port;
    proxy_set_header X-Request-Start $msec;
    $NGINX_ACL
  }
"""

NGINX_ACME_FIRSTRUN_TEMPLATE = """
    server {
        listen              $NGINX_IPV6_ADDRESS:80;
        listen              $NGINX_IPV4_ADDRESS:80;
        server_name         $NGINX_SERVER_NAME;
        location ^~ /.well-known/acme-challenge {
            allow all;
            root ${ACME_WWW};
        }
    }
"""

INTERNAL_NGINX_STATIC_MAPPING = """
  location $static_url {
      sendfile on;
      sendfile_max_chunk 1m;
      tcp_nopush on;
      directio 8m;
      aio threads;
      alias $static_path;
  }
"""

INTERNAL_NGINX_UWSGI_SETTINGS = """
    uwsgi_pass $APP;
    uwsgi_param QUERY_STRING $query_string;
    uwsgi_param REQUEST_METHOD $request_method;
    uwsgi_param CONTENT_TYPE $content_type;
    uwsgi_param CONTENT_LENGTH $content_length;
    uwsgi_param REQUEST_URI $request_uri;
    uwsgi_param PATH_INFO $document_uri;
    uwsgi_param DOCUMENT_ROOT $document_root;
    uwsgi_param SERVER_PROTOCOL $server_protocol;
    uwsgi_param REMOTE_ADDR $remote_addr;
    uwsgi_param REMOTE_PORT $remote_port;
    uwsgi_param SERVER_ADDR $server_addr;
    uwsgi_param SERVER_PORT $server_port;
    uwsgi_param SERVER_NAME $server_name;
"""

INTERNAL_NGINX_STATIC_CLAUSES = """

    # static: html & php

    root $html_root;
    index index.html index.htm index.php;
    location / {
        try_files $uri $uri/ =404;
    } 
    
    # Pass PHP scripts to PHP-FPM
    location ~* \.php$ {
        fastcgi_index   index.php;
        fastcgi_pass unix:/var/run/php/php7.2-fpm.sock;
        include         fastcgi_params;
        fastcgi_param   SCRIPT_FILENAME    $document_root$fastcgi_script_name;
        fastcgi_param   SCRIPT_NAME        $fastcgi_script_name;
    } 

    location ~ /\.ht {
        deny all;
    }
"""
# -----------------------------------------------------------------------------


def any_in_list(l1, t2):
    return any((True for x in l1 if x in t2))


def print_table(table, with_header=True):
    """
    To print data in table.
    :param table: list of lists 
    :param with_header: True if the first row is the header
    table = [
        ["ABC", "Man Utd", "Man City", "T Hotspur"],
        ["Man Utd", 1, 0, 0],
        ["Man City", 1, 1, 0],
        ["T Hotspur", 0, 1, 2],
    ]
    print_table(table)
    """
    longest_cols = [
        (max([len(str(row[i])) for row in table]) + 3)
        for i in range(len(table[0]))
        ]
    cols_size_sum = sum(longest_cols)
    row_format = "".join(["{:<" + str(longest_col) + "}" for longest_col in longest_cols])
    line = "-" * cols_size_sum
    if with_header:
        headers = table.pop(0)
        print(line)
        print(row_format.format(*headers))
        print(line)
    for row in table:
        print(row_format.format(*row))
    print(line)


def print_title(title=None, app=None):
    print("-" * 80)
    print("Daka v%s" % VERSION)
    if app:
        print("App: %s" % app)
    if title:
        print(title)
    print(" ")


def human_size(n):
    # G
    if n >= (1024*1024*1024):
        return "%.1fG" % (n/(1024*1024*1024))
    # M
    if n >= (1024*1024):
        return "%.1fM" % (n/(1024*1024))
    # K
    if n >= 1024:
        return "%.1fK" % (n/1024)
    return "%d" % n


def sanitize_app_name(app):
    """Sanitize the app name and build matching path"""
    return "".join(c for c in app if c.isalnum() or c in ('.', '_', '-')).rstrip().lstrip('/')


def exit_if_not_exists(app):
    """Utility function for error checking upon command startup."""
    app = sanitize_app_name(app)
    if not exists(join(APP_ROOT, app)):
        echo("ERROR: app '%s' not found." % app, fg='red')
        exit(1)


def get_free_port(address=""):
    """Find a free TCP port (entirely at random)"""

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((address, 0))
    port = s.getsockname()[1]
    s.close()
    return port



def setup_authorized_keys(ssh_fingerprint, script_path, pubkey):
    """Sets up an authorized_keys file to redirect SSH commands"""

    authorized_keys = join(environ['HOME'], '.ssh', 'authorized_keys')
    if not exists(dirname(authorized_keys)):
        makedirs(dirname(authorized_keys))
    # Restrict features and force all SSH commands to go through our script
    with open(authorized_keys, 'a') as h:
        h.write(
            """command="FINGERPRINT={ssh_fingerprint:s} NAME=default {script_path:s} $SSH_ORIGINAL_COMMAND",no-agent-forwarding,no-user-rc,no-X11-forwarding,no-port-forwarding {pubkey:s}\n""".format(**locals()))
    chmod(dirname(authorized_keys), S_IRUSR | S_IWUSR | S_IXUSR)
    chmod(authorized_keys, S_IRUSR | S_IWUSR)


def install_acme_sh():
    """ Install acme.sh for letsencrypt """
    if exists(ACME_ROOT):
        return
    echo("......-> Installing acme.sh", fg="green")
    call("curl https://raw.githubusercontent.com/Neilpang/acme.sh/master/acme.sh | INSTALLONLINE=1  sh", cwd=DAKA_ROOT, shell=True)


def _get_env(app):
    env_file = join(SETTINGS_ROOT, app, "ENV")
    if not exists(env_file):
        with open(env_file, 'w') as f:
            f.write('')
    config = configparser.ConfigParser() 
    config.optionxform = str              
    config.read(env_file)
    return config

def read_settings(app, section):
    data = json.loads(json.dumps(_get_env(app)._sections.get(section)))
    return {} if not data else data

def write_settings(app, section, data):
    env_file = join(SETTINGS_ROOT, app, "ENV")
    env = _get_env(app)
    if section not in env:
        env.add_section(section)
    [env.set(section, k.upper(), str(v)) for k,v in data.items()]
    env.write(open(env_file, "w"))


def expandvars(buffer, env, default=None, skip_escaped=False):
    """expand shell-style environment variables in a buffer"""

    def replace_var(match):
        return env.get(match.group(2) or match.group(1), match.group(0) if default is None else default)

    pattern = (r'(?<!\\)' if skip_escaped else '') + r'\$(\w+|\{([^}]*)\})'
    return sub(pattern, replace_var, buffer)


def command_output(cmd):
    """executes a command and grabs its output, if any"""
    try:
        env = environ
        return str(check_output(cmd, stderr=STDOUT, env=env, shell=True))
    except:
        return ""


def parse_settings(filename, env={}):
    """Parses a settings file and returns a dict with environment variables"""
    if not exists(filename):
        return {}
    with open(filename, 'r') as settings:
        for line in settings:
            if '#' == line[0] or len(line.strip()) == 0:  # ignore comments and newlines
                continue
            try:
                k, v = map(lambda x: x.strip(), line.split("=", 1))
                env[k] = expandvars(v, env)
            except:
                echo("Error: malformed setting '{}', ignoring file.".format(line), fg='red')
                return {}
    return env

def get_config(app):
    """ Return the info from daka.json """
    config_file = join(APP_ROOT, app, "daka.json")
    with open(config_file) as f:
        config = json.load(f)["apps"]

        # multiple site can be deployed by having daka.json:apps as array
        # with each item containing a domain_name to match the app name 
        if isinstance(config, list):
            for c in config:
              if app == c["domain_name"]:
                  return c

            echo("ERROR: '%s' not found in daka.json. 'daka.json:apps' is an array but app name didn't match domain_name" % app, fg="red")
            exit(1)

        # single site
        else:
            return config
    return None

def get_app_workers(app):
    """ Returns the applications to run """
    return {k.lower(): v  for k,v in get_config(app).get('run', {}).items()}


def get_app_config(app):
    """ Turn config into ENV """
    env = {}
    config = get_config(app)

    # special keys
    for k in ["env", "scripts", "run"]:
        if k in config:
            del config[k]

    for k, v in config.items():
        if isinstance(v, dict):
            env.update({("%s_%s" % (k, vk)).upper(): vv for vk, vv in v.items()})
        else:
            env[k.upper()] = v

    # Remap keys
    mapper = {
        "SERVER_NAME": "NGINX_SERVER_NAME",
        "DOMAIN_NAME": "NGINX_SERVER_NAME",
        "STATIC_PATHS": "NGINX_STATIC_PATHS",
        "HTTPS_ONLY": "NGINX_HTTPS_ONLY",
        "THREADS": "UWSGI_THREADS",
        "GEVENT": "UWSGI_GEVENT",
        "ASYNCIO": "UWSGI_ASYNCIO"
    }
    for k, v in mapper.items():
        if k in env and v not in env:
            env[v] = env[k]
    return env

def get_app_env(app):
    return get_config(app).get("env", {})

def get_app_metrics(app):
    metrics_dir = join(METRICS_ROOT, app)
    met = {
        "avg": "core.avg_response_time",
        "rss": "rss_size",
        "vsz": "vsz_size",
        "tx":  "core.total_tx"
    }
    metrics = {}
    for fk, fv in met.items():
        f2 = join(metrics_dir, fv)
        if exists(f2):
            with open(f2) as f:
                v = f.read().strip().split("\n")
                metrics[fk] = human_size(int(v[0])) if len(v) > 1 else "-"
        else:
            metrics[fk] = "-"
    return metrics

def get_app_runtime(app):
    app_path = join(APP_ROOT, app)
    config = get_app_config(app)
    runtime = config.get("RUNTIME")

    if runtime and runtime.lower() in VALID_RUNTIME:
        return runtime.lower()
    if exists(join(app_path, 'requirements.txt')):
        return "python"
    elif exists(join(app_path, 'package.json')):
        return "node"
    return "static"

def run_app_scripts(app, script_type):
    cwd = join(APP_ROOT, app)
    config = get_config(app)
    runtime = get_app_runtime(app)

    if "scripts" in config and script_type in config["scripts"]:
        scripts = config["scripts"][script_type]
        env = get_app_env(app)
        echo("......-> Running scripts: [%s] ..." % script_type, fg="green")

        # In python environment, execute everything in the virtualenv
        if runtime == "python":
            venv = join(join(ENV_ROOT, app), 'bin', 'activate');
            scripts.insert(0, '. %s' % venv)
            scripts.append("deactivate")
            cmds = ("; ".join(scripts)).rstrip(";") + ";"
            scripts = [cmds]
  
        for cmd in scripts:
            call(cmd, cwd=cwd, env=env, shell=True)

def deploy_app(app, deltas={}, newrev=None, release=False):
    """Deploy an app by resetting the work directory"""

    app_path = join(APP_ROOT, app)
    env_path = join(ENV_ROOT, app)   
    log_path = join(LOG_ROOT, app)
    conf_path = join(SETTINGS_ROOT, app)
    # list of paths that must exist
    ensure_paths = [env_path, log_path, conf_path]
    
    env = {
        'GIT_WORK_DIR': app_path
    }

    if exists(app_path):
        echo("......-> Deploying app '{}'".format(app), fg='green')
        call('git fetch --quiet', cwd=app_path, env=env, shell=True)
        if newrev:
            call('git reset --hard {}'.format(newrev), cwd=app_path, env=env, shell=True)
        call('git submodule init', cwd=app_path, env=env, shell=True)
        call('git submodule update', cwd=app_path, env=env, shell=True)

        config = get_config(app)
        workers = get_app_workers(app)
    
        if not config:
            echo("ERROR: Invalid daka.json for app '%s'." % app, fg="red")
            exit(1)
        elif not workers:
            echo("ERROR: daka.json missing the 'daka.run' processes or 'daka.run' it is empty", fg="red")
            exit(1)
        else:
            # ensure path exist
            for p in ensure_paths:
                if not exists(p):
                    makedirs(p)            

            # Delete app metrics 
            delete_app_metrics(app)

            runtime = get_app_runtime(app)
            env2 = get_app_config(app)

            if not runtime:
                echo("......-> Could not detect runtime!", fg="red")
            else:
                echo("......-> [%s] app detected." % runtime.upper(), fg="green")

                # Sanity check
                if "web" in workers:
                    # domain name
                    if "NGINX_SERVER_NAME" not in env2:
                        echo("ERROR: Missing 'DOMAIN_NAME' when there is a 'web' application", fg="red")
                        exit(1)
                    if runtime == "static":
                        if not workers["web"].startswith("/"):
                            echo("ERROR: For static site the webroot must start with a '/' (slash), instead '%s' provided" % workers["web"], fg="red")
                            exit(1)                            
                    
                # Setup runtime
                # python
                if runtime == "python":
                    setup_python_runtime(app, deltas)
                # node
                elif runtime == "node":
                    setup_node_runtime(app, deltas)
                # static html/php, shell
                elif runtime in ["static", "shell"]:
                    setup_shell_runtime(app, deltas)

                # Run release script. Once on git push
                if release is True:
                    run_app_scripts(app, "release")

                run_app_scripts(app, "predeploy")
                spawn_app(app, deltas)
                run_app_scripts(app, "postdeploy")
    else:
        echo("Error: app '{}' not found.".format(app), fg='red')


def get_spawn_env(app):
    env = {}
    # base config from daka.json
    env.update(get_app_config(app))
    # Load environment variables shipped with repo (if any)
    env.update(get_app_env(app))
    # Override with custom settings (if any)
    env.update(read_settings(app, 'CUSTOM'))
    return env 

def setup_node_runtime(app, deltas={}):
    """Deploy a Node  application"""

    virtualenv_path = join(ENV_ROOT, app)
    node_path = join(ENV_ROOT, app, "node_modules")
    node_path_tmp = join(APP_ROOT, app, "node_modules")
    deps = join(APP_ROOT, app, 'package.json')

    first_time = False
    if not exists(node_path):
        echo("......-> Creating node_modules for '{}'".format(app), fg='green')
        makedirs(node_path)
        first_time = True

    env = {
        'VIRTUAL_ENV': virtualenv_path,
        'NODE_PATH': node_path,
        'NPM_CONFIG_PREFIX': abspath(join(node_path, "..")),
        "PATH": ':'.join([join(virtualenv_path, "bin"), join(node_path, ".bin"), environ['PATH']])
    }

    version = env.get("RUNTIME_VERSION")

    if version:
        node_binary = join(virtualenv_path, "bin", "node")
        installed = check_output("{} -v".format(node_binary), cwd=join(APP_ROOT, app), env=env,
                                 shell=True).decode("utf8").rstrip("\n") if exists(node_binary) else ""

        if not installed.endswith(version):
            started = glob(join(UWSGI_ENABLED, '{}*.ini'.format(app)))
            if installed and len(started):
                echo("Warning: Can't update node with app running. Stop the app & retry.", fg='yellow')
            else:
                echo("......-> Installing node version '{RUNTIME_VERSION:s}' using nodeenv".format(**env), fg='green')
                call("nodeenv --prebuilt --node={RUNTIME_VERSION:s} --clean-src --force {VIRTUAL_ENV:s}".format(
                    **env), cwd=virtualenv_path, env=env, shell=True)
        else:
            echo("......-> Node is installed at {}.".format(version))

    if exists(deps):
        if first_time or getmtime(deps) > getmtime(node_path):
            echo("......-> Running npm for '{}'".format(app), fg='green')
            symlink(node_path, node_path_tmp)
            call('npm install', cwd=join(APP_ROOT, app), env=env, shell=True)
            unlink(node_path_tmp)


def setup_python_runtime(app, deltas={}):
    """Deploy a Python application"""

    virtualenv_path = join(ENV_ROOT, app)
    requirements = join(APP_ROOT, app, 'requirements.txt')
    activation_script = join(virtualenv_path, 'bin', 'activate_this.py')
    config = get_app_config(app)
    version = int(config.get("RUNTIME_VERSION", "3"))

    first_time = False
    if not exists(activation_script):
        echo("......-> Creating virtualenv for '{}'".format(app), fg='green')
        if not exists(virtualenv_path):
            makedirs(virtualenv_path)
        call('virtualenv --python=python{version:d} {app:s}'.format(**locals()), cwd=ENV_ROOT, shell=True)
        first_time = True

    exec(open(activation_script).read(), dict(__file__=activation_script))

    if first_time or getmtime(requirements) > getmtime(virtualenv_path):
        echo("......-> Running pip for '{}'".format(app), fg='green')
        call('pip install -r {} --upgrade'.format(requirements), cwd=virtualenv_path, shell=True)


def setup_shell_runtime(app, deltas={}):
    pass


def spawn_app(app, deltas={}):
    """Create all workers for an app"""

    app_path = join(APP_ROOT, app)
    runtime = get_app_runtime(app)
    workers = get_app_workers(app)
    ordinals = defaultdict(lambda: 1)
    worker_count = {k: 1 for k in workers.keys()}
    virtualenv_path = join(ENV_ROOT, app)
    scaling = read_settings(app, 'SCALING')

    # Bootstrap environment
    env = {
        'APP': app,
        'LOG_ROOT': LOG_ROOT,
        'HOME': environ['HOME'],
        'USER': environ.get("USER"),
        'PATH': ':'.join([join(virtualenv_path, 'bin'), environ['PATH']]),
        'PWD': app_path,
        'VIRTUAL_ENV': virtualenv_path,
        'SSL_LETSENCRYPT': True,
        'HTTPS_ONLY': True,
        'AUTO_RESTART': False,
        'WSGI': True
    }

    safe_defaults = {
        'NGINX_IPV4_ADDRESS': '0.0.0.0',
        'NGINX_IPV6_ADDRESS': '[::]',
        'BIND_ADDRESS': '127.0.0.1',
    }

    # add node path if present
    node_path = join(virtualenv_path, "node_modules")
    if exists(node_path):
        env["NODE_PATH"] = node_path
        env["PATH"] = ':'.join([join(node_path, ".bin"), env['PATH']])

    # SPAWN Env
    env.update(get_spawn_env(app))

    if 'web' in workers:
        # Pick a port if none defined
        if 'PORT' not in env:
            env['PORT'] = str(get_free_port())
            echo("......-> picking free port %s" % env["PORT"])

        # Safe defaults for addressing
        for k, v in safe_defaults.items():
            if k not in env:
                echo("......-> nginx {k:s} set to {v}".format(**locals()))
                env[k] = v

        # Set up nginx if we have NGINX_SERVER_NAME set
        if 'NGINX_SERVER_NAME' in env:
            nginx = command_output("nginx -V")
            nginx_ssl = "443 ssl"
            if "--with-http_v2_module" in nginx:
                nginx_ssl += " http2"
            elif "--with-http_spdy_module" in nginx and "nginx/1.6.2" not in nginx:
                nginx_ssl += " spdy"
            nginx_conf = join(NGINX_ROOT, "%s.conf" % app)

            env.update({
                'NGINX_SSL': nginx_ssl,
                'NGINX_ROOT': NGINX_ROOT,
                'ACME_WWW': ACME_WWW,
            })

            env['INTERNAL_NGINX_UWSGI_SETTINGS'] = 'proxy_pass http://{BIND_ADDRESS:s}:{PORT:s};'.format(**env)
            env['NGINX_SOCKET'] = "{BIND_ADDRESS:s}:{PORT:s}".format(**env)
            echo("......-> nginx will look for app '{}' on {}".format(app, env['NGINX_SOCKET']))

            domain = env['NGINX_SERVER_NAME'].split()[0]
            key = join(NGINX_ROOT, "%s.%s" % (app, 'key'))
            crt = join(NGINX_ROOT, "%s.%s" % (app, 'crt'))

            # LETSENCRYPT
            if env.get("SSL_LETSENCRYPT") is True and exists(join(ACME_ROOT, "acme.sh")):
                acme = ACME_ROOT
                www = ACME_WWW
                # if this is the first run there will be no nginx conf yet
                # create a basic conf stub just to serve the acme auth
                if not exists(nginx_conf):
                    echo("......-> writing temporary nginx conf")
                    buffer = expandvars(NGINX_ACME_FIRSTRUN_TEMPLATE, env)
                    with open(nginx_conf, "w") as h:
                        h.write(buffer)
                if not exists(key) or not exists(join(ACME_ROOT, domain, domain + ".key")):
                    echo("......-> getting letsencrypt certificate")
                    call('{acme:s}/acme.sh --issue -d {domain:s} -w {www:s}'.format(**locals()), shell=True)
                    call('{acme:s}/acme.sh --install-cert -d {domain:s} --key-file {key:s} --fullchain-file {crt:s}'.format(**locals()), shell=True)
                    if exists(join(ACME_ROOT, domain)) and not exists(join(ACME_WWW, app)):
                        symlink(join(ACME_ROOT, domain), join(ACME_WWW, app))
                else:
                    echo("......-> letsencrypt certificate already installed")

            # fall back to creating self-signed certificate if acme failed
            if not exists(key) or stat(crt).st_size == 0:
                echo("......-> generating self-signed certificate")
                call('openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -subj "/C=US/ST=NY/L=New York/O=Daka/OU=Self-Signed/CN={domain:s}" -keyout {key:s} -out {crt:s}'.format(
                    **locals()), shell=True)

            # restrict access to server from CloudFlare IP addresses
            acl = []
            if env.get('NGINX_CLOUDFLARE_ACL', 'false').lower() == 'true':
                try:
                    cf = json.loads(urlopen('https://api.cloudflare.com/client/v4/ips').read().decode("utf-8"))
                    if cf['success'] == True:
                        for i in cf['result']['ipv4_cidrs']:
                            acl.append("allow {};".format(i))
                        for i in cf['result']['ipv6_cidrs']:
                            acl.append("allow {};".format(i))
                        # allow access from controlling machine
                        if 'SSH_CLIENT' in environ:
                            remote_ip = environ['SSH_CLIENT'].split()[0]
                            echo("......-> Adding your IP ({}) to nginx ACL".format(remote_ip))
                            acl.append("allow {};".format(remote_ip))
                        acl.extend(["allow 127.0.0.1;", "deny all;"])
                except:
                    cf = defaultdict()
                    echo("......-> Could not retrieve CloudFlare IP ranges: {}".format(format_exc()), fg="red")

            env['NGINX_ACL'] = " ".join(acl)

            env['INTERNAL_NGINX_STATIC_MAPPINGS'] = ''
            env['INTERNAL_NGINX_STATIC_CLAUSES'] = ''

            # static requires just the path. It will set the url as web root
            if runtime == 'static':
                static_path = workers['web'].strip("/").rstrip("/")
                html_root = join(app_path, static_path)
                env['INTERNAL_NGINX_STATIC_CLAUSES'] = expandvars(INTERNAL_NGINX_STATIC_CLAUSES, locals())

            # Get a mapping of [/url1:path1, /url2:path2, ...] ...
            static_paths = env.get('NGINX_STATIC_PATHS', [])
            if not isinstance(static_paths, list):
                static_paths = []

            if len(static_paths):
                try:
                    for item in static_paths:
                        static_url, static_path = item.split(':', 2)
                        if static_path[0] != '/':
                            static_path = join(app_path, static_path)
                        env['INTERNAL_NGINX_STATIC_MAPPINGS'] = env['INTERNAL_NGINX_STATIC_MAPPINGS'] + \
                            expandvars(INTERNAL_NGINX_STATIC_MAPPING, locals())
                except Exception as e:
                    echo(
                        "Error {} in static_paths spec: should be a list [/url1:path1, /url2:path2, ...], ignoring.".format(e), fg="red")
                    env['INTERNAL_NGINX_STATIC_MAPPINGS'] = ''

            env['INTERNAL_NGINX_CUSTOM_CLAUSES'] = expandvars(
                open(join(app_path, env["NGINX_INCLUDE_FILE"])).read(), env) if env.get("NGINX_INCLUDE_FILE") else ""
            env['INTERNAL_NGINX_PORTMAP'] = ""

            if "static" not in runtime:
                env['INTERNAL_NGINX_PORTMAP'] = expandvars(NGINX_PORTMAP_FRAGMENT, env)
            env['INTERNAL_NGINX_COMMON'] = expandvars(NGINX_COMMON_FRAGMENT, env)

            echo("......-> nginx will map app '{}' to hostname '{}'".format(app, env['NGINX_SERVER_NAME']))
            
            if env.get('HTTPS_ONLY') is True:
                buffer = expandvars(NGINX_HTTPS_ONLY_TEMPLATE, env)
                echo("......-> nginx will redirect all requests to hostname '{}' to HTTPS".format(env['NGINX_SERVER_NAME']))
            else:
                buffer = expandvars(NGINX_TEMPLATE, env)

            with open(nginx_conf, "w") as h:
                h.write(buffer)
            # prevent broken config from breaking other deploys
            try:
                nginx_config_test = str(check_output("nginx -t 2>&1 | grep {}".format(app), env=environ, shell=True))
            except:
                nginx_config_test = None
            if nginx_config_test:
                echo("Error: [nginx config] {}".format(nginx_config_test), fg='red')
                echo("Warning: removing broken nginx config.", fg='yellow')
                unlink(nginx_conf)

    # Configured worker count
    if scaling:
        worker_count.update({k.lower(): int(v) for k, v in scaling.items() if k.lower() in workers})

    to_create = {}
    to_destroy = {}
    for k, v in worker_count.items():
        to_create[k] = range(1, worker_count[k] + 1)
        if k in deltas and deltas[k]:
            to_create[k] = range(1, worker_count[k] + deltas[k] + 1)
            if deltas[k] < 0:
                to_destroy[k] = range(worker_count[k], worker_count[k] + deltas[k], -1)
            worker_count[k] = worker_count[k]+deltas[k]

    # Cleanup env
    for k, v in list(env.items()):
        if k.startswith('INTERNAL_'):
            del env[k]

    # Save current settings
    write_settings(app, 'ENV', env)
    write_settings(app, 'SCALING', worker_count)

    # auto restart
    if env.get("AUTO_RESTART", False) is True:
        echo("......-> auto-restart triggered", fg="green")
        cleanup_uwsgi_enabled_ini(app)

    # Create new workers
    for k, v in to_create.items():
        for w in v:
            enabled = join(UWSGI_ENABLED, '{app:s}___{k:s}.{w:d}.ini'.format(**locals()))
            if not exists(enabled):
                echo("......-> spawning '{app:s}:{k:s}.{w:d}'".format(**locals()), fg='green')
                spawn_worker(app, k, workers[k], env, w)

    # Remove unnecessary workers (leave logfiles)
    for k, v in to_destroy.items():
        for w in v:
            enabled = join(UWSGI_ENABLED, '{app:s}___{k:s}.{w:d}.ini'.format(**locals()))
            if exists(enabled):
                echo("......-> terminating '{app:s}:{k:s}.{w:d}'".format(**locals()), fg='yellow')
                unlink(enabled)

    return env


def spawn_worker(app, kind, command, env, ordinal=1):
    """Set up and deploy a single worker of a given kind"""

    app_kind = kind
    runtime = get_app_runtime(app)
    workers = get_app_workers(app)
    config = get_app_config(app)

    if app_kind == "web":
        app_kind = runtime
        if runtime == "python":
            app_kind = "wsgi" if config.get("WSGI", True) is True else "shell"
        elif runtime == "node":
            app_kind = "shell"

    env['PROC_TYPE'] = app_kind
    env_path = join(ENV_ROOT, app)
    metrics_path = join(METRICS_ROOT, app)
    available = join(UWSGI_AVAILABLE, '{app:s}___{kind:s}.{ordinal:d}.ini'.format(**locals()))
    enabled = join(UWSGI_ENABLED, '{app:s}___{kind:s}.{ordinal:d}.ini'.format(**locals()))
    log_file = join(LOG_ROOT, app, kind)

    # Create metrics dir
    if not exists(metrics_path):
        makedirs(metrics_path)

    settings = [
        ('chdir',               join(APP_ROOT, app)),
        ('master',              'true'),
        ('project',             app),
        ('max-requests',        env.get('UWSGI_MAX_REQUESTS', '1024')),
        ('listen',              env.get('UWSGI_LISTEN', '16')),
        ('processes',           env.get('UWSGI_PROCESSES', '1')),
        ('procname-prefix',     '{app:s}:{kind:s}'.format(**locals())),
        ('enable-threads',      env.get('UWSGI_ENABLE_THREADS', 'true').lower()),
        ('log-x-forwarded-for', env.get('UWSGI_LOG_X_FORWARDED_FOR', 'false').lower()),
        ('log-maxsize',         env.get('UWSGI_LOG_MAXSIZE', UWSGI_LOG_MAXSIZE)),
        ('logto',               '{log_file:s}.{ordinal:d}.log'.format(**locals())),
        ('log-backupname',      '{log_file:s}.{ordinal:d}.log.old'.format(**locals())),
        ('metrics-dir',         metrics_path),
    ]

    http = '{BIND_ADDRESS:s}:{PORT:s}'.format(**env)

    # only add virtualenv to uwsgi if it's a real virtualenv
    if exists(join(env_path, "bin", "activate_this.py")):
        settings.append(('virtualenv', env_path))

    # for Python only
    if app_kind == 'wsgi':
        python_version = int(env.get('RUNTIME_VERSION', '3'))
        settings.extend([('module', command), ('threads', env.get('UWSGI_THREADS', '4'))])
        if python_version == 2:
            settings.extend([('plugin', 'python')])
            if 'UWSGI_GEVENT' in env:
                settings.extend([('plugin', 'gevent_python'), ('gevent', env['UWSGI_GEVENT'])])
            elif 'UWSGI_ASYNCIO' in env:
                settings.extend([('plugin', 'asyncio_python')])
        elif python_version == 3:
            settings.extend([('plugin', 'python3'), ])
            if 'UWSGI_ASYNCIO' in env:
                settings.extend([('plugin', 'asyncio_python3'), ])

        echo("......-> nginx will talk to uWSGI via %s" % http, fg='yellow')
        settings.extend([('http', http), ('http-socket', http)])

    # shell
    elif app_kind == 'shell':
        echo("......-> nginx will talk to the web process via %s" % http, fg='yellow')
        settings.append(('attach-daemon', command))

    elif app_kind == 'static':
        echo("......-> nginx will serve static HTML/PHP files only".format(**env), fg='yellow')
        
    else:
        settings.append(('attach-daemon', command))

    if app_kind in ['wsgi', 'shell']:
        settings.append(
            ('log-format', '%%(addr) - %%(user) [%%(ltime)] "%%(method) %%(uri) %%(proto)" %%(status) %%(size) "%%(referer)" "%%(uagent)" %%(msecs)ms'))

    # remove unnecessary variables from the env in nginx.ini
    for k in ['NGINX_ACL']:
        if k in env:
            del env[k]

    # insert user defined uwsgi settings if set
    settings += parse_settings(join(APP_ROOT, app, env.get("UWSGI_INCLUDE_FILE"))).items() if env.get("UWSGI_INCLUDE_FILE") else []

    for k, v in env.items():
        settings.append(('env', '{k:s}={v}'.format(**locals())))

    if kind != 'static':
        with open(available, 'w') as h:
            h.write('[uwsgi]\n')
            for k, v in settings:
                h.write("{k:s} = {v}\n".format(**locals()))
        copyfile(available, enabled)


def cleanup_uwsgi_enabled_ini(app):
    config = glob(join(UWSGI_ENABLED, '{}*.ini'.format(app)))
    if len(config):
        for c in config:
            remove(c)
        return True


def remove_nginx_conf(app):
    nginx_conf = join(NGINX_ROOT, "%s.conf" % app)
    if exists(nginx_conf):
        remove(nginx_conf)


def multi_tail(app, filenames, catch_up=20):
    """Tails multiple log files"""

    # Seek helper
    def peek(handle):
        where = handle.tell()
        line = handle.readline()
        if not line:
            handle.seek(where)
            return None
        return line

    inodes = {}
    files = {}
    prefixes = {}

    # Set up current state for each log file
    for f in filenames:
        prefixes[f] = splitext(basename(f))[0]
        files[f] = open(f)
        inodes[f] = stat(f).st_ino
        files[f].seek(0, 2)

    longest = max(map(len, prefixes.values()))

    # Grab a little history (if any)
    for f in filenames:
        for line in deque(open(f), catch_up):
            yield "{} | {}".format(prefixes[f].ljust(longest), line)

    while True:
        updated = False
        # Check for updates on every file
        for f in filenames:
            line = peek(files[f])
            if not line:
                continue
            else:
                updated = True
                yield "{} | {}".format(prefixes[f].ljust(longest), line)

        if not updated:
            sleep(1)
            # Check if logs rotated
            for f in filenames:
                if exists(f):
                    if stat(f).st_ino != inodes[f]:
                        files[f] = open(f)
                        inodes[f] = stat(f).st_ino
                else:
                    filenames.remove(f)

def delete_app_metrics(app):
    metrics_dir = join(METRICS_ROOT, app)
    if exists(metrics_dir):
        rmtree(metrics_dir)
    if not exists(metrics_dir):
        makedirs(metrics_dir)

# === CLI commands ===

@click.group()
def cli():
    """ Daka - A very small PaaS to do git push deployments. 

    https://github.com/mardix/daka/ """
    pass


# --- User commands ---

@cli.command("apps")
def list_apps():
    """List all apps"""
    print_title("All apps")
    enabled = {a.split("___")[0] for a in listdir(UWSGI_ENABLED) if "___" in a}
    data = [["App Name", "Domain Name", "Runtime", "Running", "Web", "Port", "SSL", "Workers", "AVG", "RSS", "VSZ", "TX"]]
    for app in listdir(APP_ROOT):
        if not app.startswith((".", "_")):
            runtime = get_app_runtime(app)
            workers = get_app_workers(app)
            metrics = get_app_metrics(app)
            settings = read_settings(app, 'ENV')

            nginx_file = join(NGINX_ROOT, "%s.conf" % app)
            running = False
            port = settings.get("PORT", "-")
            domain_name = settings.get('DOMAIN_NAME', '-')
            ssl = "Y" if settings.get("SSL_LETSENCRYPT") is True else "-"
            
            avg = metrics.get("avg", "-")
            rss = metrics.get("rss", "-")
            vsz = metrics.get("vsz", "-")
            tx = metrics.get("tx", "-")

            workers_len = len(workers.keys()) if workers else 0 
            web_len = "-" 
            if "web" in workers:
                web_len = "Y"
                workers_len = workers_len - 1
            if runtime == "static":
                if exists(nginx_file):
                    running = True
            else:
                running = app in enabled
            status = "Y" if running else "-"

            data.append([app, domain_name, runtime, status, web_len, port, ssl, workers_len, avg, rss, vsz, tx])
    print_table(data)

@cli.command("set")
@click.argument('app')
@click.argument('settings', nargs=-1)
def cmd_config_set(app, settings):
    """Set ENV config: [<app> [{KEY1}={VAL1}, ...]]"""

    echo("Update config for %s" % app, fg="green")
    exit_if_not_exists(app)
    app = sanitize_app_name(app)
    env = read_settings(app, 'CUSTOM')
    for s in settings:
        try:
            k, v = map(lambda x: x.strip(), s.split("=", 1))
            env[k] = v
            echo("......-> set {k:s}={v} for '{app:s}'".format(**locals()), fg='white')
        except:
            echo("Error: malformed setting '{}'".format(s), fg='red')
            return
    write_settings(app, 'CUSTOM', env)
    deploy_app(app)


@cli.command("del")
@click.argument('app')
@click.argument('settings', nargs=-1)
def cmd_config_unset(app, settings):
    """Delete ENV config: [<app> {KEY}] """

    echo("Update config for %s" % app, fg="green")
    exit_if_not_exists(app)
    app = sanitize_app_name(app)
    env = read_settings(app, 'CUSTOM')
    for s in settings:
        if s in env:
            del env[s]
            echo("......-> unset {} for '{}'".format(s, app), fg='white')
    write_settings(app, 'CUSTOM', env)
    deploy_app(app)


@cli.command("env")
@click.argument('app')
def cmd_config_live(app):
    """Show ENV config: [<app>] """
    print_title("Env Config", app=app)
    exit_if_not_exists(app)
    app = sanitize_app_name(app)
    env_file = join(SETTINGS_ROOT, app, 'ENV')

    if exists(env_file):
        echo("")      
        echo(open(env_file).read().strip(), fg='white') 

@cli.command("deploy")
@click.argument('app')
def cmd_deploy(app):
    """Deploy app: [<app>]"""
    echo("Deploy app", fg="green")
    exit_if_not_exists(app)
    app = sanitize_app_name(app)
    deploy_app(app)


@cli.command("destroy")
@click.argument('app')
def cmd_destroy(app):
    """Delete app: [<app>]"""
    echo("**** WARNING ****", fg="red")
    echo("**** YOU ARE ABOUT TO DESTROY AN APP ****", fg="red")

    exit_if_not_exists(app)
    app = sanitize_app_name(app)

    if not click.confirm("Do you want to destroy this app? It will delete everything"):
        exit(1)
    if not click.confirm("Are you really sure?"):
        exit(1)

    # on destroy
    run_app_scripts(app, "destroy")

    for p in [join(x, app) for x in [APP_ROOT, GIT_ROOT, ENV_ROOT, SETTINGS_ROOT, 
                                        LOG_ROOT, METRICS_ROOT]]:
        if exists(p):
            echo("Removing folder '{}'".format(p), fg='yellow')
            rmtree(p)

    for p in [join(x, '{}*.ini'.format(app)) for x in [UWSGI_AVAILABLE, UWSGI_ENABLED]]:
        g = glob(p)
        if len(g):
            for f in g:
                echo("Removing file '{}'".format(f), fg='yellow')
                remove(f)

    nginx_files = [join(NGINX_ROOT, "{}.{}".format(app, x)) for x in ['conf', 'sock', 'key', 'crt']]
    for f in nginx_files:
        if exists(f):
            echo("Removing file '{}'".format(f), fg='yellow')
            remove(f)

    acme_link = join(ACME_WWW, app)
    acme_certs = realpath(acme_link)
    if exists(acme_certs):
        echo("Removing folder '{}'".format(acme_certs), fg='yellow')
        rmtree(acme_certs)
        echo("Removing file '{}'".format(acme_link), fg='yellow')
        unlink(acme_link)


@cli.command("log")
@click.argument('app')
def cmd_logs(app):
    """Read tail logs [<app>]"""

    exit_if_not_exists(app)
    app = sanitize_app_name(app)
    logfiles = glob(join(LOG_ROOT, app, '*.log'))
    if len(logfiles):
        for line in multi_tail(app, logfiles):
            echo(line.strip(), fg='white')
    else:
        echo("No logs found for app '{}'.".format(app), fg='yellow')


@cli.command("ps")
@click.argument('app')
def cmd_ps(app):
    """Show process count: [<app>]"""

    print_title("Process", app=app)
    exit_if_not_exists(app)
    app = sanitize_app_name(app)
    env = read_settings(app, 'SCALING')
    if env:
        data = [[k, v] for k, v in env.items()]
        data.insert(0, ["Process", "Size"])
        print_table(data)    
    else:
        echo("Error: no workers found for app '%s'." % app, fg='red')


@cli.command("scale")
@click.argument('app')
@click.argument('settings', nargs=-1)
def cmd_ps_scale(app, settings):
    """Scale processes: [<app> [<proc>=<count>, ...]]"""

    exit_if_not_exists(app)
    app = sanitize_app_name(app)
    env = read_settings(app, 'SCALING')
    worker_count = {k.lower(): int(v) for k, v in env.items()}
    deltas = {}
    for s in settings:
        try:
            k, v = map(lambda x: x.strip(), s.split("=", 1))
            c = int(v)
            if c < 0:
                echo("Error: cannot scale type '{}' below 0".format(k), fg='red')
                return
            if k not in worker_count:
                echo("Error: worker type '{}' not present in '{}'".format(k, app), fg='red')
                return
            deltas[k] = c - worker_count[k]
        except:
            echo("Error: malformed setting '{}'".format(s), fg='red')
            return
    deploy_app(app, deltas)


@cli.command("reload")
@click.argument('app')
def cmd_reload(app):
    """Reload app: [<app>]"""
    echo("Reloading app", fg="green")
    exit_if_not_exists(app)
    app = sanitize_app_name(app)
    remove_nginx_conf(app)
    cleanup_uwsgi_enabled_ini(app)
    echo("......-> reloading '{}'...".format(app), fg='yellow')
    spawn_app(app)


@cli.command("reload-all")
def cmd_reload_all():
    """Reload all apps"""
    echo("Reloading all apps", fg="green")
    for app in listdir(APP_ROOT):
        if not app.startswith((".", "_")):
            app = sanitize_app_name(app)
            remove_nginx_conf(app)
            cleanup_uwsgi_enabled_ini(app)
            echo("...-> reloading '{}'...".format(app), fg='yellow')
            spawn_app(app)

@cli.command("stop")
@click.argument('app')
def cmd_stop(app):
    """Stop app: [<app>]"""
    echo("Stopping app", fg="green")
    exit_if_not_exists(app)
    app = sanitize_app_name(app)
    remove_nginx_conf(app)
    cleanup_uwsgi_enabled_ini(app)
    echo("......-> '%s' stopped" % app, fg='yellow')

@cli.command("stop-all")
def cmd_stop_all():
    """Stop all apps"""
    echo("Stopping all apps", fg="green")
    for app in listdir(APP_ROOT):
        if not app.startswith((".", "_")):
            app = sanitize_app_name(app)
            remove_nginx_conf(app)
            cleanup_uwsgi_enabled_ini(app)
            echo("......-> '%s' stopped" % app, fg='yellow')


@cli.command("set-ssh")
@click.argument('public_key_file')
def cmd_setup_ssh(public_key_file):
    """Set up a new SSH key (use - for stdin)"""

    def add_helper(key_file):
        if exists(key_file):
            try:
                fingerprint = str(check_output('ssh-keygen -lf ' + key_file, shell=True)).split(' ', 4)[1]
                key = open(key_file, 'r').read().strip()
                echo("Adding key '{}'.".format(fingerprint), fg='white')
                setup_authorized_keys(fingerprint, DAKA_SCRIPT, key)
            except Exception:
                echo("Error: invalid public key file '{}': {}".format(key_file, format_exc()), fg='red')
        elif '-' == public_key_file:
            buffer = "".join(stdin.readlines())
            with NamedTemporaryFile(mode="w") as f:
                f.write(buffer)
                f.flush()
                add_helper(f.name)
        else:
            echo("Error: public key file '{}' not found.".format(key_file), fg='red')

    add_helper(public_key_file)


@cli.command("version")
def cmd_version():
    """ Get Version """
    echo("%s v.%s" % (NAME, VERSION), fg="green")


@cli.command("update")
def cmd_update():
    """ Update Daka to the latest from Github """
    print_title("Updating")
    url = "https://raw.githubusercontent.com/mardix/daka/master/daka.py"
    echo("...downloading 'daka.py' from github")
    unlink(DAKA_SCRIPT)
    urllib.request.urlretrieve(url, DAKA_SCRIPT)
    chmod(DAKA_SCRIPT, stat(DAKA_SCRIPT).st_mode | S_IXUSR)
    echo("...update completed!", fg="green")

@cli.command("ssl-download")
@click.argument('app')
def cmd_ssl_download(app):
    """Downloading SSL CERT & KEY"""
    print_title("Download SSL Key & Cert")
    echo("Copy and paste ", fg="green")
    exit_if_not_exists(app)
    app = sanitize_app_name(app)
    key = join(NGINX_ROOT, "%s.%s" % (app, 'key'))
    crt = join(NGINX_ROOT, "%s.%s" % (app, 'crt')) 
    echo("") 
    echo("SSL CRT:")  
    call('cat %s' % crt, shell=True)
    echo("-" * 80)
    echo("SSL KEY:")
    call('cat %s' % key, shell=True)
    echo("") 


# ssl:upload-key
# ssl:upload-crt
def cmd_x(): pass

# --- Internal commands ---


def cmd_init():
    """Initialize Daka for 1st time"""

    print_title()
    echo("......-> running in Python {}".format(".".join(map(str, version_info))))

    # Create required paths
    for p in [APP_ROOT, GIT_ROOT, ACME_WWW, ENV_ROOT, UWSGI_ROOT, 
                UWSGI_AVAILABLE, UWSGI_ENABLED, LOG_ROOT, 
                SETTINGS_ROOT, NGINX_ROOT, METRICS_ROOT]:
        if not exists(p):
            echo("Creating '{}'.".format(p), fg='green')
            makedirs(p)

    # Set up the uWSGI emperor config
    settings = [
        ('chdir',           UWSGI_ROOT),
        ('emperor',         UWSGI_ENABLED),
        ('log-maxsize',     UWSGI_LOG_MAXSIZE),
        ('logto',           join(UWSGI_ROOT, 'uwsgi.log')),
        ('log-backupname',  join(UWSGI_ROOT, 'uwsgi.old.log')),
        ('socket',          join(UWSGI_ROOT, 'uwsgi.sock')),
        ('uid',             getpwuid(getuid()).pw_name),
        ('gid',             getgrgid(getgid()).gr_name),
        ('enable-threads',  'true'),
        ('threads',         '{}'.format(cpu_count() * 2)),
    ]
    with open(join(UWSGI_ROOT, 'uwsgi.ini'), 'w') as h:
        h.write('[uwsgi]\n')
        for k, v in settings:
            h.write("{k:s} = {v}\n".format(**locals()))

    # mark this script as executable (in case we were invoked via interpreter)
    if not(stat(DAKA_SCRIPT).st_mode & S_IXUSR):
        echo("Setting '{}' as executable.".format(DAKA_SCRIPT), fg='yellow')
        chmod(DAKA_SCRIPT, stat(DAKA_SCRIPT).st_mode | S_IXUSR)

    # ACME
    install_acme_sh()



def cmd_git_hook(app):
    """INTERNAL: Post-receive git hook"""

    app = sanitize_app_name(app)
    repo_path = join(GIT_ROOT, app)
    app_path = join(APP_ROOT, app)

    for line in stdin:
        oldrev, newrev, refname = line.strip().split(" ")
        if not exists(app_path):
            echo("......-> Creating app '{}'".format(app), fg='green')
            makedirs(app_path)
            call('git clone --quiet {} {}'.format(repo_path, app), cwd=APP_ROOT, shell=True)

        deploy_app(app, newrev=newrev, release=True)


def cmd_git_receive_pack(app):
    """INTERNAL: Handle git pushes for an app"""

    app = sanitize_app_name(app)
    app_dir = join(GIT_ROOT, app)
    hook_path = join(app_dir, 'hooks', 'post-receive')
    env = globals()
    env.update(locals())

    if not exists(hook_path):
        makedirs(app_dir)
        # Initialize the repository with a hook to this script
        call("git init --quiet --bare " + app, cwd=GIT_ROOT, shell=True)
        with open(hook_path, 'w') as h:
            h.write("""#!/usr/bin/env bash
set -e; set -o pipefail;
cat | DAKA_ROOT="{DAKA_ROOT:s}" {DAKA_SCRIPT:s} git-hook {app:s}""".format(**env))
        # Make the hook executable by our user
        chmod(hook_path, stat(hook_path).st_mode | S_IXUSR)

    call('git-shell -c "{}" '.format(argv[1] + " '{}'".format(app)), cwd=GIT_ROOT, shell=True)


def cmd_upload_pack(app):
    """INTERNAL: Handle git upload pack for an app"""
    app = sanitize_app_name(app)
    env = globals()
    env.update(locals())
    # Handle the actual receive. Will be called with 'git-hook' after it happens
    call('git-shell -c "{}" '.format(argv[1] + " '{}'".format(app)), cwd=GIT_ROOT, shell=True)


def main():
    _argvs = sys.argv
    script_name = sys.argv[0].split('/')[-1]

    # Internal GIT command
    if _argvs and len(_argvs) >= 2 and _argvs[1] in ["init", "git-hook", "git-upload-pack", "git-receive-pack"]:
        cmd = sys.argv[1]

        if cmd == "init":
            cmd_init()
        elif len(_argvs) >= 3:
            app = sys.argv[2]
            if cmd == "git-hook":
                cmd_git_hook(app)
            elif cmd == "git-upload-pack":
                cmd_git_upload_pack(app)
            elif cmd == "git-receive-pack":
                cmd_git_receive_pack(app)
    else:
        cli()


if __name__ == "__main__":
    main()
