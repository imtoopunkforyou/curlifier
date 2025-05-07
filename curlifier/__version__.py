# ░█████╗░██╗░░░██╗██████╗░██╗░░░░░██╗███████╗██╗███████╗██████╗░
# ██╔══██╗██║░░░██║██╔══██╗██║░░░░░██║██╔════╝██║██╔════╝██╔══██╗
# ██║░░╚═╝██║░░░██║██████╔╝██║░░░░░██║█████╗░░██║█████╗░░██████╔╝
# ██║░░██╗██║░░░██║██╔══██╗██║░░░░░██║██╔══╝░░██║██╔══╝░░██╔══██╗
# ╚█████╔╝╚██████╔╝██║░░██║███████╗██║██║░░░░░██║███████╗██║░░██║
# ░╚════╝░░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝

from importlib.metadata import PackageMetadata, metadata
from pathlib import Path
from typing import Final

pkg_data: PackageMetadata = metadata(str(Path(__file__).parent.name))

NAME: Final[str] = pkg_data['Name']
"""Package name."""

VERSION: Final[str] = pkg_data['Version']
"""Package version."""

AUTHOR: Final[str] = pkg_data['Author']
"""Package author."""

AUTHOR_EMAIL: Final[str] = pkg_data['Author-email']
"""Package author e-mail."""

LICENSE: Final[str] = pkg_data['License']
"""Package license."""


def get_package_information() -> dict[str, str]:
    """Short info about package."""
    pkg_info = {
        'name': NAME,
        'version': VERSION,
        'author': AUTHOR,
        'author_email': AUTHOR_EMAIL,
        'license': LICENSE,
    }

    return pkg_info
