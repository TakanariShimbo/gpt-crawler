import json
from typing import Any, Dict, List, Optional, TextIO
from urllib.parse import urlparse

from config import Config


def analyze_layer(
    page_dicts: List[Dict[str, str]],
) -> Dict[str, Any]:
    layer_dict: Dict[str, Any] = {}
    for item in page_dicts:
        url = item["url"]
        parsed_url = urlparse(url)
        path_segments = [segment for segment in parsed_url.path.strip("/").split("/") if segment]
        domain = parsed_url.netloc
        current_level: Dict[str, Any] = layer_dict.setdefault(domain, {})
        for segment in path_segments:
            current_level = current_level.setdefault(segment, {})
    return layer_dict


def print_layer(
    layer_dict: Dict[str, Any],
    indent: int = 0,
    n_layer: Optional[int] = None,
    file: Optional[TextIO] = None,
) -> None:
    if n_layer is not None and indent >= n_layer:
        return
    for key, value in layer_dict.items():
        if key:
            print("  " * indent + "- " + key, file=file)
        if value:
            print_layer(value, indent + 1, n_layer=n_layer, file=file)


if __name__ == "__main__":
    with open(Config.input_json_path, "r", encoding="utf-8") as input_file:
        page_dicts = json.load(input_file)

    layer_dict = analyze_layer(page_dicts=page_dicts)
    with open(Config.output_markdown_path, "w", encoding="utf-8") as output_file:
        print_layer(layer_dict=layer_dict, n_layer=Config.n_layer_depth, file=output_file)
