import argparse
import json
from urllib.parse import urlparse


def build_hierarchy_with_files(data):
    hierarchy = {}
    for item in data:
        url = item["url"]
        parsed_url = urlparse(url)
        path_segments = [segment for segment in parsed_url.path.strip("/").split("/") if segment]
        domain = parsed_url.netloc
        current_level = hierarchy.setdefault(domain, {})
        for segment in path_segments:
            current_level = current_level.setdefault(segment, {})
    return hierarchy


def print_hierarchy_with_files(hierarchy, indent=0, file=None):
    for key, value in hierarchy.items():
        if key:
            print("  " * indent + "- " + key, file=file)
        if value:
            print_hierarchy_with_files(value, indent + 1, file=file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Path to the input JSON file")
    parser.add_argument("--output", type=str, required=True, help="Path to the output MARKDOWN file")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as input_file:
        data = json.load(input_file)

    hierarchy_with_files = build_hierarchy_with_files(data)
    with open(args.output, "w", encoding="utf-8") as output_file:
        print_hierarchy_with_files(hierarchy_with_files, file=output_file)
