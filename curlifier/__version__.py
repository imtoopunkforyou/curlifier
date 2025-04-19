# ░█████╗░██╗░░░██╗██████╗░██╗░░░░░██╗███████╗██╗███████╗██████╗░
# ██╔══██╗██║░░░██║██╔══██╗██║░░░░░██║██╔════╝██║██╔════╝██╔══██╗
# ██║░░╚═╝██║░░░██║██████╔╝██║░░░░░██║█████╗░░██║█████╗░░██████╔╝
# ██║░░██╗██║░░░██║██╔══██╗██║░░░░░██║██╔══╝░░██║██╔══╝░░██╔══██╗
# ╚█████╔╝╚██████╔╝██║░░██║███████╗██║██║░░░░░██║███████╗██║░░██║
# ░╚════╝░░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝

from importlib.metadata import PackageMetadata, metadata
from pathlib import Path
from typing import Final

pkg_name: Final[str] = str(Path(__file__).parent.name)
pkg_data: PackageMetadata = metadata(pkg_name)

NAME: Final[str] = pkg_data['Name']
VERSION: Final[str] = pkg_data['Version']
AUTHOR: Final[str] = pkg_data['Author']
AUTHOR_EMAIL: Final[str] = pkg_data['Author-email']
LICENSE: Final[str] = pkg_data['License']


def get_package_information() -> dict[str, str]:
    pkg_info = {
        'name': NAME,
        'version': VERSION,
        'author': AUTHOR,
        'author_email': AUTHOR_EMAIL,
        'license': LICENSE,
    }

    return pkg_info
