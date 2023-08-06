from setuptools import setup, find_packages
import re

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

version = ""
with open("dglbots/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("version is not set")

setup(
    name="dgl-bots.py",
    author="Piyush Bhangale",
    url="https://github.com/discord-gl/dgl-bots.py",
    project_urls={"Issue tracker": "https://github.com/discord-gl/dgl-bots.py/issues",},
    version=version,
    packages=["dglbots"],
    license="MIT",
    description="A python wrapper for https://bots.discord.gl",
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.5.3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
