from setuptools import find_packages
from setuptools import setup


with open("README.md") as readme_file:
    readme = readme_file.read()

install_requirements = ["aiohttp"]

setup_requirements = ["setuptools_scm"]

setup(
    author="Nikhil Dhandre",
    author_email="nik.digitronik@live.com",
    classifiers=[
        "Natural Language :: English",
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Communications :: Chat",
        "Topic :: Communications :: Chat :: Internet Relay Chat",
    ],
    version="0.1",
    python_requires=">=3.6",
    description="IRC bot",
    entry_points={"console_scripts": ["ircbot=src:main"]},
    install_requires=install_requirements,
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    setup_requires=setup_requirements,
    keywords="bot-irc",
    name="bot-irc",
    packages=find_packages(include=["bot-irc"]),
    url="https://github.com/pythonpune/bot-irc",
    license="GPLv3.0",
    zip_safe=False,
)
