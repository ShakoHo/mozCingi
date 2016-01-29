__author__ = 'shako'
from mozCingi.steps.step import AbsStep
class AbsExecutor(AbsStep):

    def launch_execute_file(self):
        pass

    def run(self):
        self.launch_execute_file()

