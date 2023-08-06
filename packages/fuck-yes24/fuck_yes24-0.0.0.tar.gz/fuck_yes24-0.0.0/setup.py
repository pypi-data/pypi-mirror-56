from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='fuck_yes24',
    packages=['fuck_yes24py'],
    description='',
    author='carpedm20',
    install_requires=requirements,
    scripts=['fuck_yes24'],
)
