import argparse
import json
from typing import Any, Dict, List, Optional, TextIO
from urllib.parse import urlparse

from config import AnalyzeConfig


parser = argparse.ArgumentParser(description='Analyze web page structure and generate a layer markdown file.')
parser.add_argument('--input', type=str, default=None, help='Path to the input JSON file containing page URLs')
parser.add_argument('--output', type=str, required=None, help='Path to the output Markdown file for the layer structure')
parser.add_argument('--layer', type=int, default=None, help='Optional depth of layers to analyze')
parser.add_argument('--disable-titles', action='store_true', default=None, help='Display titles in the layer structure')


def analyze_layer(
    page_dicts: List[Dict[str, str]],
) -> Dict[str, Any]:
    layer_dict: Dict[str, Any] = {}
    for item in page_dicts:
        url = item["url"]
        title = item["title"]
        parsed_url = urlparse(url)
        path_segments = [segment for segment in parsed_url.path.strip("/").split("/") if segment]
        domain = parsed_url.netloc
        current_level: Dict[str, Any] = layer_dict.setdefault(domain, {})
        for i, segment in enumerate(path_segments):
            is_last_segment = i == len(path_segments) - 1
            if segment not in current_level:
                current_level[segment] = {}
            if is_last_segment:
                current_level[segment]["__title__"] = title
            current_level = current_level[segment]
    return layer_dict


def print_layer(
    layer_dict: Dict[str, Any],
    indent: int = 0,
    n_layer: Optional[int] = None,
    show_titles: bool = True,
    file: Optional[TextIO] = None,
) -> None:
    if n_layer is not None and indent >= n_layer:
        return
    for c_layer_name, c_layer_dict in layer_dict.items():
        if c_layer_name == "__title__":
            continue

        title = c_layer_dict.get("__title__", "") if show_titles else ""

        formatted_c_layer_name = f"{c_layer_name} [{title}]" if title else c_layer_name
        print("  " * indent + "- " + formatted_c_layer_name, file=file)
        c_layer_dict_without_title = {k: v for k, v in c_layer_dict.items() if k != "__title__"}
        if c_layer_dict_without_title:
            print_layer(layer_dict=c_layer_dict_without_title, indent=indent + 1, n_layer=n_layer, show_titles=show_titles, file=file)


if __name__ == "__main__":
    args = parser.parse_args()

    """
    GET PARAMS
    """
    if args.input:
        input_filepath = args.input
    elif AnalyzeConfig.input:
        input_filepath = AnalyzeConfig.input
    else:
        raise Exception("input is not set.")

    if args.output:
        output_filepath = args.output
    elif AnalyzeConfig.output:
        output_filepath = AnalyzeConfig.output
    else:
        output_filepath = input_filepath[:-5] + ".md"

    if args.layer:
        n_layer = args.layer
    elif AnalyzeConfig.layer:
        n_layer = AnalyzeConfig.layer
    else:
        n_layer = None

    if args.disable_titles != None:
        show_titles = not args.disable_titles
    elif AnalyzeConfig.disable_titles != None:
        show_titles = not AnalyzeConfig.disable_titles
    else:
        show_titles = True

    """
    MAIN
    """
    with open(input_filepath, "r", encoding="utf-8") as input_file:
        page_dicts = json.load(input_file)

    layer_dict = analyze_layer(page_dicts=page_dicts)

    with open(output_filepath, "w", encoding="utf-8") as output_file:
        print_layer(layer_dict=layer_dict, n_layer=n_layer, show_titles=show_titles, file=output_file)
