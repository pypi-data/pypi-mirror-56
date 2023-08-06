"""
Represents a single session of roamer.
Preps the state, gathers records from disk, opens user's file editor
and passes into the Engine for processing
"""

from __future__ import print_function
import os
import sys
from roamer.file_edit import file_editor
from roamer.directory import Directory
from roamer.edit_directory import EditDirectory
from roamer.engine import Engine
from roamer import record
from roamer.database import db_init

try:
    input = raw_input  # pylint: disable=invalid-name, redefined-builtin
except NameError:
    pass

class Session(object):
    def __init__(self, cwd=None, skipapproval=True):
        self.cwd = cwd
        self.skipapproval = skipapproval
        if cwd is None:
            self.cwd = os.getcwd()
        db_init()
        raw_entries = os.listdir(self.cwd)
        self.directory = Directory(self.cwd, raw_entries)
        self.edit_directory = None
        record.add_dir(self.directory)

    def run(self):
        output = file_editor(self.directory.text())
        self.process(output)

    def print_raw(self):
        print(self.directory.text())

    def process(self, output):
        self.edit_directory = EditDirectory(self.cwd, output)
        engine = Engine(self.directory, self.edit_directory)
        engine.compile_commands()
        print(engine.commands_to_str())
        if engine.commands and not self.skipapproval:
            print(
                'Argument --skip-approval could be used to run roamer '
                'in a noninteractive mode.'
            )
            try:
                answer = input('Please indicate approval: [y/N] ')
            except KeyboardInterrupt:
                # Add line feed
                print()
                answer = None
            if not answer or answer[0].lower() != 'y':
                print('You did not indicate approval.')
                sys.exit(1)
        engine.run_commands()
        record.add_dir(Directory(self.cwd, os.listdir(self.cwd)))
