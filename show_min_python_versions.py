#!/usr/bin/env python3
import json
import sys
import requests
import toml


def get_python_version(package_name: str):
    """
    Get the python version of a package from pypi.org
    :param package_name: name of the package
    :return: python version of the package
    """
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data["info"]["requires_python"]
    else:
        response.raise_for_status()


def get_packages(file_name: str):
    poetry_file = toml.load(file_name)
    packages = poetry_file["tool"]["poetry"]["dependencies"].keys()
    return [
        (package, get_python_version(package))
        for package in packages
        if package != "python"
    ]


if __name__ == "__main__":
    for package_name, python_version in get_packages(sys.argv[1]):
        print(f"{package_name}: {python_version}")
