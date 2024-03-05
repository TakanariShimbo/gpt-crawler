import argparse
import json
from typing import Any, Dict, List, Optional, TextIO
from urllib.parse import urlparse

from config import AnalyzeConfig


parser = argparse.ArgumentParser(description='Analyze web page structure and generate a layer markdown file.')
parser.add_argument('--input', type=str, default=None, help='Path to the input JSON file containing page URLs')
parser.add_argument('--output', type=str, default=None, help='Path to the output Markdown file for the layer structure')
parser.add_argument('--layer', type=int, default=None, help='Optional depth of layers to analyze')
parser.add_argument('--detail', action='store_true', default=None, help='Display titles in the layer structure')
parser.add_argument('--full', action='store_true', default=None, help='Display full url in the layer structure')


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
        if not path_segments:
            current_level["__title__"] = title
            current_level["__url__"] = url            
        for i, segment in enumerate(path_segments):
            is_last_segment = i == len(path_segments) - 1
            if segment not in current_level:
                current_level[segment] = {}
            if is_last_segment:
                current_level[segment]["__title__"] = title
                current_level[segment]["__url__"] = url
            current_level = current_level[segment]
    return layer_dict


def print_layer(
    layer_dict: Dict[str, Any],
    indent: int = 0,
    n_layer: Optional[int] = None,
    show_titles: bool = True,
    full_url: bool = True,
    file: Optional[TextIO] = None,
) -> None:
    if n_layer is not None and indent >= n_layer:
        return
    for c_layer_name, c_layer_dict in layer_dict.items():
        if c_layer_name in ("__title__", "__url__"):
            continue

        title = c_layer_dict.get("__title__", "") if show_titles else ""
        url = c_layer_dict.get("__url__", "") if show_titles else ""

        if not show_titles:
            formatted_c_layer_name = c_layer_name
        elif full_url:
            formatted_c_layer_name = f"{url} [{title}]"
        else:
            formatted_c_layer_name = f"{c_layer_name} [{title}]"

        print("  " * indent + "- " + formatted_c_layer_name, file=file)
        c_layer_dict_without_title = {k: v for k, v in c_layer_dict.items() if k not in ("__title__", "__url__")}
        if c_layer_dict_without_title:
            print_layer(layer_dict=c_layer_dict_without_title, indent=indent + 1, n_layer=n_layer, full_url=full_url, show_titles=show_titles, file=file)


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

    if args.detail != None:
        show_titles = args.detail
    elif AnalyzeConfig.detail != None:
        show_titles = AnalyzeConfig.detail
    else:
        show_titles = False

    if args.full != None:
        full_url = args.full
    elif AnalyzeConfig.full != None:
        full_url = AnalyzeConfig.full
    else:
        full_url = False

    """
    MAIN
    """
    with open(input_filepath, "r", encoding="utf-8") as input_file:
        page_dicts = json.load(input_file)

    layer_dict = analyze_layer(page_dicts=page_dicts)

    with open(output_filepath, "w", encoding="utf-8") as output_file:
        print_layer(layer_dict=layer_dict, n_layer=n_layer, show_titles=show_titles, full_url=full_url, file=output_file)
