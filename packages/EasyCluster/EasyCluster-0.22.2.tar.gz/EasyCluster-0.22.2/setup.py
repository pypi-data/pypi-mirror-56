#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup

from easycluster import VERSION

setup(name="EasyCluster",
      version=VERSION,
      description="EasyCluster: a remote execution/clustering module for Python",
      author="Katie Stafford",
      author_email="katie@ktpanda.org",
      url="http://pypi.python.org/pypi/EasyCluster",
      license="MIT License",
      packages=["easycluster"],
      entry_points = {
        'console_scripts': ['easycluster = easycluster.server:server_main'],
      },
      classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: System :: Clustering",
        "Topic :: System :: Distributed Computing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        ]
     )
