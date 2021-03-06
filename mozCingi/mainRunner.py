__author__ = 'shako'
#!/usr/bin/python
import os
import sys
import json
import time
import argparse
import logging
import importlib
from apscheduler.schedulers.background import BackgroundScheduler
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if len(logger.handlers) == 0:
    logger.addHandler(logging.StreamHandler())


class JsonHandler(PatternMatchingEventHandler):
    def set_handler(self, oncreated=None, onmodified=None, ondeleted=None):
        self.create_handler = oncreated
        self.modify_handler = onmodified
        self.delete_handler = ondeleted

    def on_created(self, event):
        self.create_handler(event.src_path)

    def on_modified(self, event):
        self.modify_handler(event.src_path)

    def on_deleted(self, event):
        self.delete_handler(event.src_path)


class MainRunner(object):
    workers = {}
    dirpath = '.'
    defaultOutputPath = 'output'

    def __init__(self, dirpath='.'):
        '''
        local path for load config
        '''
        logger.info("Initialing Main Runner for Fuzzy Testing")
        if os.path.isdir(dirpath):
            self.dirpath = dirpath
            logger.info("loading runner config folder: " + dirpath)
        else:
            logger.info(dirpath + " is invalid, use default path instead")

        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.load_dir(dirpath)

        event_handler = JsonHandler(patterns=["*.json"], ignore_directories=True)
        event_handler.set_handler(oncreated=self.load, onmodified=self.load, ondeleted=self.remove)
        observer = Observer()
        observer.schedule(event_handler, self.dirpath, recursive=True)
        observer.start()

    def load_dir(self, folder):
        (dirpath, dirnames, filenames) = os.walk(folder).next()
        for fname in filenames:
            if 'json' in fname[-4:]:
                self.load(os.path.join(dirpath, fname))

    def load(self, fp):
        '''
        given a json file, load and create a task run regularly
        '''
        logger.info(fp + " was loaded!")
        with open(fp) as in_data:
            try:
                data = json.load(in_data)
                data['path'] = fp
            except ValueError as e:
                logger.warning(fp + " loaded failed: " + e.message)
                return None
            interval = 30
            if 'interval' in data:
                interval = int(data['interval'])

            if 'output' in data:
                if 'defaultOutputPath' in data['output']:
                    self.defaultOutputPath = data['output']['defaultOutputPath']
                if 'dirpath' in data['output']:
                    data['output']['outputPath'] = os.path.join(self.defaultOutputPath, data['output']['dirpath'])
            else:
                data['output'] = {'outputPath': self.defaultOutputPath}

            if 'type' not in data:
                logger.error("Missing type attribute in \
                                your configuration file [%s]" % fp)
                return None

            if fp in self.workers:  # existing runner found
                logger.info("Update exisitng runner [%s]" % fp)
                runner = self.workers[fp]
                runner.update(**data)
                # //memo: Interval can't be modified
                self.scheduler.modify_job(job_id=fp,
                                          func=runner.run,
                                          name=runner.name
                                          )

            else:  # Create new
                logger.info("Create new runner [%s]" % fp)
                module_path = data['type'][:data['type'].rfind(".")]
                object_name = data['type'][data['type'].rfind(".") + 1:]
                try:
                    runner_module = getattr(importlib.import_module(
                                            module_path), object_name)
                except Exception as e:
                    logger.exception(e)
                    return None

                runner = runner_module(**data)
                self.workers[fp] = runner
                self.scheduler.add_job(runner.run, 'interval',
                                       id=fp,
                                       name=runner.name,
                                       seconds=interval
                                       )
            return runner
        return None

    def list(self):
        '''
        to list all configs loaded
        format: [squence number] [minion name] [config_path] [status]
        '''
        for (fp, worker) in self.workers:
            logger.info("path=" + fp + "," + str(worker) + ";")

    def remove(self, fp):
        '''
        given file path, stop running instance if possible
        '''
        if fp in self.workers:
            self.workers[fp].onstop()
            self.scheduler.remove_job(job_id=fp)
            del self.workers[fp]
            return True
        return False

    def remove_advanced(self):
        '''
        TODO:
        1. remove by start, end
        2. by directory(?)
        '''
        pass

    def unload_all(self):
        '''
        stop all running instances
        '''
        self.scheduler.shutdown()

    def pause(self, fp):
        '''
        simply stop running instance but not remove config
        TODO: should have timeout if stop failed
        '''
        self.scheduler.pause(job_id=fp)

    def resume(self, sn):
        # not sure we can do this
        pass

    def __del__(self):
        self.unload_all()

    def get_config(self):
        conf = {}
        return conf

    def _wake(self):
        '''
        For periodical minions, waking them according to timing
        '''
        pass


def main():
    # TODO: Add test for loading files
    parser = argparse.ArgumentParser(description="Fuzz Runner")
    parser.add_argument('--dirpath', help="FuzzRunner will load the configuration from this directory",
                        default='.')
    options = parser.parse_args(sys.argv[1:])
    b = MainRunner(**options.__dict__)
    logger.info('Press Ctrl+{0} to exit'.format(
                'Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main
        # thread alive).
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
            del b

if __name__ == '__main__':
    main()
