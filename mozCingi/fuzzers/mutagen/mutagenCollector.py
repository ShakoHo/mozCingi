__author__ = 'shako'
import os
from mozCingi.util.fuzzManagerCollector import FuzzManagerCollector
from mozCingi.steps.collector import AbsCollector
class MutagenCollector(AbsCollector):
    DEFAULT_EXEC_LOG_NAME = "exec.log"
    DEFAULT_STDERR_LOG_NAME = "stderr.log"
    fuzzManagerObj = None

    def run(self):
        log_dir_path = os.path.join(self.DEFAULT_ROOT_LOG_DIR, self.fuzzer_name)
        stdout_log = os.path.join(log_dir_path, self.DEFAULT_EXEC_LOG_NAME)
        stderr_log = os.path.join(log_dir_path, self.DEFAULT_STDERR_LOG_NAME)
        self.fuzzManagerObj = FuzzManagerCollector()
        self.fuzzManagerObj.collector_submit(stdout_log, stderr_log, self.configurations['collector_svr_addr'],
                                             self.configurations['collector_svr_port'], self.configurations['collector_svr_proto'],
                                             self.configurations['collector_tool'], self.configurations['collector_client_id'],
                                             self.configurations['collector_token_path'], self.configurations['product'],
                                             self.configurations['platform'], self.configurations['os'],)
