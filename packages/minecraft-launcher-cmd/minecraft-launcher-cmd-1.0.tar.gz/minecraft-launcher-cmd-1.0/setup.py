#!/usr/bin/env python3
from setuptools import find_packages, setup

with open("README.md","r",encoding="utf-8") as f:
    description = f.read()

setup(name='minecraft-launcher-cmd',
    version='1.0',
    description='Start Minecraft from commandline',
    long_description=description,
    long_description_content_type='text/markdown',
    author='JakobDev',
    author_email='jakobdev@gmx.de',
    url='https://gitlab.com/JakobDev/minecraft-launcher-cmd',
    python_requires='>=3.5',
    include_package_data=True,
    install_requires=[
        'minecraft-launcher-lib',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['minecraft-launcher-cmd = minecraft_launcher_cmd.minecraft_launcher_cmd:main']
    },
    license='BSD',
    keywords=['JakobDev','Minecraft','Mojang','launcher','minecraft-launcher','java'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Environment :: Other Environment',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Topic :: Games/Entertainment',
        'Operating System :: OS Independent',
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
 )

