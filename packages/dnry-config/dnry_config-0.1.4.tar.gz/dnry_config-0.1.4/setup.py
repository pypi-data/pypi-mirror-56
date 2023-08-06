from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.readlines()

with open('README.md', "r") as f:
    long_description = f.read()

setup(
    name='dnry_config',
    version='0.1.4',
    author='Ian Laird',
    author_email='irlaird@gmail.com',
    url='https://github.com/en0/dnry-config',
    keywords=['config', 'configuration', 'dnry'],
    description='Multi-source config library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=[
        'dnry.config',
        'dnry.config.arg',
        'dnry.config.delegate',
        'dnry.config.environ',
        'dnry.config.in_memory',
        'dnry.config.yaml',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=requirements,
)
