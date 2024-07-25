from setuptools import setup, find_packages
from typing import List

def get_requirements(path: str) -> List[str]:
    with open(path, 'r') as file:
        requirements = [req.replace('\n', '') for req in file.readlines()]
        
    if '-e .' in requirements:
        requirements.remove('-e .')
    return requirements


setup(
    name='TextToVideo',
    version='0.0.1',
    author='Dinesh',
    author_email='dineshsai7728@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)