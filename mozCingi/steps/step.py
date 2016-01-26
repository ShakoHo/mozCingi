__author__ = 'shako'
import os
class AbsStep(object):

    DEFAULT_ROOT_DATA_DIR = "data"
    DEFAULT_ROOT_OUTPUT_DIR = "output"
    DEFAULT_ROOT_LOG_DIR = "log"
    DEFAULT_ROOT_TMP_DIR = "tmp"
    DEFAULT_ROOT_LIB_DIR = "lib"

    configurations = {}

    def __init__(self, name, fuzzer_name, obj_index, **parameters):
        self.name = name
        self.working_dir = os.getcwd()
        self.fuzzer_name = fuzzer_name
        self.obj_index = obj_index
        self.read_configuration(**parameters)
        self.validate_default_folder_exist

    def validate_default_folder_exist(self):
        validate_folder_list = []
        validate_folder_list.append(os.path.join(self.working_dir, self.DEFAULT_ROOT_DATA_DIR))
        validate_folder_list.append(os.path.join(self.working_dir, self.DEFAULT_ROOT_OUTPUT_DIR))
        validate_folder_list.append(os.path.join(self.working_dir, self.DEFAULT_ROOT_LOG_DIR))
        validate_folder_list.append(os.path.join(self.working_dir, self.DEFAULT_ROOT_TMP_DIR))
        validate_folder_list.append(os.path.join(self.working_dir, self.DEFAULT_ROOT_LIB_DIR))

        for dir_path in validate_folder_list:
            if os.path.exists(dir_path) is False:
                os.makedirs(dir_path)

    def read_configuration(self, **kwargs):
        self.configurations = kwargs

    def run(self):
        pass

