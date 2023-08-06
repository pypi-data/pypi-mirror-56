from test_containers.application import Application
from test_containers.evaluator import Evaluator
from test_containers.test import Test
from test_containers.utils import parse_yaml_file, TextTestResultWithSuccesses
import argparse
import os
import sys
import unittest
import warnings

dir_path = os.path.dirname(os.path.abspath(__file__))


class UnitTestGenerator(unittest.TestCase):
    test_functions = []

    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)

    @staticmethod
    def generate_tests(tests):
        def generate_test_method(test):
            def generated_test_method(self):
                evaluator.run_test(self, test["application"], test["test"])
            return generated_test_method

        if UnitTestGenerator.test_functions:
            while UnitTestGenerator.test_functions:
                delattr(UnitTestGenerator, UnitTestGenerator.test_functions.pop())

        evaluator = Evaluator()
        for test in tests:
            test_name = "test_%s_%s" % (test["application"].name, test["test"].name)
            setattr(UnitTestGenerator, test_name, generate_test_method(test))
            UnitTestGenerator.test_functions.append(test_name)


def get_pending_evaluations(tests):
    pending_evaluations = []
    for application_tests in tests:
        application_object = Application(
            application_tests["application"]["name"],
            application_tests["application"]["type"],
            application_tests["application"]["arguments"]
        )
        for test in application_tests["tests"]:
            test_arguments = {key: test[key] for key in test.keys()
                              if key not in ["name", "command", "environment"]}
            test_object = Test(
                test["name"],
                test["command"],
                test["environment"],
                test_arguments
            )
            pending_evaluations.append({
                "application": application_object,
                "test": test_object
            })
    return pending_evaluations


def run(path, exit=True):
    UnitTestGenerator.generate_tests(get_pending_evaluations(parse_yaml_file(path)))
    tests = unittest.defaultTestLoader.loadTestsFromTestCase(UnitTestGenerator)
    suite = unittest.TestSuite()
    suite.addTests(tests)
    result = unittest.TextTestRunner(resultclass=TextTestResultWithSuccesses).run(suite)
    if exit:
        if result.wasSuccessful():
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        return result


if __name__ == "__main__":
    with open(os.path.join(dir_path, "help.txt"), "r") as f:
        help_text = f.read()
    parser = argparse.ArgumentParser(description=help_text)
    parser.add_argument("--config", help="configuration file to get the tests from", required=True)
    args = parser.parse_args()
    run(args.config)
