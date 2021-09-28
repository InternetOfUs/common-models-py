import anybadge
import yaml
from yaml import Loader
import subprocess
import os
import os.path
import re

# This script is responsible for the creation of custom badges.
# In particular, it supports the creation of the following badges:
#   - ansible role versions
#   - git submodule versions
#   - pip package versions


dir_path = os.path.dirname(os.path.realpath(__file__))


def create_badge(label: str, value: str):
    color = "red"
    if re.match("^([0-9]+\.[0-9]+\.[0-9]+)$", value):
        color = "green"
    elif re.match("^([0-9]+\.[0-9]+\.[0-9]+)-([a-z]+)([\-0-9]+)?$", value):
        color = "yellow"


    badge = anybadge.Badge(label, value, default_color=color)
    badge.write_badge(f"{label}.svg", overwrite=True)


# Ansible role version badges.
# These are created by parsing requirements.yml files.


def badges_for_ansible_requirements(file_path):
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            res = yaml.load(f, Loader=Loader)

            for role in res["roles"]:
                if role["name"] == "uh.project_template" or role["name"] == "uh.project-template":
                    print(" - Creating [project-template] badge")
                    create_badge("template", role["version"])
                elif role["name"] == "uh.deploy-docker-service":
                    print(" - Creating [deploy-docker-service] badge")
                    create_badge("deploy", role["version"])
                else:
                    print(" - Nothing to to for role [%s]" % role["name"])


print("+ Creating Ansible role badges")

requirement_paths = [
    f"{dir_path}/../requirements.yml",
    f"{dir_path}/../deployment/requirements.yml"
]
for requirement_path in requirement_paths:
    badges_for_ansible_requirements(requirement_path)


# Pip package version badges.
# These are created by parsing the requirements.txt file.

print("+ Creating pip package badges")

uhopper_pip_libraries = [
    "uhopper-hubspot",
    "uhopper-utils",
    "uhopper-mysql",
    "uhopper-mqtt",
    "uhopper-elasticsearch",
    "uhopper-alert",
    "uhopper-language",
    "uhopper-chatbot",
    "uhopper-rule-engine",
    "wenet-common"
]

if os.path.isfile(f"{dir_path}/../requirements.txt"):
    with open(f"{dir_path}/../requirements.txt", "r", encoding="utf-8") as f:
        requirements = f.read()
        x = re.findall("([a-zA-Z\-0-9]+)([=~><]+)?([a-zA-Z0-9.\-]+)?", requirements)
        for library, eq, version in x:
            if library in uhopper_pip_libraries:
                if not version:
                    version = "unknown"
                print(f" - Creating [{library}] badge")
                create_badge(library, version)
else:
    print("Skipping requirements.txt, file not found")


# git submodule badges.
# These are created

print("+ Creating git submodule badges")

bashCommand = "git submodule status --recursive"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

if not error:
    x = re.findall(" ([a-z\-]+)( [\(\)0-9a-zA-Z.\-]+)?", str(output))
    for module, module_version in x:
        module_version = module_version.replace(" ", "").replace("(", "").replace(")", "")
        if module_version == "" or not module_version:
            module_version = "unstable"
        print(f" - Creating [{module}] badge with version [{module_version}]")
        create_badge(module, module_version)
else:
    print(f"Error while identifying submodules: {error}")
    exit(1)
