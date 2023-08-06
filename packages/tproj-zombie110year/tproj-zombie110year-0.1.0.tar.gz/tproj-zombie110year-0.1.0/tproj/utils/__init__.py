"""tproj 的通用工具
"""
import os
import sys
from pathlib import Path
from typing import Union
from warnings import warn

__all__ = (
    "get_tproj_home",
    "get_template_dir",
    "get_templates",
    "ensure_dir_exist",
    "ensure_file_exist",
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
        path.mkdir(parents=True)


def ensure_file_exist(path: Union[str, Path]):
    # public
    "确保文件存在，如果不存在就创建"
    if isinstance(path, str):
        path = Path(path)
    if not path.exists():
        ensure_dir_exist(path.parent)
        path.touch()


def get_templates() -> List[Path]:
    # public
    template_dir = get_template_dir()
    return list(template_dir.glob("*.zip"))


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
