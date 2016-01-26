__author__ = 'shako'
import os
from mozCingi.util.mozITPWrapper import MozITPWrapper
from mozCingi.steps.executor import AbsExecutor
class MutagenExecutor(AbsExecutor):
    DEFAULT_EXEC_LOG_NAME = "exec.log"

    def launch_execute_file(self):
        mozitp_obj = MozITPWrapper()
        pack_file_name = self.fuzzer_name + "_" + str(self.obj_index) + ".zip"
        pack_file_path = os.path.join(self.working_dir, self.DEFAULT_ROOT_TMP_DIR, pack_file_name)
        execution_log_dir = os.path.join(self.working_dir, self.DEFAULT_ROOT_LOG_DIR, self.fuzzer_name)
        if os.path.exists(execution_log_dir) is False:
            os.makedirs(execution_log_dir)
        execution_log_path = os.path.join(execution_log_dir, self.DEFAULT_EXEC_LOG_NAME)
        mozitp_obj.launch_itp_for_fuzz(pack_file_path, execution_log_path)
        mozitp_obj.stop_itp()


