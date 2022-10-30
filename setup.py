from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    """
    This function will return list of requirements
    """
    """
    Write a code to read requirements.txt file and append each requirements in requirement_list variable.
    """
    with open("requirements.txt", 'r') as f:
        lst = f.read().splitlines()
    lst = [lib for lib in lst if not (lib.strip() == '' or lib.strip() == '-e .')]
    return lst

setup(
    name="sensor",
    version="0.0.1",
    author="Devendra_Jakhmola",
    author_email="devjakhmola1990@gmail.com",
    packages = find_packages(),
    install_requires=get_requirements(),#["pymongo==4.2.0"],
)

