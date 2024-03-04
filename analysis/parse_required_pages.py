import json
from typing import List
import fnmatch

from config import Config


def match_url_pattern(url: str, matches: List[str]):
    for match in matches:
        if fnmatch.fnmatch(name=url, pat=match):
            return True
    return False


if __name__ == "__main__":
    with open(Config.input_json_path, "r", encoding="utf-8") as input_file:
        page_dicts = json.load(input_file)

    matched_page_dicts = []
    for page_dict in page_dicts:
        is_matched = match_url_pattern(url=page_dict["url"], matches=Config.matches)
        if is_matched:
            matched_page_dicts.append(page_dict)

    with open(Config.output_json_path, "w", encoding="utf-8") as output_file:
        json.dump(matched_page_dicts, output_file, ensure_ascii=False, indent=4)