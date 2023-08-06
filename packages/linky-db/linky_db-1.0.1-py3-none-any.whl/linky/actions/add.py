import logging

from linky.actions.tag import tag
from linky.utils.library_utils import move_to_base, recreate_with_symlinks
from linky.utils.path_utils import get_path_in_base


def add(path, base_path, config, cat_tag=None, prefix="", linked_root_prefix=False):
    """
    Imports a path into the base to be managed by linky

    @param path: What we're trying to import
    @type path: Path
    @param base_path: The base into which the item should be imported
    @type base_path: Path
    @type config: linky.config.Config
    @param cat_tag: The predefined tag for a specific category
    @type cat_tag: linky.utils.path_utils.CategoryTagTuple
    @param prefix: An additional prefix to add to the path
                   If config.prefix_at_import is used in addition to this,
                   this prefix will first be added and the standard prefix
                   calculated thereafter
    @type prefix: basestring
    @param linked_root_prefix: Mutually exclusive with prefix.
                                Calculates the prefix within the linked root
                                while removing categories and tags
    @type linked_root_prefix: bool
    """
    logger = logging.getLogger("actions.add.add")
    logger.info("Adding: %s", path)
    logger.debug("Base path: %s", base_path)
    if cat_tag:
        logger.info("Pre cat-tag: %s", cat_tag)

    if linked_root_prefix:
        prefix = get_path_in_base(base_path, path, relative=True).parent
        logger.debug("Adding linked root prefix '%s'", prefix)

    path_in_base = move_to_base(path, base_path, config, prefix)
    logger.debug("New path in base '%s'", path_in_base)
    if len(config.categories):
        logger.debug("Categorizing and tagging...")
        # Apply default tags for everything
        # except when cat_tag is passed
        for cat_name, category in config.categories.items():
            tag_name = category.default
            if cat_tag is not None and cat_name == cat_tag.c:
                tag_name = cat_tag.t
            tag(path_in_base, "%s/%s" % (cat_name, tag_name), config)
    else:
        logger.info("Simply relinking in root...")
        recreate_with_symlinks(base_path.parent / path_in_base.relative_to(base_path), path_in_base)
