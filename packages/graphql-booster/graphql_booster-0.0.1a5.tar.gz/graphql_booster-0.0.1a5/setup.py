from setuptools import setup, find_packages
from setuptools.command.install import install
from graphql_booster.install import setup_gateway


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        setup_gateway()


setup(
    name="graphql_booster",
    version="0.0.1a5",
    author="jimtheplant",
    author_email="jimtheplant1@gmail.com",
    packages=find_packages(),
    python_requires=">=3.7",
    cmdclass={
        "install": PostInstallCommand
    },
    include_package_data=True,
    install_requires=[
        "ariadne>=0.7",
        "uvicorn",
        "nodeenv"
    ]
)
