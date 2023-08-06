from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.readlines()

with open('README.md', "r") as f:
    long_description = f.read()

setup(
    name='ipwg',
    version='0.1.0',
    author='Ian Laird',
    author_email='irlaird@gmail.com',
    url='https://github.com/en0/ipwg',
    keywords=['password'],
    description='Password Generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=['ipwg'],
    entry_points={
        'console_scripts': [
            'ipwg = ipwg.entry:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
)
