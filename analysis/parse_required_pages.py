import argparse
import json
from typing import List
import re

from config import ParseConfig


parser = argparse.ArgumentParser(description='Analyze web page structure and generate a layer markdown file.')
parser.add_argument('--input', type=str, default=None, help='Path to the input JSON file containing page URLs')
parser.add_argument('--output', type=str, required=None, help='Path to the output JSON file containing page URLs')


def match_url_pattern(
    url: str,
    matches: List[str],
    excludes: List[str],
):
    for exclude in excludes:
        if re.search(exclude, url):
            return False
    for match in matches:
        if re.search(match, url):
            return True
    return False


if __name__ == "__main__":
    args = parser.parse_args()

    """
    GET PARAMS
    """
    if args.input:
        input_filepath = args.input
    elif ParseConfig.input:
        input_filepath = ParseConfig.input
    else:
        raise Exception("input is not set.")

    if args.output:
        output_filepath = args.output
    elif ParseConfig.output:
        output_filepath = ParseConfig.output
    else:
        raise Exception("output is not set.")

    if ParseConfig.matches:
        matches = ParseConfig.matches
    else:
        raise Exception("matches is not set.")

    if ParseConfig.excludes:
        excludes = ParseConfig.excludes
    else:
        excludes = []

    """
    MAIN
    """
    with open(input_filepath, "r", encoding="utf-8") as input_file:
        page_dicts = json.load(input_file)

    matched_page_dicts = []
    for page_dict in page_dicts:
        is_matched = match_url_pattern(url=page_dict["url"], matches=matches, excludes=excludes)
        if is_matched:
            matched_page_dicts.append(page_dict)

    with open(output_filepath, "w", encoding="utf-8") as output_file:
        json.dump(matched_page_dicts, output_file, ensure_ascii=False, indent=2)
