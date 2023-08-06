import os


class Application:
    def __init__(self, name, application_type, arguments):
        self.__name = name.replace("-", "_").replace(" ", "_")
        self.__application_type = application_type
        self.__arguments = arguments
        self.__expand_paths()

    def __expand_paths(self):
        if self.__application_type == "docker" and "volumes" in self.__arguments:
            volumes = self.__arguments["volumes"]
            for path in volumes.keys():
                abs_path = os.path.abspath(path)
                if not path == abs_path:
                    self.__arguments["volumes"][abs_path] = self.__arguments["volumes"][path]
                    self.__arguments["volumes"].pop(path)

    @property
    def name(self):
        return self.__name

    @property
    def application_type(self):
        return self.__application_type

    @property
    def arguments(self):
        return self.__arguments
