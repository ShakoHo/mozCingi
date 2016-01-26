__author__ = 'shako'
import os
class FuzzManagerCollector(object):

    collector = None

    def create_collector(self):
        pass
        #with open(self.collector_token_path) as f:
        #    collector_token_str = f.read().rstrip()
        #self.collector = Collector(serverHost=self.collector_svr_addr, serverPort=self.collector_svr_port,
        #                           serverProtocol=self.collector_svr_proto, serverAuthToken=collector_token_str,
        #                           clientId=self.collector_client_id, tool=self.collector_tool)

    def execute_cmd(self, input_stdout_log_path, input_stderr_log_path, collector_svr_addr, collector_svr_port,
                    collector_svr_proto, collector_tool, collector_client_id, collector_token_path):
        cmd_str = "python lib/FuzzManager/Collector/Collector.py --submit --product mozilla-central --platform x86-64 --os linux " \
                  "--stdout %s --stderr %s --serverhost %s --serverport %s --serverproto %s --tool %s " \
                  "--clientid %s --serverauthtokenfile %s" % (input_stdout_log_path, input_stderr_log_path,
                                                              collector_svr_addr, collector_svr_port,
                                                              collector_svr_proto, collector_tool,
                                                              collector_client_id, collector_token_path)
        os.system(cmd_str)
