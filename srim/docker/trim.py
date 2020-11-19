import srim

from .executor import DockerExecutor


class TRIM(DockerExecutor, srim.TRIM):
    executable_path = "/tmp/srim/TRIM.exe"
    results_cls = srim.output.Results

    def _prepare_input_files(self):
        self._write_input_files()
