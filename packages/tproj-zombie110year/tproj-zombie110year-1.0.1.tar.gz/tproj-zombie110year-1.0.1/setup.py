from pathlib import Path

from setuptools import setup

from tproj import __version__

setup(
    author="zombie110year",
    author_email="zombie110year@outlook.com",
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    description="管理项目模板",
    entry_points = {
        "console_scripts": [
            "tproj = tproj.cli:main",
        ],
    },
    install_requires=[
        "pyyaml>=5.0"
    ],
    license="MIT",
    long_description=Path("README.md").read_text("utf-8"),
    long_description_content_type="text/markdown",
    maintainer="zombie110year",
    maintainer_email="zombie110year@outlook.com",
    name="tproj-zombie110year",
    packages=["tproj", "tproj.utils"],
    platforms=["win32", "linux"],
    python_requires='>=3.7',
    url="https://github.com/zombie110year/tproj-py/",
    version=__version__,
)
