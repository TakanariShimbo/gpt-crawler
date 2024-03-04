

class Config:
    # analyze url layer
    input_json_path = "./res/uniontool.json"
    output_markdown_path = "./res/uniontool.md"
    n_layer_depth = None

    # parse required pages
    matches = [
        "https://www.uniontool.co.jp/product/**",
    ]
    excludes = [
        "https://www.uniontool.co.jp/product/**.html",
    ]
    output_json_path = "./res/parsed_uniontool.json"