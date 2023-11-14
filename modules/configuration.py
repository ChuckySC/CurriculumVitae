from modules.constants import Constants
from functions.universal import load_json

from pathlib import Path
import logging
import os

class Configuration:
    config_file_path = 'pyconfig.json'

    CONFIG_LOCAL_STR = 'local'
    CONFIG_TEST_STR = 'test'
    CONFIG_LIVE_STR = 'live'

    CONFIGTOUSE = CONFIG_LOCAL_STR
    
    description = None
    
    logger = None

    def __init__(self, id:int = None):
        self.logger = logging.getLogger(Constants.project_name)
        self.config_file_path = os.path.join(
            Path(os.path.dirname(__file__)).parents[0], 
            self.config_file_path
        )
        data = load_json(self.config_file_path)
        try:
            self.loaddata(data[self.CONFIGTOUSE])
        except Exception as e:
            self.logger.exception(e)
            raise

    @staticmethod
    def getenvironment():
        return Configuration.CONFIGTOUSE

    def loaddata(self, environment):
        self.description = environment['description']