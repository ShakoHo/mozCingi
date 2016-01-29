__author__ = 'shako'
import os
import zipfile
from mozCingi.steps.generator import AbsGenerator
from mozCingi.util.mutagenWrapper import MutagenWrapper


class MutagenGenerator(AbsGenerator):

    DEFAULT_MP3_TITLE_LENGTH = 30
    DEFAULT_TESTVARS_FILE_NAME = "testvars.json"
    DEFAULT_EXEC_LOG_NAME = "exec.log"
    DEFAULT_EXEC_CMD = ["adb logcat 2>&1 > logcat.log & \n",
                        "gaiatest %s --address %s --testvars %s 2>&1|tee %s \n",
                        "cat logcat.log"]

    data_folder_name = ""
    output_folder_name = ""
    output_audio_file_path_list = []

    def generate_data(self):
        self.data_folder_name = os.path.join(self.DEFAULT_ROOT_DATA_DIR, self.fuzzer_name)
        self.output_folder_name = os.path.join(self.DEFAULT_ROOT_OUTPUT_DIR, self.fuzzer_name)
        if os.path.exists(self.output_folder_name) is False:
            os.mkdir(self.output_folder_name)

        audio_files_src_folder_path = os.path.join(self.data_folder_name, self.configurations['audio_files_folder_name'])
        audio_files_dst_folder_path = os.path.join(self.output_folder_name, self.configurations['audio_files_folder_name'])
        if os.path.exists(audio_files_dst_folder_path) is False:
            os.mkdir(audio_files_dst_folder_path)

        mutagen_obj = MutagenWrapper()
        self.output_audio_file_path_list = mutagen_obj.mutate_audio_file_header(audio_files_src_folder_path,
                                                                                audio_files_dst_folder_path,
                                                                                self.configurations['data_gen_num'])

    def generate_steps(self):
        test_cases_src_folder_path = os.path.join(self.data_folder_name, self.configurations['test_cases_folder_name'])
        test_cases_dst_folder_path = os.path.join(self.output_folder_name, self.configurations['test_cases_folder_name'])
        black_list_file_path = os.path.join(self.data_folder_name, self.configurations['black_list_file_name'])
        test_case_black_list = self.read_black_list(black_list_file_path)
        if os.path.exists(test_cases_dst_folder_path) is False:
            os.mkdir(test_cases_dst_folder_path)

        tmp_list = [t_name for t_name in os.listdir(test_cases_src_folder_path) if t_name.endswith(".py")]
        filter_list = [f_name for f_name in tmp_list if f_name not in test_case_black_list]
        for src_case_file_name in filter_list:
            new_file_no = 1
            for audio_file_path in self.output_audio_file_path_list:
                if src_case_file_name not in test_case_black_list:
                    src_case_file_path = os.path.join(test_cases_src_folder_path, src_case_file_name)
                    new_file_name = src_case_file_name.split(".")[0] + "_" + str(new_file_no) + "." + src_case_file_name.split(".")[1]
                    new_file_path = os.path.join(test_cases_dst_folder_path, new_file_name)
                    self.mutate_test_case(src_case_file_path, audio_file_path, new_file_path)
                    new_file_no += 1

    def generate_execution_file(self):
        self.generate_testvars()
        execution_log_path = self.DEFAULT_EXEC_LOG_NAME
        execution_target = "127.0.0.1:2828"
        for index in xrange(0, len(self.DEFAULT_EXEC_CMD)):
            if "%s" in self.DEFAULT_EXEC_CMD[index]:
                self.DEFAULT_EXEC_CMD[index] = self.DEFAULT_EXEC_CMD[index] % (self.configurations['test_cases_folder_name'],
                                                                               execution_target,
                                                                               self.DEFAULT_TESTVARS_FILE_NAME,
                                                                               execution_log_path)
        execution_file_path = os.path.join(self.output_folder_name, self.DEFAULT_LAUNCH_SCRIPT_FILE_NAME)
        file_obj = open(execution_file_path, "w")
        file_obj.writelines(self.DEFAULT_EXEC_CMD)
        file_obj.close()

    def generate_testvars(self):
        testvars_ctnt = ["{\"acknowledged_risks\": true}"]
        testvars_file_path = os.path.join(self.output_folder_name, self.DEFAULT_TESTVARS_FILE_NAME)
        file_obj = open(testvars_file_path, "w")
        file_obj.writelines(testvars_ctnt)
        file_obj.close()

    def mutate_test_case(self, src_case_file_path, audio_file_path, new_file_path):
        operator = {"push_resource": "        self.device.file_manager.push_file(\"../../" + audio_file_path + "\", None, 1)"}
        file_obj = open(src_case_file_path, "r")
        file_ctnt = file_obj.readlines()
        flag = 0
        for index in range(0, len(file_ctnt)):
            for search_key in operator.keys():
                if search_key in file_ctnt[index]:
                    file_ctnt[index] = operator[search_key]
                    flag = 1
        if flag == 1:
            new_file_obj = open(new_file_path, "w")
            new_file_obj.writelines(file_ctnt)
            new_file_obj.close()
        file_obj.close()

    def read_black_list(self, input_file_path):
        with open(input_file_path) as f:
            return f.readlines()

    def pack_files(self):
        if os.path.exists(self.DEFAULT_ROOT_TMP_DIR) is False:
            os.mkdir(self.DEFAULT_ROOT_TMP_DIR)
        zip_file_name = self.fuzzer_name + "_" + str(self.obj_index) + ".zip"
        zip_file_path = os.path.join(self.DEFAULT_ROOT_TMP_DIR, zip_file_name)
        zip_file_obj = zipfile.ZipFile(zip_file_path, "w")
        try:
            for root, dirs, files in os.walk(self.output_folder_name):
                for archive_file in files:
                    zip_file_obj.write(os.path.join(root, archive_file))
        finally:
            zip_file_obj.close()
