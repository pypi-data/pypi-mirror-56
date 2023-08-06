from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
from kubernetes.stream.ws_client import ERROR_CHANNEL
import docker
import kubernetes
import os
import shutil
import sys
import tempfile
import time
import yaml

docker_client = docker.from_env()

kubernetes.config.load_kube_config()
kubernetes_api = kubernetes.client.CoreV1Api()


class TestEnvironment:
    def __init__(self):
        pass

    def __enter__(self):
        self.__previous_working_dir = os.getcwd()
        self.__working_dir = tempfile.mkdtemp()
        os.chdir(self.__working_dir)

    def __exit__(self, type, value, traceback):
        os.chdir(self.__previous_working_dir)
        shutil.rmtree(self.__working_dir)

    def execute_command(self, command):
        raise NotImplementedError


class DockerTestEnvironment(TestEnvironment):
    def __init__(self, container):
        super().__init__()
        self.__container = container

    def __enter__(self):
        super().__enter__()
        self.__docker_container = docker_client.containers.run(detach=True, **self.__container.arguments)
        self.__wait_container_ready()

    def __exit__(self, type, value, traceback):
        self.__docker_container.stop()
        super().__exit__(type, value, traceback)

    def __wait_container_ready(self):
        inspection = docker_client.api.inspect_container(self.__docker_container.id)
        if "Health" in inspection["State"]:
            print("\nWaiting for container to be healthy... ", end="", file=sys.stderr, flush=True)
            while inspection["State"]["Health"]["Status"] != "healthy":
                time.sleep(2)
                inspection = docker_client.api.inspect_container(self.__docker_container.id)
            print("Container healthy.", file=sys.stderr)
        else:
            time.sleep(2)

    def execute_command(self, command):
        if type(command) == str:
            command = ["bash", "-c", command]

        exec_run_result = self.__docker_container.exec_run(command, demux=True)

        result = dict()
        result["exit-code"] = exec_run_result.exit_code
        if exec_run_result.output[0]:
            result["output"] = exec_run_result.output[0].decode("utf-8").strip()
        else:
            result["output"] = ""
        if exec_run_result.output[1]:
            result["error"] = exec_run_result.output[1].decode("utf-8").strip()
        else:
            result["error"] = ""

        return result


class KubernetesTestEnvironment(TestEnvironment):
    def __init__(self, pod):
        super().__init__()
        self.__pod = pod

    def __enter__(self):
        super().__enter__()
        kubernetes_api.create_namespaced_pod(
            self.__pod.arguments["metadata"]["namespace"],
            self.__pod.arguments
        )
        self.__wait_pod_ready()

    def __exit__(self, type, value, traceback):
        kubernetes_api.delete_namespaced_pod(
            self.__pod.arguments["metadata"]["name"],
            self.__pod.arguments["metadata"]["namespace"],
            grace_period_seconds=2
        )
        self.__wait_pod_deleted()
        super().__exit__(type, value, traceback)

    def __pod_is_ready(self):
        try:
            pod_info = kubernetes_api.read_namespaced_pod(
                self.__pod.arguments["metadata"]["name"],
                self.__pod.arguments["metadata"]["namespace"]
            )
        except ApiException:
            return False
        if not pod_info.to_dict()["status"]["conditions"]:
            return False
        for condition in pod_info.to_dict()["status"]["conditions"]:
            if condition["type"] == "Ready":
                if condition["status"] == "True":
                    return True
                elif condition["status"] == "False":
                    return False
                else:
                    raise NotImplementedError
        return False

    def __wait_pod_deleted(self):
        print("\nWaiting for Pod to be deleted... ", end="", file=sys.stderr, flush=True)
        try:
            while True:
                kubernetes_api.read_namespaced_pod(
                    self.__pod.arguments["metadata"]["name"],
                    self.__pod.arguments["metadata"]["namespace"]
                )
                time.sleep(2)
        except ApiException:
            print("Pod deleted.", file=sys.stderr)

    def __wait_pod_ready(self):
        print("\nWaiting for Pod to be ready... ", end="", file=sys.stderr, flush=True)
        while not self.__pod_is_ready():
            time.sleep(2)
        print("Pod ready.", file=sys.stderr)

    def execute_command(self, command):
        if type(command) == str:
            command = ["bash", "-c", command]

        exec_stream = stream(
            kubernetes_api.connect_get_namespaced_pod_exec,
            self.__pod.arguments["metadata"]["name"],
            self.__pod.arguments["metadata"]["namespace"],
            command=command,
            stderr=True, stdin=True,
            stdout=True, tty=False,
            _preload_content=False
        )
        exec_stream.run_forever(timeout=60)

        result = dict()
        if exec_stream.peek_stdout():
            result["output"] = exec_stream.read_stdout()
        if exec_stream.peek_stderr():
            result["error"] = exec_stream.read_stderr()
        error = yaml.full_load(exec_stream.read_channel(ERROR_CHANNEL))
        if error["status"] == "Success":
            result["exit-code"] = 0
        else:
            for cause in error["details"]["causes"]:
                if cause["reason"] == "ExitCode":
                    result["exit-code"] = int(cause["message"])
                    break

        exec_stream.close()

        return result
