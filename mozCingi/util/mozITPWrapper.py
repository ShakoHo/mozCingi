__author__ = 'shako'
import os
class MozITPWrapper(object):
    DEFAULT_ITP_DIR_PATH = "lib/MozITP"
    DEFAULT_ITP_LAUNCH_CMD_NAME = "launch.sh"
    DEFAULT_ITP_STOP_CMD_NAME = "bin/stop.sh"

    def launch_itp_for_fuzz(self, input_pack_file_path, output_log_path):
        cmd_format = "cd %s; bash %s fuzz %s 2>&1 > %s"
        cmd_str = cmd_format % (self.DEFAULT_ITP_DIR_PATH, self.DEFAULT_ITP_LAUNCH_CMD_NAME,
                                input_pack_file_path, output_log_path)
        print "launch ITP script! cmd : [%s] " % cmd_str
        os.system(cmd_str)

    def stop_itp(self):
        cmd_format = "cd %s; bash %s"
        cmd_str = cmd_format % (self.DEFAULT_ITP_DIR_PATH, self.DEFAULT_ITP_STOP_CMD_NAME)
        print "stop ITP script! cmd : [%s] " % cmd_str
        os.system(cmd_str)
