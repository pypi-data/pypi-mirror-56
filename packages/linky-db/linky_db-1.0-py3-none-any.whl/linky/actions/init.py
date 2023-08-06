import logging
import shutil

from linky.actions import add
from linky.config import Config, read_conf
from linky.utils.path_utils import BASE_NAME, iter_linked_root, CONFIG_DIR_NAME


def init(root_path, overwrite_config=False):
    """
    Creates the base directory and moves everything else inside

    If there are already category dirs then the move will be followed by symlinking
     the contents of those category folders.

    :param root_path:
    :type root_path: Path
    :param overwrite_config: Whether a config in the link root
                              should overwrite the one in the base
    :type overwrite_config: bool
    """
    logger = logging.getLogger("init")
    if not root_path.is_dir():
        raise ValueError("Given path must be a directory")

    base_dir = root_path / BASE_NAME
    if base_dir.is_dir():
        raise ValueError("Given path has already been initialized")

    logger.info("Initializing...")
    base_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Base dir: %s", base_dir)

    # Try and read a config first (we need categories)
    config = _get_config_for_init(root_path, base_dir, overwrite_config)
    for root_entry, cat_tag in iter_linked_root(root_path, config):
        add(root_entry, base_dir, config, cat_tag)
    logger.info("Done...")


def _get_config_for_init(link_root, base_dir, overwrite_config):
    """
    Tries to read the config from the link root or base path.

    The one in the link will override an existing config in the base path.
    But that's only possible by passing @param overwrite_config


    @type link_root: Path
    @type base_dir: Path
    @type overwrite_config: bool
    @return: An initialized config if one was detected
    @rtype: Config
    """
    possible_config_dir = link_root / CONFIG_DIR_NAME
    config_dir = base_dir / CONFIG_DIR_NAME
    config = Config(base_dir)

    if possible_config_dir.is_dir():
        # Replace config if possible
        if config_dir.exists():
            if overwrite_config:
                shutil.rmtree(config_dir)
            else:
                raise ValueError("New configuration found. Pass --overwrite-config to supersede old config")
        shutil.move(possible_config_dir, config_dir)

    if config_dir.exists():
        config = read_conf(link_root)
    return config
