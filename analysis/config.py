

class AnalyzeConfig:
    input  = "./res/uniontool.json"
    output = None
    layer  = None
    detail = None
    full = None

class ParseConfig:
    input  = "./res/uniontool.json"
    output = "./res/uniontool_recruit_info.json"

    matches = [
        r"https://www\.uniontool\.co\.jp/recruit/.+",
    ]
    excludes = []
