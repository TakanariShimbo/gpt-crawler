import { Config } from "./src/config";

export const defaultConfig: Config = {
  url: "https://www.uniontool.co.jp/",
  match: ["https://www.uniontool.co.jp/**"],
  exclude: [
    "https://www.uniontool.co.jp/en/**",
    "https://www.uniontool.co.jp/cn/**",
    "https://www.uniontool.co.jp/assets/**",
    "https://www.uniontool.co.jp/**/assets/**",
  ],
  maxPagesToCrawl: 500,
  outputFileName: "./res/uniontool.json",
  maxTokens: 2000000,
};
