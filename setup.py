"""Bricker - A Tetris-like brick game.
Copyright (C) 2017-2020  John Hyland
GNU GENERAL PUBLIC LICENSE Version 3"""

from setuptools import find_packages, setup


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name="PyCentipede",
    version="1.3.1",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    package_data={
        "": ["*.py", "*.txt", "*.png", "*.ttf"]
    },
    author="John Hyland",
    author_email="jonhyland@hotmail.com",
    description="A Tetris-like brick game.",
    keywords="game tetris pygame bricker brick",
    license='GNU',
    project_urls={
        "Source Code": "https://github.com/jon-hyland/bricker/"
    }
)
