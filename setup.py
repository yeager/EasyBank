"""Setup script for EasyBank."""

from setuptools import find_packages, setup

setup(
    name="easybank",
    version="1.0.0",
    description="Visuell budgetapp med piktogram för personer med intellektuella funktionshinder",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="EasyBank Team",
    license="GPL-3.0",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[
        "PyGObject>=3.42",
    ],
    entry_points={
        "console_scripts": [
            "easybank=easybank.app:main",
        ],
    },
    data_files=[
        ("share/applications", ["easybank.desktop"]),
        ("share/locale/sv/LC_MESSAGES", ["po/sv/LC_MESSAGES/easybank.po"]),
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Swedish",
        "Programming Language :: Python :: 3",
        "Topic :: Office/Business :: Financial",
    ],
)
