import os
import unittest
from argparse import ArgumentParser
from contextlib import redirect_stdout
from io import StringIO
from typing import Union, List

from generate import generator

cwd = os.path.dirname(__file__)
test_output_log_dir = os.path.abspath(os.path.join(cwd, 'data'))
template_dir = os.path.abspath(os.path.join(cwd, '..', 'Sample'))
settings_file = os.path.abspath(os.path.join(cwd, '..', 'Default', 'settings.py'))
cache_dir = os.path.abspath(os.path.join(cwd, 'cache'))
model_dir = os.path.abspath(os.path.join(cwd, 'model'))

class HelpPrinted(Exception):
    pass


# Override the exit method
def exit(self, status=0, message=None):
    if message:
        self._print_message(message)
    raise HelpPrinted()


ArgumentParser.exit = exit


class CLITestCase(unittest.TestCase):
    def do_test(self, args: Union[str, List[str]], expected_fname: str) -> None:
        args = args.split() if isinstance(args, str) else args
        if '-td' not in args:
            args += ['-td', template_dir]
        if '-o' not in args:
            args += ['-o', model_dir]
        if '-cd' not in args:
            args += ['-cd', cache_dir]

        actual = StringIO()
        expected_file = os.path.join(test_output_log_dir, expected_fname)
        with redirect_stdout(actual):
            try:
                generator(args)
            except HelpPrinted:
                pass
        if os.path.exists(expected_file):
            with open(expected_file) as f:
                expected = f.read()
            self.assertEqual(expected.strip(), actual.getvalue().strip())
        else:
            with open(expected_file, 'w') as f:
                f.write(actual.getvalue())
            self.fail(f"{expected_file} created - rerun test")

    def test_help(self):
        self.do_test("-h", "help")

    def test_force_download(self):
        self.do_test(settings_file + " -f -u http://hl7.org/fhir/R4", "forcedr4")

    def test_use_cache(self):
        self.do_test(settings_file + " -c -u http://hl7.org/fhir/R4", "usecache")


if __name__ == '__main__':
    unittest.main()
