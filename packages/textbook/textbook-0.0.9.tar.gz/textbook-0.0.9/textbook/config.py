#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-17 14:09:21
# @Author  : Chenghao Mou (chenghaomou@gmail.com)

# pylint: disable=unused-wildcard-import
# pylint: disable=no-member

import os
import json
import _jsonnet as jsonnet

from dataclasses import dataclass
from typing import *
from pathlib import Path

alphanli_config = """
local data = std.parseJson(std.extVar("input"));
{
    text: [
        [data["obs1"], data["hyp1"], data["obs2"]],
        [data["obs1"], data["hyp2"], data["obs2"]],
    ],
    label: if "label" in data then self.label2int[std.toString(data["label"])] else null,
    image: if "image" in data then data["image"] else null,
    token_type_id: [0, 1, 0],
    attention: [1, 1, 1],
    int2label: {
        "0": "1",
        "1": "2",
    },
    label2int: {
        "1": 0,
        "2": 1,
    }
}
"""

hellaswag_config = """
local data = std.parseJson(std.extVar("input"));
{
    text: [
        [data["ctx"], x] for x in data["ending_options"]
    ],
    label: if "label" in data then std.parseInt(std.toString(data["label"])) else null,
    image: if "image" in data then data["image"] else null,
    token_type_id: [0, 1],
    attention: [1, 1],
    label2int: {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
    },
    int2label: {
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
    }
}
"""

physicaliqa_config = """
local data = std.parseJson(std.extVar("input"));
{
    text: [
        [data["goal"], data["sol1"]],
        [data["goal"], data["sol2"]],
    ],
    label: if "label" in data then std.parseInt(std.toString(data["label"])) else null,
    image: if "image" in data then data["image"] else null,
    token_type_id: [0, 1],
    attention: [1, 1],
    label2int: {
        "0": 0,
        "1": 1,
    },
    int2label: {
        "0": "0",
        "1": "1",
    }
}
"""


socialiqa_config = """
local data = std.parseJson(std.extVar("input"));
{
    text: [
        [data["context"], data["question"], data["answerA"]],
        [data["context"], data["question"], data["answerB"]],
        [data["context"], data["question"], data["answerC"]],
    ],
    label: if "label" in data then std.parseInt(std.toString(data["label"])) else null,
    image: if "image" in data then data["image"] else null,
    token_type_id: [0, 0, 1],
    attention: [1, 1, 1],
    int2label: {
        "0": "1",
        "1": "2",
        "2": "3"
    },
    label2int: {
        "1": 0,
        "2": 1,
        "3": 2
    },
}
"""

smthsmth_config = """
local data = std.parseJson(std.extVar("input"));
{
    text: [
        [data["label"]],
    ],
    token_type_id: [0],
    attention: [1],
    label: null,
    image: data["id"],
}
"""


@dataclass
class Configuration:

    config: str

    def transform(self, datum: str, ext_vars: Dict[str, Any] = None) -> Dict[str, Any]:

        if ext_vars is None:
            ext_vars = {}

        json_datum: Dict = json.loads(jsonnet.evaluate_snippet("snippet", self.config, ext_vars={"input": datum}))

        json_datum.update(ext_vars)

        return json_datum

    def load(self, path: Union[Path, str]) -> List[Dict[str, Any]]:

        path = Path(path)

        with open(path, "r") as f:

            if str(path).endswith("jsonl"):
                for line in f:
                    yield self.transform(line)
            else:
                data = json.loads(f.read())
                for datum in data:
                    yield self.transform(json.dumps(datum))


if __name__ == "__main__":

    # config_alphanli = Configuration(alphanli_config)
    # for datum in config_alphanli.load("data_cache/alphanli/eval.jsonl"):
    #     print(datum, end="\r")

    # config_smthsmth = Configuration(smthsmth_config)
    # for datum in config_smthsmth.load("data_cache/smthsmth/something-something-v2-validation.json"):
    #     print(datum, end='\r')

    pass
