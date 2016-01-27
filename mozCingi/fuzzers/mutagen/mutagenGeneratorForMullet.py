__author__ = 'shako'
import os
from mutagenGenerator import MutagenGenerator

class MutagenGeneratorForMullet(MutagenGenerator):

    DEFAULT_EXEC_CMD = ["adb forward --remove-all \n",
                        "Xvfb :10 -ac 2> /dev/null & \n",
                        "export DISPLAY=:10 \n",
                        "GAIATEST_SKIP_WARNING=1 gaiatest %s --binary=/home/vagrant/gaia/firefox/firefox-bin --profile=/home/vagrant/gaia/profile/ --app-arg=-chrome --app-arg=chrome://b2g/content/shell.html --testvars %s 2>&1|tee %s \n",
                        "killall Xvfb \n",
                        "cat gecko.log"]

    def generate_execution_file(self):
        self.generate_testvars()
        execution_log_path = self.DEFAULT_EXEC_LOG_NAME
        for index in xrange(0, len(self.DEFAULT_EXEC_CMD)):
            if "%s" in self.DEFAULT_EXEC_CMD[index]:
                self.DEFAULT_EXEC_CMD[index] = self.DEFAULT_EXEC_CMD[index] % (self.configurations['test_cases_folder_name'],
                                                                               self.DEFAULT_TESTVARS_FILE_NAME,
                                                                               execution_log_path)
        execution_file_path = os.path.join(self.output_folder_name, self.DEFAULT_LAUNCH_SCRIPT_FILE_NAME)
        file_obj = open(execution_file_path, "w")
        file_obj.writelines(self.DEFAULT_EXEC_CMD)
        file_obj.close()
