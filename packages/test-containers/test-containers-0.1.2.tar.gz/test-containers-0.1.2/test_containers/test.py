from test_containers.utils import execute_command


class Test:
    def __init__(self, name, command, environment, arguments):
        self.__name = name.replace("-", "_").replace(" ", "_")
        self.__command = command
        self.__environment = environment
        self.__arguments = arguments
        self.__expand_environment_variables()

    def __expand_environment_variables(self):
        if "environment-variables" not in self.__arguments:
            return

        environment_variables = self.__arguments["environment-variables"]
        for variable, definition in environment_variables.items():
            environment_variables[variable] = execute_command(definition)["output"]

        for key in ["command", "expected-output", "excluded-output", "expected-error", "excluded-error"]:
            if key not in self.__arguments:
                continue
            for variable, value in environment_variables.items():
                self.__arguments[key] = self.__arguments[key].replace("${%s}" % variable, value)

    @property
    def name(self):
        return self.__name

    @property
    def command(self):
        return self.__command

    @property
    def environment(self):
        return self.__environment

    @property
    def arguments(self):
        return self.__arguments
