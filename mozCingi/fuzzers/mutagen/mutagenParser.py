__author__ = 'shako'
import os
from mozCingi.steps.parser import AbsParser
from mozCingi.util.simpleParser import SimpleParser
class MutagenParser(AbsParser):
    simpleParserObj = None
    log_dir_path = ""
    DEFAULT_EXEC_LOG_NAME = "exec.log"
    DEFAULT_STDERR_LOG_NAME = "stderr.log"

    def parse_data(self):
        self.simpleParserObj = SimpleParser()
        self.log_dir_path = os.path.join(self.DEFAULT_ROOT_LOG_DIR, self.fuzzer_name)
        input_data_path = os.path.join(self.log_dir_path, self.DEFAULT_EXEC_LOG_NAME)
        self.simpleParserObj.parse_data(input_data_path)

    def output_data(self):
        output_data_path = os.path.join(self.log_dir_path, self.DEFAULT_STDERR_LOG_NAME)
        self.simpleParserObj.output_data(output_data_path)
