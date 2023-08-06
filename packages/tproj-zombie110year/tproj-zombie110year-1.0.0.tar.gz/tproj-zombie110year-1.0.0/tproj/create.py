"""创建模板归档
"""

import zipfile
from pathlib import Path

from typing import Union
from typing import List

from .utils import parse_cfg
from .utils import create_mem_zip
from .utils import get_template_dir

__all__ = (
    "create_main",
)


def create_main(name: Union[str, None], src: str, force: bool):
    """根据当前工作目录的内容创建模板归档

    :param str name: 命令行传入的模板归档的命名
    :param str src: 要打包的目录
    :param bool force: 是否强制覆写已存在的同名归档
    """
    zf_file = Path(get_template_dir() / "{}.zip".format(name))
    if not force:
        overwrite = input(
            "there is a exsiting template named {}, overwrite? [y/n] ").strip().startswith("y")
    else:
        overwrite = force

    if overwrite:

        src_path = Path(src)
        cfg_path = Path(src_path / "tproj.yml")
        if cfg_path.exists():
            cfg = parse_cfg(cfg_path.read_text())
        else:
            cfg = parse_cfg(None)
        if cfg.get("name") == "":
            name = input("Template Name: ").strip()

        files = read_src_dir(src_path, cfg.get("include"))
        zf_content = create_mem_zip(files)
        zf_file.write_bytes(zf_content)
        print("template saved at {}".format(zf_file.as_posix()))


def read_src_dir(src: Path, include: List[str]) -> List[Path]:
    """递归地读取源目录中所有文件

    :param src: 源目录
    :param include: 要包含的文件，可以使用通配符
    """
    include_files = sum(
        [list(filter(lambda x: x.is_file(), src.glob(pat))) for pat in include], [])
    return list(set(include_files))
