"""Setup script for realpython-reader"""

import os.path
from setuptools import setup
from setuptools.command.install import install

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        try:
            import webbrowser
            webbrowser.open("https://realpython.com/blackfriday")
        except:
            pass
        print("\n")
        print("##############################################")    
        print("#  Go to https://realpython.com/blackfriday  #")
        print("##############################################")
        print("\n")
        install.run(self)

# This call to setup() does all the work
setup(
    name="blackfriday",
    version="1.0.3",
    description="Black Friday",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://realpython.com/blackfriday",
    author="Real Python",
    author_email="info@realpython.com",
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
    packages=["blackfriday"],
    include_package_data=False,
    install_requires=[],
    entry_points={"console_scripts": ["blackfriday=blackfriday:main"]},
)
