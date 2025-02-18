# switchbot-mqtt - MQTT client controlling SwitchBot button & curtain automators,
# compatible with home-assistant.io's MQTT Switch & Cover platform
#
# Copyright (C) 2020 Fabian Peter Hammerle <fabian@hammerle.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pathlib

import setuptools

_REPO_URL = "https://github.com/fphammerle/switchbot-mqtt"

setuptools.setup(
    name="switchbot-mqtt",
    use_scm_version={
        # > AssertionError: cant parse version docker/0.1.0-amd64
        # https://github.com/pypa/setuptools_scm/blob/master/src/setuptools_scm/git.py#L15
        "git_describe_command": "git describe --dirty --tags --long --match v*"
    },
    packages=setuptools.find_packages(),
    description="MQTT client controlling SwitchBot button & curtain automators, "
    # https://www.home-assistant.io/integrations/switch.mqtt/
    "compatible with home-assistant.io's MQTT Switch & Cover platform",
    long_description=pathlib.Path(__file__)
    .parent.joinpath("README.md")
    .read_text(encoding="utf8"),
    long_description_content_type="text/markdown",
    author="Fabian Peter Hammerle",
    author_email="fabian@hammerle.me",
    url=_REPO_URL,
    project_urls={"Changelog": _REPO_URL + "/blob/master/CHANGELOG.md"},
    license="GPLv3+",
    keywords=[
        "IoT",
        "automation",
        "bluetooth",
        "button",
        "click",
        "cover",
        "curtain",
        "home-assistant.io",
        "home-automation",
        "mqtt",
        "press",
        "push",
        "switchbot",
    ],
    classifiers=[
        # https://pypi.org/classifiers/
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        # .github/workflows/python.yml
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Home Automation",
    ],
    entry_points={"console_scripts": ["switchbot-mqtt = switchbot_mqtt._cli:_main"]},
    # >=3.6 variable type hints, f-strings, typing.Collection & * to force keyword-only arguments
    # >=3.7 postponed evaluation of type annotations (PEP563) & dataclass
    python_requires=">=3.7",
    install_requires=[
        # >=0.10.0 for SwitchbotCurtain.{update,get_position}
        # >=0.9.0 for SwitchbotCurtain.set_position
        "PySwitchbot>=0.15.0",
        "asyncio-mqtt>=0.12.0",
    ],
    setup_requires=["setuptools_scm"],
    tests_require=["pytest"],
)
