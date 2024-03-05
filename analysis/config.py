

class AnalyzeConfig:
    input  = "./res/uniontool.json"
    output = None
    layer  = None

class ParseConfig:
    input  = "./res/uniontool.json"
    output = "./res/parsed_uniontool.json"

    matches = [
        r"https://www\.uniontool\.co\.jp/product/.+",
    ]
    excludes = [
        r"https://www\.uniontool\.co\.jp/product/.+\.html",
    ]
