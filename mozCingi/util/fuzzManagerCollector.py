__author__ = 'shako'
import os
from lib.FuzzManager.Collector import Collector
from lib.FuzzManager.FTB.ProgramConfiguration import ProgramConfiguration
from lib.FuzzManager.FTB.Signatures.CrashInfo import CrashInfo

class SimpleCrashInfo(CrashInfo):
    def __init__(self, stdout, stderr, configuration, crashData=None):
        CrashInfo.__init__(self)

        if stdout is not None:
            self.rawStdout.extend(stdout)

        if stderr is not None:
            self.rawStderr.extend(stderr)

        if crashData is not None:
            self.rawCrashData.extend(crashData)

        self.configuration = configuration

        self.rawCrashData.extend(["test crash data"])

        self.crashAddress = long("0x123",16)
        self.backtrace.append("Crash|")
        self.crashInstruction = "test crash instruction"

class FuzzManagerCollector(object):

    def collector_submit(self, input_stdout_log_path, input_stderr_log_path, collector_svr_addr, collector_svr_port,
                         collector_svr_proto, collector_tool, collector_client_id, collector_token_path, input_product,
                         input_platform, input_os):

        with open(collector_token_path) as f:
            token_string = f.read().strip()
        with open(input_stdout_log_path) as f:
            stdout = f.read()
        with open(input_stderr_log_path) as f:
            stderr = f.read()

        configuration = ProgramConfiguration(input_product, input_platform, input_os)

        crash_info = CrashInfo.fromRawCrashData(stdout, stderr, configuration)

        collector = Collector(serverHost=collector_svr_addr, serverPort=collector_svr_port,
                              serverProtocol=collector_svr_proto, serverAuthToken=token_string,
                              clientId=collector_client_id, tool=collector_tool)

        collector.submit(crash_info)

    def execute_cmd(self, input_stdout_log_path, input_stderr_log_path, collector_svr_addr, collector_svr_port,
                    collector_svr_proto, collector_tool, collector_client_id, collector_token_path, input_product,
                    input_platform, input_os):
        cmd_str = "python lib/FuzzManager/Collector.py --submit --product %s --platform %s --os %s " \
                  "--stdout %s --stderr %s --serverhost %s --serverport %s --serverproto %s --tool %s " \
                  "--clientid %s --serverauthtokenfile %s" % (input_product, input_platform, input_os,
                                                              input_stdout_log_path, input_stderr_log_path,
                                                              collector_svr_addr, collector_svr_port,
                                                              collector_svr_proto, collector_tool,
                                                              collector_client_id, collector_token_path)
        print "execute collector command:[%s]" % cmd_str
        os.system(cmd_str)
