import argparse
import json
from urllib.parse import urlparse


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
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Path to the input JSON file")
    parser.add_argument("--output", type=str, required=True, help="Path to the output MARKDOWN file")
    parser.add_argument("--layer", type=int, default=None, help="Maximum depth of layer to display. Defaults to showing all layers.")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as input_file:
        page_dicts = json.load(input_file)

    hierarchy_with_files = build_hierarchy_with_files(page_dicts)
    with open(args.output, "w", encoding="utf-8") as output_file:
        print_hierarchy_with_files(hierarchy_with_files, n_layer=args.layer, file=output_file)
