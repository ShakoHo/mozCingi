__author__ = 'shako'
import os
import zipfile
from mozCingi.steps.executor import AbsExecutor
from b2g_util.util.adb_helper import AdbWrapper
class MutagenExecutorWithoutITP(AbsExecutor):
    DEFAULT_EXEC_LOG_NAME = "exec.log"

    def unpack_data(self):
        pack_file_name = self.fuzzer_name + "_" + str(self.obj_index) + ".zip"
        pack_file_path = os.path.join(self.working_dir, self.DEFAULT_ROOT_TMP_DIR, pack_file_name)
        with zipfile.ZipFile(pack_file_path) as zip_file_obj:
            zip_file_obj.extractall(self.DEFAULT_ROOT_TMP_DIR)

    def launch_execute_file(self):
        working_dir = os.path.join(self.DEFAULT_ROOT_TMP_DIR, self.DEFAULT_ROOT_OUTPUT_DIR, self.fuzzer_name)
        cmd_format = "cd %s; bash %s 2>&1 > %s"
        execution_log_dir = os.path.join(self.working_dir, self.DEFAULT_ROOT_LOG_DIR, self.fuzzer_name)
        if os.path.exists(execution_log_dir) is False:
            os.makedirs(execution_log_dir)
        execution_log_path = os.path.join(execution_log_dir, self.DEFAULT_EXEC_LOG_NAME)
        cmd_str = cmd_format % (working_dir, self.DEFAULT_LAUNCH_SCRIPT_FILE_NAME, execution_log_path)
        adb_obj = AdbWrapper()
        adb_obj.adb_forward(local="tcp:2828", remote="tcp:2828")
        os.system(cmd_str)



