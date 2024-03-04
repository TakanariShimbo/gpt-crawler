import json
from urllib.parse import urlparse

from config import Config


def build_hierarchy_with_files(page_dicts):
    hierarchy = {}
    for item in page_dicts:
        url = item["url"]
        parsed_url = urlparse(url)
        path_segments = [segment for segment in parsed_url.path.strip("/").split("/") if segment]
        domain = parsed_url.netloc
        current_level = hierarchy.setdefault(domain, {})
        for segment in path_segments:
            current_level = current_level.setdefault(segment, {})
    return hierarchy


def print_hierarchy_with_files(hierarchy, indent=0, n_layer=None, file=None):
    if n_layer is not None and indent >= n_layer:
        return
    for key, value in hierarchy.items():
        if key:
            print("  " * indent + "- " + key, file=file)
        if value:
            print_hierarchy_with_files(value, indent + 1, n_layer=n_layer, file=file)


if __name__ == "__main__":
    with open(Config.input_json_path, "r", encoding="utf-8") as input_file:
        page_dicts = json.load(input_file)

    hierarchy_with_files = build_hierarchy_with_files(page_dicts)
    with open(Config.output_markdown_path, "w", encoding="utf-8") as output_file:
        print_hierarchy_with_files(hierarchy_with_files, n_layer=Config.n_layer_depth, file=output_file)
