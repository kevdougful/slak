from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install


def _find_or_create_dotdir(dotdir_name):
    """Looks for an existing dotdir directory and creates one if not found"""
    dotdir = Path.home().joinpath(dotdir_name)
    if not Path(dotdir).exists():
        # Create dotdir and empty .env file
        dotdir.mkdir()
        dotdir.joinpath(".env").touch()


class PostDevelopCommand(develop):
    """Post-installation script for development mode"""
    def run(self):
        # Find or create dotdir
        _find_or_create_dotdir(".slak")
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation script for installation mode"""
    def run(self):
        # Find or create dotdir
        _find_or_create_dotdir(".slak")
        install.run(self)


setup(
    name="slak",
    version="0.1.0",
    py_modules=["emoji"],
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=["Click"],
    entry_points={
        "console_scripts": [
            "slak-migrate=emoji.cli:migrate",
            "slak-emoji=emoji.cli:uri",
        ]
    },
    cmdclass={
        "develop": PostDevelopCommand,
        "install": PostInstallCommand,
    },
)