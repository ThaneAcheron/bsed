import unittest
import os
from os import path
import json
from shutil import copy

from .context import bted
import bted.definitions as definitions
from bted import interpreter


class TestInPlaceFlag(unittest.TestCase):

    @staticmethod
    def __f_to_str(file_path):
        with open(file_path, 'r') as fin:
            content = fin.read()
        return content

    def setUp(self):
        self.test_files = [path.join(definitions.TESTS_DIR, f)
                           for f in os.listdir(definitions.TESTS_DIR)
                           if f.startswith('test_') and f.endswith('.json')]
        command_tree_fp = definitions.COMMAND_TOKEN_TREE
        translations_fp = definitions.COMMAND_TRANSLATIONS_FILE
        self.interpreter = interpreter.Interpreter(command_tree_fp, translations_fp)

    def perform_test(self, command: [str], input_file: str, expected_result_file: str):
        expected = TestInPlaceFlag.__f_to_str(expected_result_file)
        tmp_file = 'tmp.txt'
        copy(input_file, 'tmp.txt')
        cmd, flags = self.interpreter.build_command(command, tmp_file)
        self.interpreter.execute_command(cmd, flags, return_output=True)
        res = TestInPlaceFlag.__f_to_str(tmp_file)
        os.remove(tmp_file)
        self.assertEqual(expected, res)

    def test_all(self):
        for test_file in self.test_files:
            print(path.split(test_file)[-1])
            with open(test_file, 'r') as fin:
                test_dict = json.load(fin)
            for command, tests in test_dict.items():
                print('\t%s' % command)
                for test in tests:
                    input_file = path.join(definitions.TEST_FILES_DIR, test['input'])
                    expected_file = path.join(definitions.TEST_FILES_DIR, test['expected'])
                    command = test['command'] + ['-i']
                    self.perform_test(command, input_file, expected_file)
