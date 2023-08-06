import os
import setuptools

dir_path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(dir_path, "test_containers/help.txt"), "r") as f:
    help_text = f.read()

setuptools.setup(
    name="test-containers",
    version="0.1.3",
    author="Alassane Ndiaye",
    author_email="alassane.ndiaye@gmail.com",
    description=help_text,
    long_description="https://github.com/AlassaneNdiaye/test-containers",
    long_description_content_type="text/markdown",
    url="https://github.com/AlassaneNdiaye/test-containers",
    packages=setuptools.find_packages(),
    install_requires=[
        "docker",
        "kubernetes",
        "PyYAML"
    ]
)
