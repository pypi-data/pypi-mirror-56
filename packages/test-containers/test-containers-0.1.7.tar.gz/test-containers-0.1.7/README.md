# test-containers

[![CircleCI](https://circleci.com/gh/AlassaneNdiaye/test-containers.svg?style=svg)](https://circleci.com/gh/AlassaneNdiaye/test-containers)

test-containers is a program for testing pods and containers on the Docker and Kubernetes platforms
using yaml files for configuration.

## Getting Started

### Prerequisites

* [pip](https://pip.pypa.io/en/stable/)

* [Python](https://www.python.org/)

* [venv](https://docs.python.org/3/library/venv.html)

### Installion

For installation, follow these steps.

Create a Python virtual environment:

```
python -m venv environment
```

Activate the virtual environment:

```
source environment/bin/activate
```

Install the library.

```
pip install test-containers
```

The library is now ready for use.
Assuming you have a valid configuration file `tests.yaml`, you can run your tests using:

```
python -m test_containers --config tests.yaml
```

### Usage

The general syntax for writing tests is:

```
- application:
    name: example name
    type: docker # Specify on what platform containers are run.
    arguments: # Arguments used for running the application.
      image: httpd:2.4
      ...
  tests:
  - name: example test name
    command: command arguments
    environment: external # Environment where the command will be run.
    exit-code: 0 # Verify the command exit code. Other test options are mentioned further below.
    ...
  - name: second test name
    ...
- application:
    name: second application name
    ...
```

#### Platforms

The supported platforms (application types) are Docker and Kubernetes.

Example Docker application:

```
- application:
    name: test-container
    type: docker
    arguments:
      image: httpd:2.4
      auto_remove: True
      ports:
        80: 80
  tests:
  - name: test the webserver is accessible locally
    command: wget http://localhost/
    environment: external
    exit-code: 0
```

Example Kubernetes application:

```
- application:
    name: test-pod
    type: kubernetes
    arguments:
      apiVersion: v1
      kind: Pod
      metadata:
        name: httpd
        namespace: default
      spec:
        containers:
        - name: httpd
          image: httpd:2.4
        hostNetwork: true
  tests:
  - name: test the webserver is accessible locally
    command: wget http://localhost/
    environment: external
    exit-code: 0
```

Docker applications use the same interface as the Python Docker SDK for the client.containers.run command.
A list of all supported arguments is available in the
[official documentation](https://docker-py.readthedocs.io/en/stable/containers.html).

Kubernetes applications are written using the standard yaml syntax.

#### Environment

Commands can be run from either the machine hosting the container/pod using the `external` keyword 
or from inside the container/pod using the `internal` keyword.

The `external` keyword is useful for testing how the application interacts with clients.
The `internal` keyword is useful for testing the application internals.

For example:

```
- application:
    name: test-pod-1
    type: kubernetes
    arguments:
      apiVersion: v1
      kind: Pod
      metadata:
        name: httpd
        namespace: default
      spec:
        containers:
        - name: httpd
          image: httpd:2.4
        hostNetwork: true
  tests:
  - name: test the webserver can be used by clients to retrieve content
    command: wget http://localhost/
    environment: external
    exit-code: 0
- application:
    name: test-pod-2
    type: kubernetes
    arguments:
      apiVersion: v1
      kind: Pod
      metadata:
        name: busybox
        namespace: default
      spec:
        containers:
        - name: busybox
          image: busybox:1.28
          command:
          - sleep
          - "3600"
  tests:
  - name: test Pod DNS is working correctly
    command:
    - nslookup
    - kubernetes.default
    environment: internal
    exit-code: 0
    expected-output: kube-dns.kube-system.svc
```

#### Supported Tests

Following is a list of features that can be tested with this library.

Test commands have the right exit code:

```
- application:
    name: test-container
    type: docker
    arguments:
      image: httpd:2.4
  tests:
  - name: test name
    command: echo test
    environment: internal
    exit-code: 0
```

Test a regular expression is present or missing from standard output or standard error:

```
- application:
    name: test-container
    type: docker
    arguments:
      image: httpd:2.4
  tests:
  - name: test name
    command: bash -c "echo making a test; echo making a test 1>&2"
    environment: internal
    expected-output: .*test.*
    excluded-output: undesirable pattern
    expected-error: .*test.*
    excluded-error: undesirable pattern
```

Test a file exists:

```
- application:
    name: test-container
    type: docker
    arguments:
      image: httpd:2.4
  tests:
  - name: test name
    command: touch file
    environment: internal
    files:
    - path: "file"
      exists: True
```

Test content is present or missing in a file:

```
- application:
    name: test-container
    type: docker
    arguments:
      image: httpd:2.4
  tests:
  - name: test name
    command: echo "content of the file">file
    environment: internal
    files:
    - path: file
      expected-content: .*content.*
      excluded-content: undesirable pattern
```

#### Additional Examples

Other examples can be found in sister projects:

* [dhcp-server](https://github.com/AlassaneNdiaye/dhcp-server/tree/master/tests)
* [os-web-server](https://github.com/AlassaneNdiaye/os-web-server/tree/master/tests)
* [pxe-server](https://github.com/AlassaneNdiaye/pxe-server/tree/master/tests)

## Design and Benefits

If you want to know how and why this library was made, take a look at the
[design document](design.md).

## Authors

* **Alassane Ndiaye** - [AlassaneNdiaye](https://github.com/AlassaneNdiaye)

## License

This project is licensed under the GNU General Public License v3.0 -
see the [LICENSE.txt](LICENSE.txt) file for details.
