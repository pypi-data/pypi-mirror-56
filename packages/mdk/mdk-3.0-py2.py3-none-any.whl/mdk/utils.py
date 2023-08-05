"""mdk utility functions & classes"""
import functools
import json
import os
from pathlib import Path
import subprocess
from typing import Any, Dict, List, TypeVar, Union
import sys
from click import echo, style

CONFIG_FILENAME: str = "mdk.json"
ReturnCode = int
T = TypeVar('T')


def require_active_container(func):
    @functools.wraps(func)
    def _active_container(self, *args, **kwargs):
        container_name = self.conf_req("name")
        if self(["container", "inspect", container_name], io=False, log=False) != 0:
            Log.warning(f"{container_name} is not active (command not executed)")
            sys.exit(1)
        return func(self, *args, **kwargs)
    return _active_container


def forbid_active_container(func):
    @functools.wraps(func)
    def _active_container(self, *args, **kwargs):
        container_name = self.conf_req("name")
        if self(["container", "inspect", container_name], io=False, log=False) != 0:
            return func(self, *args, **kwargs)
        Log.warning(f"{container_name} is already active (command not executed)")
        sys.exit(1)
    return _active_container


class DockerCommand():
    def __call__(self, args: List, io=True, log=True) -> ReturnCode:
        cmd = ["docker"] + args
        if log:
            Log.cmd(cmd)
        if io:
            return subprocess.call(cmd)
        return subprocess.call(
            cmd,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL)

    def __init__(self) -> None:
        # find nearest config file to cwd
        self.conf_path = None
        for dir_path in (Path().cwd()/"_").parents:
            if (dir_path/CONFIG_FILENAME).is_file():
                self.conf_path = dir_path/CONFIG_FILENAME
                break

        if self.conf_path is None:
            self.conf_data: Dict[str, Any] = {}
            return

        self.conf_data = json.load(open(self.conf_path))

    def cli_opts(self) -> List[str]:
        opt_builder: List[str] = []
        volumes = self.conf("volumes")
        if volumes is not None:
            for volume in volumes:
                vol_builder = volume
                if vol_builder.startswith('.'):
                    vol_builder = str(self.conf_path.parent) + vol_builder.lstrip('.')
                opt_builder += ["-v", vol_builder]

        if self.conf("shareX11") is True:
            opt_builder += ["-v", "/tmp/.X11-unix:/tmp/.X11-unix", "-e", f"DISPLAY={os.getenv('DISPLAY')}"]

        environment = self.conf("environment")
        if environment is not None:
            for env_var in environment:
                env_pair = env_var.split('=')
                if len(env_pair) != 2:
                    continue
                if env_pair[1].startswith('$'):
                    env_name = env_pair[1].lstrip('$')
                    if env_name == "UID":
                        env_pair[1] = str(os.getuid())
                    elif env_name == "GID":
                        env_pair[1] = str(os.getgid())
                    else:
                        env_pair[1] = os.getenv(env_pair[1].lstrip('$'))
                if env_pair[1] is not None:
                    opt_builder += ["-e", '='.join(env_pair)]

        if self.conf("core-image") is True:
            opt_builder += ["-e", f"HOST_UID={os.getuid()}", "-e", f"DOCKER_CONTAINER_NAME={self.conf('name')}", "-e",
                            f"DOCKER_CONTAINER_ROOT=~/{Path.cwd().relative_to(Path.home())}"]

        if self.conf('workdir') is not None:
            opt_builder += ["-w", self.conf('workdir')]

        extra_opts = self.conf("options")
        if extra_opts is not None:
            opt_builder += extra_opts

        return opt_builder

    @require_active_container
    def container_cmd(self, command: str) -> ReturnCode:
        contianer_name = self.conf_req("name")
        code = self([command, contianer_name], io=False)
        if code == 0:
            Log.success(f"{command} -> {contianer_name}")
        else:
            Log.error(f"{command} -> {contianer_name}", f"error code {code}")
        return code

    def conf(self, key: str) -> Union[T, None]:
        if self.conf_path is None:
            return None
        return self.conf_data.get(key, None)

    def conf_req(self, key: str) -> str:
        if self.conf_path is None:
            Log.error(f"finding config", f"{CONFIG_FILENAME} does not exist in current directory or its parents")
            sys.exit(1)
        val = self.conf(key)
        if val is None:
            Log.error(f"loading config", f"\"{key}\" not assigned in {self.conf_path}")
            sys.exit(1)
        return val

    def output(self, args):
        return subprocess.getoutput("docker " + " ".join(args))

    @require_active_container
    def down(self) -> ReturnCode:
        container_name = self.conf_req("name")
        self(["stop", container_name], io=False)
        code = self(["rm", container_name], io=False)
        if code == 0:
            Log.success(f"stopped and removed {container_name}")
        else:
            Log.error(f"bringing {container_name} down", f"error code {code}")
        return code

    @require_active_container
    def exec(self, exec_cmd: List[str], interactive=True) -> ReturnCode:
        cmd = ["exec", self.conf_req("name")]
        if interactive:
            cmd.insert(1, "-it")
        return self(cmd + exec_cmd)

    def run(self, run_cmd: List[str], interactive=True) -> ReturnCode:
        cmd = ["run", self.conf_req("image")]
        if interactive:
            cmd.insert(1, "-it")
        return self(cmd + run_cmd)

    def status(self):
        container_name = self.conf_req('name')
        container_exists = self(["container", "inspect", container_name], io=False, log=False) == 0

        Log.log("Container:")
        Log.log("  {:12}{}".format("Name", container_name))

        if container_exists:
            status_fields = ["Image", "ID", "Status", "Command", "Size"]
            docker_output = self.output([
                "ps", "-a",
                "--format", "{{." + "}},{{.".join(status_fields) + "}}",
                "--filter", f"name={container_name}",
            ]).strip(" \n")
            status_results = docker_output.split(",") if docker_output else None
            if len(status_results) == len(status_fields):
                for field in status_fields:
                    Log.log("  {:12}{}".format(field, status_results.pop(0)))
        else:
            Log.log("  {:12}{}".format("Image", self.conf_req('image')))
            Log.log("  {:12}{}".format("Status", "container not created"))

    @forbid_active_container
    def up(self) -> ReturnCode:
        container_name = self.conf_req("name")
        cmd = ["run", "-d", "--name", container_name]
        cmd += self.cli_opts()
        code = self(cmd + [self.conf_req("image"), "top", "-b"])
        if code == 0:
            Log.success(f"{container_name} is now active")
        else:
            Log.error(f"starting {container_name}", f"error code {code}")
        return code


class Log():
    @staticmethod
    def cmd(args) -> None:
        if args:
            echo(style(f"$ {' '.join(args)}", fg="cyan"))

    @staticmethod
    def error(context, message) -> None:
        echo(f"{style('ERROR:', fg='red')} {context}\n\t{message}")

    @staticmethod
    def log(message) -> None:
        echo(message)

    @staticmethod
    def success(context) -> None:
        echo(f"{style('SUCCESS:', fg='green')} {context}")

    @staticmethod
    def warning(message) -> None:
        echo(f"{style('WARNING:', fg='yellow')} {message}")
