import contextlib
import os
import subprocess
import tempfile


@contextlib.contextmanager
def cwd_as(path):
    cwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(cwd)


class DockerExecutor:
    docker_image = "costrouc/srim"
    entrypoint_contents = """
#!/usr/bin/env bash
shopt -s extglob globstar nullglob
set -eu

pwd > pwd

# Copy inputs
cp -R "{directory}/." .

# Run wine
xvfb-run -a wine "{executable}"

# Copy outputs (recursively)
cp -n **/*.{{IN,txt}} "{directory}/" || true
"""

    @property
    def executable_path(self):
        raise NotImplementedError

    @property
    def results_cls(self):
        raise NotImplementedError

    def run(self, *args, mount_path="/usr/local/src/srim", **kwargs):
        local_path = tempfile.mkdtemp()

        srim_directory, srim_executable = os.path.split(self.executable_path)
        assert srim_directory and srim_executable

        with cwd_as(local_path):
            self._prepare_input_files()

            # Make sure compatible with Windows, OSX, and Linux
            # If 'wine' command exists use it to launch TRIM
            subprocess.check_call(
                [
                    "docker",
                    "run",
                    "--rm",
                    "--volume",
                    f"{local_path}:{mount_path}",
                    "--workdir",
                    srim_directory,
                    self.docker_image,
                    "bash",
                    "-c",
                    self.entrypoint_contents.format(
                        executable=srim_executable, directory=mount_path
                    ),
                ]
            )

        return self.results_cls(local_path)
