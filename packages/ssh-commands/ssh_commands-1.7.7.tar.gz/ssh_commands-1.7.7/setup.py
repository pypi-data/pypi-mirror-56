from os.path import dirname, abspath, join

import os
import setuptools

cur_dir = abspath(dirname(__file__))

with open(join(cur_dir, "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ssh_commands",
    version=os.getenv("SSH_COMMANDS_VERSION", "1.0.0"),
    author="Donii Sergii",
    author_email="s.donii@infomir.com",
    description="SSH commands and gitlab helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.infomir.dev/backend/python-packages/commands-helper",
    packages=setuptools.find_packages(),
    include_package_data=True,
    scripts=[
        'ssh_commands/ssh-expand-password',
        'ssh_commands/ssh-expand-password-sleep',
    ],
    install_requires=["pyyaml", "cryptography", "python-gitlab"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
