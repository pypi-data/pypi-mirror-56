import os
import logging

from flambe.const import FLAMBE_GLOBAL_FOLDER
from flambe.experiment.wording import print_extensions_cache_size_warning

logger = logging.getLogger(__name__)


MB = 2**20
WARN_LIMIT_MB = 100


def get_folder_size_MB(path: str) -> float:
    """Return the size of a folder in MB.

    Parameters
    ----------
    path: str
        The path to the folder

    Returns
    -------
    float
        The size in MB

    """
    accum = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp) and not os.path.islink(fp):
                accum += os.path.getsize(fp)
    return accum / MB


def check_system_reqs() -> None:
    """Run system checks and prepare the system before a run.

    This method should:
        * Create folders, files that are needed for flambe
        * Raise errors in case requirements are not met. This should
        run under the SafeExecutionContext, so errors will be handled
        * Warn the user in case something needs attention.

    """
    # Create the flambe folder if it does not exist
    if not os.path.exists(FLAMBE_GLOBAL_FOLDER):
        os.mkdir(FLAMBE_GLOBAL_FOLDER)

    # Check if extensions folder is getting big
    extensions_folder = os.path.join(FLAMBE_GLOBAL_FOLDER, "extensions")
    if get_folder_size_MB(extensions_folder) > WARN_LIMIT_MB:
        logger.warning(f"Extensions folder exceeds {WARN_LIMIT_MB} MB")
        print_extensions_cache_size_warning(extensions_folder, WARN_LIMIT_MB)
