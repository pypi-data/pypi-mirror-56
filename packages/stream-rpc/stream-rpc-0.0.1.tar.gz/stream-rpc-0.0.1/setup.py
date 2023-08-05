"""Пакет проекта."""
from setuptools import setup

setup(
    name="stream-rpc",
    packages=["stream_rpc"],
    version=open("VERSION").read().strip(),
    install_requires=["cryptography==2.8"],
    include_package_data=True,
    author="Andrew Burdyug",
    author_email="buran83@gmail.com",
    description="Stream RPC protocol with cryptography",
    url="https://github.com/AndrewBurdyug/stream-rpc",
    license="Copyright (c) 2019 Andrew Burdyug. All rights reserved.",
    keywords="stream rpc crypto",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Internet",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
    ],
)
