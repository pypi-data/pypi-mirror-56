"""tproj 的通用工具
"""
import os
import sys
from io import BytesIO
from pathlib import Path
from typing import List
from typing import Union
from warnings import warn
from zipfile import ZIP_DEFLATED
from zipfile import ZipFile

import yaml

__all__ = (
    "get_tproj_home",
    "get_template_dir",
    "get_templates",
    "ensure_dir_exist",
    "ensure_file_exist",
    "create_mem_zip",
)


def get_template_dir() -> Path:
    # public
    "获取 template 目录"
    path = get_tproj_home() / "template"
    ensure_dir_exist(path)
    return path


def get_tproj_home() -> Path:
    # public
    """获取 TPROJ_HOME 目录
    """
    var = os.getenv("TPROJ_HOME")
    if var is None:
        home = get_default_tproj_home()
    else:
        home = Path(var)
    ensure_dir_exist(home)
    return home


def ensure_dir_exist(path: Union[str, Path]):
    # public
    "确保目录存在，如果不存在就创建"
    if isinstance(path, str):
        path = Path(path)
    if not path.exists():
        print("create directory: {}".format(path.absolute().as_posix()))
        path.mkdir(parents=True)


def ensure_file_exist(path: Union[str, Path]):
    # public
    "确保文件存在，如果不存在就创建"
    if isinstance(path, str):
        path = Path(path)
    if not path.exists():
        ensure_dir_exist(path.parent)
        print("create file: {}".format(path.absolute().as_posix()))
        path.touch()


def parse_cfg(conf_text: Union[str, None]) -> dict:
    """解析创建模板归档的配置文件

    |   键    |   类型    |     默认值      | 含义                      |
    | :-----: | :-------: | :-------------: | ------------------------- |
    |  name   |    str    |      `""`       | 此模板的名字              |
    | author  |    str    |      `""`       | 模板的作者，`name<email>` |
    | include | List[str] |   `["**/*"]`    | 默认包含所有文件、子目录  |
    | exclude | List[str] | `[".git/**/*"]` | 被排除的文件              |

    :param conf_text: 配置文件的内容
    """
    default = {
        "name": "",
        "author": "",
        "include": [
            "**/*"
        ],
        "exclude": [
            ".git/**/*"
        ]
    }
    if conf_text is None:
        return default
    else:
        config = yaml.load(conf_text, Loader=yaml.SafeLoader)
        assert isinstance(config, dict)
        for k in default.keys():
            if k in config.keys():
                default[k] = config.get(k)
        return default


def create_mem_zip(files: List[Path]) -> bytes:
    # public
    """在内存中创建一个 zipfile
    """
    buffer = BytesIO()
    zf = ZipFile(buffer, "w", ZIP_DEFLATED)
    for file in files:
        zf.write(file.as_posix())
    zf.close()
    buffer.seek(0)
    data = buffer.read()
    return data


def get_templates() -> List[Path]:
    # public
    template_dir = get_template_dir()
    return list(template_dir.glob("*.zip"))

def extract_zip(src: Path, out_dir: Path):
    # public
    """解压 zip 包到 out_dir
    """
    zf = ZipFile(src, "r", compression=ZIP_DEFLATED)
    zf.extractall(out_dir)

def extract_zip(src: Path, out_dir: Path):
    # public
    """解压 zip 包到 out_dir
    """
    zf = ZipFile(src, "r", compression=ZIP_DEFLATED)
    zf.extractall(out_dir)


def get_default_tproj_home() -> Path:
    """获取默认的 TPROJ_HOME

    | 操作系统 | 默认值                 |
    |:--------:|------------------------|
    |  Linux   | `$XDG_DATA_HOME/tproj` |
    | Windows  | `%APPDATA%\\tproj`     |

    其他系统未实现，将尝试使用 Linux 的设置
    """
    if sys.platform == "win32":
        return get_default_tproj_home_win32()
    elif sys.platform == "linux":
        return get_default_tproj_home_linux()
    else:
        warn("未知的操作系统，加载 Linux 配置，这可能会导致一些问题，请谨慎使用")
        return get_default_tproj_home_linux()


def get_default_tproj_home_linux() -> Path:
    var = os.getenv("XDG_DATA_HOME")
    if var is None:
        return Path.home() / ".local" / "share" / "tproj"
    else:
        return Path(var)


def get_default_tproj_home_win32() -> Path:
    var = os.getenv("APPDATA")
    return Path(var) / "tproj"
