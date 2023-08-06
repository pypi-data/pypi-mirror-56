#!/usr/bin/env python -e

"""
DOCSTRING IS HERE
"""

from platform import system

user_platform = system()

if user_platform == "Windows":

    from .windows import Mixer

elif user_platform == "Darwin":

    from .darwin import Mixer

elif user_platform == "Linux":

    from .linux import Mixer

else:

    raise Exception(
        "Sorry, your platform isn't supported yet by cpmixer ({})".format(
            user_platform
        )
    )

__metadata_version__ = "2.1"
__name__ = "cpmixer"
__version__ = "0.8.0"
__summary__ = "Cross-platform module for controlling audio mixers"
__description__ = "Cross-platform module for controlling audio mixers"
__description_content_type__ = "text/markdown"
__keywords__ = (
    "media workflow volume sound modular cross-platform"
)  # A list of additional keywords to be used to assist searching for the distribution in a larger catalog.
__homepage__ = "https://github.com/drtexx/{}".format(__name__)
__author__ = "Denver Pallis"
__author_email__ = "DenverPallisProjects@gmail.com"
# __maintainer__ = "Denver Pallis" # should be omitted if it is identical to Author
# __maintainer_email__ = "DenverPallisProjects@gmail.com" # should be omitted if it is identical to Author
__license__ = "GPLv3+"
__classifiers__ = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Environment :: MacOS X",
    "Environment :: Win32 (MS Windows)",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Natural Language :: English",
    "Operating System :: MacOS",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Topic :: Multimedia",
    "Topic :: Scientific/Engineering :: Human Machine Interfaces",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries",
]
__requires_dist__ = ["pyalsaaudio"]  # requirements
__setup_requires__ = ["wheel", "setuptools"]
__requires_python__ = [">=3"]  # required python version
__requires_external__ = []  # external requirements
__project_urls__ = {  # a browsable URL for the project and a label for it, separated by a comma
    "Bug Reports": "https://github.com/drtexx/{}/issues".format(__name__),
    "Source": "https://github.com/drtexx/{}".format(__name__),
    "Funding": "https://paypal.me/denverpallis",
    "Docs": "https://{}.readthedocs.io".format(__name__),
}
__exclude_packages__ = ["contrib", "docs", "tests"]

# metadata standard: https://packaging.python.org/specifications/core-metadata/
