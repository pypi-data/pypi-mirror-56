from .utils import get_template_dir
from .utils import extract_zip

def apply_main(name: str, out_dir: str):
    """应用模板归档

    :param str name: 模板归档名
    :param str out_dir: 应用目录
    """
    base_dir = get_template_dir()
    matches = list(base_dir.glob("{}*.zip".format(name)))
    matches_count = len(matches)
    if matches_count == 0:
        print("no template matches: {}".format(name))
    elif matches_count == 1:
        match = matches[0]
        extract_zip(match, out_dir)
        print("apply template {} at {}".format(match.stem, out_dir))
    else:
        print("too many match:")
        for i in matches:
            print("\t{}".format(i.stem))
