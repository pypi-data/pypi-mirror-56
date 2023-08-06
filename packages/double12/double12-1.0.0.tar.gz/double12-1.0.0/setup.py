#coding=utf-8

import os.path
from setuptools import setup
from setuptools.command.install import install

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as f:
    README = f.read()


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        try:
            import webbrowser
            webbrowser.open("https://www.pycourses.com/double12")
        except:
            pass
        print("\n")
        print("##############################################")
        print("#          看看爱湃森最新课程优惠喽          #")
        print("##############################################")
        print("\n")
        install.run(self)


setup(
    name="double12",
    version="1.0.0",
    description="double12",
    long_description=README,
    long_description_content_type="text/markdown",
    py_modules=['double12'],
    url="https://www.pycourses.com/double12",
    author="IPaisen",
    author_email="admin@pycourses.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
    include_package_data=False,
    install_requires=[],
    entry_points={"console_scripts": ["double12=double12:main"]},
)
