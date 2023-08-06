import os
import tempfile

####################################################
# Note this file is for variables only, no imports
# except standard libs where necessary
# as its imported for docs gen etc
####################################################

PROJECT_VERSION = "0.0.1"

PROJECT_SHORT = "ogt-py"
PROJECT_LONG = "ogt-py"

PROJECT_DESCRIPTION = "Python code that eats geotechcical data"
PROJECT_CONTACT = "ogt@daffodil.uk.com"

PROJECT_DOMAIN = "open-geotechnical.gitlab.io"
PROJECT_WWW = "http://open-geotechnical.gitlab.io/"
PROJECT_HOME = "https://gitlab.com/open-geotechnical/ogt-py"
PROJECT_ISSUES = "https://gitlab.com/open-geotechnical/ogt-py/issues"
PROJECT_API_DOCS = "http://open-geotechnical.gitlab.io/ogt-py"


def get_project_info():
    """
    :return: A `dict` with the project info
    """
    return dict(
        version=PROJECT_VERSION,
        short=PROJECT_SHORT,
        long=PROJECT_LONG,
        description=PROJECT_DESCRIPTION,
        contact=PROJECT_CONTACT,
        domain=PROJECT_DOMAIN,
        www=PROJECT_WWW,
        home=PROJECT_HOME,
        issues=PROJECT_ISSUES,
        api_docs=PROJECT_API_DOCS
    )


HERE_PATH = os.path.abspath(os.path.dirname(__file__))

PROJECT_ROOT_PATH = os.path.abspath(os.path.join(HERE_PATH, ".."))
"""Root dir of the project"""

TEMP_DIR = tempfile.gettempdir()
TEMP_WORKSPACE = os.path.join(TEMP_DIR, "temp_workspace")
"""Path to temporary directory"""

EXAMPLES_DIR = os.path.join(TEMP_DIR, "example_files")
"""Path to examples folder"""

USER_HOME = os.path.expanduser("~")
"""Path to users home dir"""

USER_TEMP = os.path.join(USER_HOME, "ogt-workspace")
"""Path to open-getechnical cache directory"""

FORMATS = ["json", "geojson", "yaml", "xlsx", "ags4", "ags"]
"""Formats allowed, depending on libs installed"""


class CELL_COLORS:
    empty_bg = "#666666"
    ok_bg = "#E7FFDC"
    err_bg = "#FFC5C5"
    warn_bg = "#F7F89F"


class COLOR:
    required = "purple"
