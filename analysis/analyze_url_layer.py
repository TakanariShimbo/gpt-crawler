import argparse
import json
from typing import Any, Dict, List, Optional, TextIO
from urllib.parse import urlparse

from config import AnalyzeConfig


parser = argparse.ArgumentParser(description='Analyze web page structure and generate a layer markdown file.')
parser.add_argument('--input', type=str, default=None, help='Path to the input JSON file containing page URLs')
parser.add_argument('--output', type=str, required=None, help='Path to the output Markdown file for the layer structure')
parser.add_argument('--layer', type=int, default=None, help='Optional depth of layers to analyze')


def analyze_layer(
    page_dicts: List[Dict[str, str]],
) -> Dict[str, Any]:
    url_layer_dict: Dict[str, Any] = {}
    for item in page_dicts:
        url = item["url"]
        parsed_url = urlparse(url)
        path_segments = [segment for segment in parsed_url.path.strip("/").split("/") if segment]
        domain = parsed_url.netloc
        current_level: Dict[str, Any] = url_layer_dict.setdefault(domain, {})
        for segment in path_segments:
            current_level = current_level.setdefault(segment, {})
    return url_layer_dict


def print_layer(
    url_layer_dict: Dict[str, Any],
    indent: int = 0,
    n_layer: Optional[int] = None,
    file: Optional[TextIO] = None,
) -> None:
    if n_layer is not None and indent >= n_layer:
        return
    for key, value in url_layer_dict.items():
        if key:
            print("  " * indent + "- " + key, file=file)
        if value:
            print_layer(url_layer_dict=value, indent=indent + 1, n_layer=n_layer, file=file)


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

    """
    MAIN
    """
    with open(input_filepath, "r", encoding="utf-8") as input_file:
        page_dicts = json.load(input_file)

    layer_dict = analyze_layer(page_dicts=page_dicts)
    with open(output_filepath, "w", encoding="utf-8") as output_file:
        print_layer(url_layer_dict=layer_dict, n_layer=n_layer, file=output_file)
