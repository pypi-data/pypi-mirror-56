"""命令行入口
"""
import argparse

from . import __version__
from .apply import apply_main
from .create import create_main
from .ls import ls_main

__all__ = (
    "get_tproj_argparser",
)


def get_tproj_argparser():
    "获取本程序的命令行参数解析器"
    parser = argparse.ArgumentParser("tproj")
    parser.add_argument("--version", action="version", version=__version__)
    subcmd = parser.add_subparsers(dest="subcmd")

    apply = subcmd.add_parser("apply")
    create = subcmd.add_parser("create")
    ls = subcmd.add_parser("ls")

    apply.add_argument("name",
                       help="指定模板命名")
    apply.add_argument("-O", "--our-dir", dest="out_dir",
                       help="归档解压到指定目录",
                       default=".")

    create.add_argument("-n", "--name", dest="name",
                        help="指定归档的命名",
                        required=False,
                        default=None)

    create.add_argument("-f", "--force", dest="force",
                        help="强制覆盖同名的模板归档",
                        action="store_true")

    return parser


def main():
    "程序入口"
    args = get_tproj_argparser().parse_args()

    if args.subcmd == "apply":
        apply_main(args.name, args.out_dir)
    elif args.subcmd == "create":
        create_main(args.name, ".", args.force)
    elif args.subcmd == "ls":
        ls_main()
