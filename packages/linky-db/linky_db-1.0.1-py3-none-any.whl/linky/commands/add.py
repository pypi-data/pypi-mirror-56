from cliff.command import Command

import linky.utils.path_utils as path_utils
from linky.actions import add
from linky.config import read_conf


class AddCommand(Command):
    """
    Add an item to the linky management
    """

    def get_parser(self, prog_name):
        parser = super(AddCommand, self).get_parser(prog_name)
        parser.add_argument("-b", "--base-path",
                            help="Where to add the file/dir")
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-l", "--linked-root-prefix",
                           action="store_true",
                           help="Calculates the prefix in the linked root"
                                "(ignoring category and base folders of course)"
                                "e.g"
                                "  path = linked_root/category/tag/dir/subdir/filename"
                                "  -->prefix = dir/subdir"
                                "  -->result = base_path/dir/subdir/filename")
        group.add_argument("-p", "--prefix",
                           default="",
                           help="<base_path>/<prefix>/<path name>\n"
                                "e.g\n"
                                "  path = /tmp/dir/subdir/filename\n"
                                "  prefix = just/a/prefix\n"
                                "  result --> base_path/just/a/prefix/filename\n")
        parser.add_argument("path")
        return parser

    def take_action(self, parsed_args):
        _abs_path = path_utils.abs_path(parsed_args.path)
        base_path = parsed_args.base_path or path_utils.find_base(_abs_path)
        add(
            _abs_path,
            base_path,
            read_conf(base_path),
            prefix=parsed_args.prefix,
            linked_root_prefix=parsed_args.linked_root_prefix
        )
