
"""
This is the setup file of the code base. All needed configurations
for the setup of this library to other systems should be contained
here.
"""

from setuptools import setup, find_packages


# These are the setup parameters, in global form in the event that
# other parts of the this program needs it.
NAME = 'IfA_Smeargle'
VERSION = '0.2.0'

DEPENDENCIES = ['astropy', 'configobj >= 5.0', 'matplotlib', 'numpy', 
                'pandas','pylint', 'pytest', 'scipy', 'setuptools',
                'Sphinx', 'sympy']

ENTRY_POINTS =  {
    "console_scripts": ["ifa_smeargle = ifa_smeargle:run_entry"]}

AUTHOR = 'Sparrow'
AUTHOR_EMAIL = 'kemerson@hawaii.edu'
DESCRIPTION = 'Software reduction package for LmAPD and SAPHIRA arrays.'
KEYWORDS = ['LmAPD', 'SAPHIRA', 'Smeargle', 'IfA_Smeargle']
URL = 'https://github.com/psmd-iberutaru/IfA_Smeargle'
BUG_URL = 'https://github.com/psmd-iberutaru/IfA_Smeargle/issues'
DOCUMENTATION_URL = 'https://github.com/psmd-iberutaru/IfA_Smeargle/wiki'
SOURCE_URL = 'https://github.com/psmd-iberutaru/IfA_Smeargle'

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),

    # These are all of the dependencies of this project/library.
    install_requires=DEPENDENCIES,

    package_data={
        # Include data text, configuration files and specifications.
        "": ["*.md", "**/*.md", "**/**/*.md",
             "*.txt", "**/*.txt", "**/**/*.txt",
             "*.ini", "**/*.ini", "**/**/*.ini",
             "*.spec", "**/*.spec", "**/**/*.spec"]
    },

    entry_points=ENTRY_POINTS,

    # metadata to display on PyPI
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    keywords=KEYWORDS,
    url=URL,
    project_urls={
        "Bug Tracker":BUG_URL,
        "Documentation":DOCUMENTATION_URL,
        "Source Code":SOURCE_URL,
    }
)