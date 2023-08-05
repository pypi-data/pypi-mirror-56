#!/usr/bin/env python

from distutils.core import setup, Extension

#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup

setup(name="lthread",
      version="1.0.2",
      description="lightweight threads in Python using extended generators",
      author="Katie Stafford",
      author_email="katie@ktpanda.org",
      license="MIT License",
      packages=["lthread"],
      classifiers = [
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        ]

     )
