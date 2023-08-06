from pathlib import Path
from .utils import get_templates

from typing import List

def ls_main():
    """列出所有可用的模板归档"""
    for i in get_templates():
        print("{}".format(i.stem))
