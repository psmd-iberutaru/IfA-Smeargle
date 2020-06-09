
"""
This is the setup file of the code base. All needed configurations
for the setup of this library to other systems should be contained
here.
"""

from setuptools import setup, find_packages


setup(
    name="IfA_Smeargle",
    version="0.1.1",
    packages=find_packages(),

    # These are all of the dependencies of this project/library.
    install_requires=["astropy", "configobj >= 5.0", "matplotlib", "numpy", 
                      "pandas","pylint", "pytest", "scipy", "setuptools",
                      "Sphinx", "sympy"],

    package_data={
        # Include data text, configuration files and specifications.
        "": ["*.md", "*.txt", "*.ini", "*.spec"]
    },

    # metadata to display on PyPI
    author="Sparrow",
    author_email="kemerson@hawaii.edu",
    description="Software reduction package for LmAPD and SAPHIRA arrays.",
    keywords="LmAPD SAPHIRA Smeargle IfA_Smeargle",
    url="https://github.com/psmd-iberutaru/IfA_Smeargle",
    project_urls={
        "Bug Tracker":"https://github.com/psmd-iberutaru/IfA_Smeargle/issues",
        "Documentation":"https://github.com/psmd-iberutaru/IfA_Smeargle/wiki",
        "Source Code":"https://github.com/psmd-iberutaru/IfA_Smeargle",
    }
)