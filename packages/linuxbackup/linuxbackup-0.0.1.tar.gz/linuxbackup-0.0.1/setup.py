import setuptools
import sys
argv=sys.argv
sys.argv=['','__setup__']
import linuxbackup
sys.argv=argv
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="linuxbackup",
    version=linuxbackup.VERSION,
    author="Tianyi Chen",
    author_email="",
    description="Backup and restore for linux",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: POSIX :: Linux",
    ],
)