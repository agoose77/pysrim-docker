import srim

from .executor import DockerExecutor


class SR(DockerExecutor, srim.SR):
    executable_path = "/tmp/srim/SR Module/SRModule.exe"
    results_cls = srim.output.SRResults

    def _prepare_input_files(self):
        self._write_input_file()
