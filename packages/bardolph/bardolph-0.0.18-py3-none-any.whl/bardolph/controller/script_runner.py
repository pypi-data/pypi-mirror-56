import logging

from ..lib.job_control import Job
from .machine import Machine
from ..parser.parse import Parser


class ScriptRunner(Job):
    def __init__(self):
        self._program = None
        self._parser = Parser()
        self._machine = Machine()

    @classmethod
    def from_file(cls, file_name):
        new_instance = ScriptRunner()
        new_instance.load_file(file_name)
        return new_instance

    @classmethod
    def from_string(cls, script):
        new_instance = ScriptRunner()
        new_instance.load_string(script)
        return new_instance

    def load_file(self, file_name):
        self._program = self._parser.load(file_name)
        if self._program is None:
            logging.error(self._parser.get_errors())
        return self._program

    def load_string(self, input_string):
        self._program = self._parser.parse(input_string)
        if self._program is None:
            logging.error(self._parser.get_errors())
        return self._program
    
    @property
    def program(self):
        return self._program

    def execute(self):
        if self._program is not None:
            self._machine.run(self._program)

    def request_stop(self):
        self._machine.stop()
