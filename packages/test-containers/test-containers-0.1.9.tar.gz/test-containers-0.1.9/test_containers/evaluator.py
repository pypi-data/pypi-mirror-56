from test_containers.environments import DockerTestEnvironment, KubernetesTestEnvironment
from test_containers.utils import execute_command
import os


class Evaluator:
    def __init__(self):
        self.__application = None
        self.__test = None
        self.__test_result = None
        self.__unit_test_object = None

    def __evaluate_result(self):
        if "exit-code" in self.__test.arguments:
            self.__unit_test_object.assertEqual(
                self.__test_result["exit-code"],
                self.__test.arguments["exit-code"]
            )

        if "expected-output" in self.__test.arguments:
            self.__unit_test_object.assertRegex(
                self.__test_result["output"],
                self.__test.arguments["expected-output"]
            )

        if "excluded-output" in self.__test.arguments:
            self.__unit_test_object.assertNotRegex(
                self.__test_result["output"],
                self.__test.arguments["excluded-output"]
            )

        if "expected-error" in self.__test.arguments:
            self.__unit_test_object.assertRegex(
                self.__test_result["error"],
                self.__test.arguments["expected-error"]
            )

        if "excluded-error" in self.__test.arguments:
            self.__unit_test_object.assertNotRegex(
                self.__test_result["error"],
                self.__test.arguments["excluded-error"]
            )

        if "files" in self.__test.arguments:
            for file_tests in self.__test.arguments["files"]:
                file_path = file_tests["path"]
                file_content = self.__test_result["files"][file_path]
                if "exists" in file_tests:
                    self.__unit_test_object.assertEqual(file_content is not None, file_tests["exists"])
                if "expected-content" in file_tests or "excluded-content" in file_tests:
                    self.__unit_test_object.assertIsNotNone(file_content)
                if "expected-content" in file_tests:
                    self.__unit_test_object.assertRegex(file_content, file_tests["expected-content"])
                if "excluded-content" in file_tests:
                    self.__unit_test_object.assertNotRegex(file_content, file_tests["excluded-content"])

    def run_test(self, unit_test_object, application, test):
        self.__unit_test_object = unit_test_object
        self.__application = application
        self.__test = test
        if self.__application.application_type == "docker":
            environment = DockerTestEnvironment(container=self.__application)
        elif self.__application.application_type == "kubernetes":
            environment = KubernetesTestEnvironment(pod=self.__application)
        else:
            raise NotImplementedError
        with environment:
            if self.__test.environment == "external":
                self.__test_result = execute_command(self.__test.command)
                if "files" in self.__test.arguments:
                    self.__test_result["files"] = {}
                    for file_tests in self.__test.arguments["files"]:
                        file_path = file_tests["path"]
                        if os.path.exists(file_path):
                            if "expected-content" in file_tests or "excluded-content" in file_tests:
                                with open(file_path) as f:
                                    file_content = f.read()
                                self.__test_result["files"][file_path] = file_content
                            else:
                                self.__test_result["files"][file_path] = ""
                        else:
                            self.__test_result["files"][file_path] = None
            elif self.__test.environment == "internal":
                self.__test_result = environment.execute_command(self.__test.command)
                if "files" in self.__test.arguments:
                    self.__test_result["files"] = {}
                    for file_tests in self.__test.arguments["files"]:
                        file_path = file_tests["path"]
                        command_result = environment.execute_command("cat %s" % file_path)
                        if command_result["exit-code"] == 0:
                            self.__test_result["files"][file_path] = command_result["output"]
                        else:
                            self.__test_result["files"][file_path] = None
            else:
                raise NotImplementedError
            self.__evaluate_result()
