#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-20 21:20:23
# @Author  : Chenghao Mou (chengham@isi.edu)

# pylint: disable=unused-wildcard-import
# pylint: disable=no-member

import abc
import os
import multiprocessing

from pathlib import Path
from dataclasses import dataclass
from multiprocessing import Pool
from typing import *
from textbook.transforms_video import *


import numpy as np
import torchvision
import av
import torch
from transformers import PreTrainedTokenizer
from loguru import logger
from tqdm import tqdm

NUM_CORES = max(2, multiprocessing.cpu_count() // 4)
SCALE = 1.1


def parallel_map(func: Callable, iterable: Iterable, ordered=True) -> List[Any]:

    results: List[Any] = []

    with Pool(NUM_CORES) as p:
        if ordered:
            results = list(tqdm(p.map(func, iterable), total=len(iterable)))
        else:
            results = list(tqdm(p.imap_unordered(func, iterable), total=len(iterable)))

    return results


class Renderer(abc.ABC):

    @abc.abstractmethod
    def render(self, json_datum: Dict[str, Any], parallel: bool = False) -> Dict[str, Any]:
        raise Exception("render function not implemented")


@dataclass
class TextRenderer(Renderer):

    tokenizer: PreTrainedTokenizer

    def __post_init__(self):

        assert getattr(self.tokenizer, "cls_token") is not None, "cls token not found"
        assert getattr(self.tokenizer, "pad_token") is not None, "pad token not found"
        assert getattr(self.tokenizer, "mask_token") is not None, "mask token not found"
        logger.debug(
            f"Tokenizer special vocab: cls_token {self.tokenizer.cls_token}/{self.tokenizer.cls_token_id}; "
            f"pad_token {self.tokenizer.pad_token}/{self.tokenizer.pad_token_id}; mask_token {self.tokenizer.mask_token}/{self.tokenizer.mask_token_id}")

    def render_sample(self, json_datum: Dict[str, Any]) -> Dict[str, Any]:

        template = {
            "input_id": [[] for _ in range(len(json_datum["text"]))],
            "label": json_datum["label"],
            "attention": [[] for _ in range(len(json_datum["text"]))],
            "token_type_id": [[] for _ in range(len(json_datum["text"]))],
            "image": json_datum["image"],
        }

        max_seq_len = 0

        for i, group in enumerate(json_datum["text"]):

            for j, (attn, token_type, sentence) in enumerate(zip(json_datum["attention"], json_datum["token_type_id"], group)):
                tokens = self.tokenizer.tokenize(sentence)
                if j == 0:
                    tokens = [self.tokenizer.cls_token] + tokens
                tokens = tokens + [self.tokenizer.pad_token]

                template["attention"][i].extend(attn for _ in tokens)
                template["token_type_id"][i].extend(token_type for _ in tokens)
                template["input_id"][i].extend(self.tokenizer.convert_tokens_to_ids(tokens))

            max_seq_len = max(max_seq_len, len(template["input_id"][i]))

        for j in range(len(template["input_id"])):
            while len(template["input_id"][j]) < max_seq_len:
                template["input_id"][j].append(self.tokenizer.pad_token_id)
                template["attention"][j].append(0)
                template["token_type_id"][j].append(0)

        return template

    def render(self, samples: List, parallel=False) -> List[Any]:

        if parallel:
            return parallel_map(self.render_sample, samples)
        else:
            return list(map(self.render_sample, tqdm(samples)))


@dataclass
class VideoRenderer(Renderer):

    data_dir: Union[Path, str]
    nframe: int = 72
    nclip: int = 1
    width: int = 64
    dstep_size: int = 1
    transform_pre: Callable = None
    transform_post: Callable = None

    def __post_init__(self):

        if self.transform_pre is None:
            upscale_size = int(self.width * SCALE)
            self.transform_pre = ComposeMix([
                [Scale(upscale_size), "img"],
                [RandomCropVideo(self.width), "vid"],
            ])

        if self.transform_post is None:
            self.transform_post = ComposeMix([
                [torchvision.transforms.ToTensor(), "img"],
            ])

    def render_sample(self, json_datum: Dict[str, Any]) -> Dict[str, Any]:
        assert json_datum["image"] is not None, json_datum
        path = os.path.join(self.data_dir, json_datum["image"] + ".webm")
        with av.open(path) as reader:

            try:
                imgs = []
                imgs = [f.to_rgb().to_ndarray() for f in reader.decode(video=0)]
            except (RuntimeError, ZeroDivisionError) as exception:
                print('{}: WEBM reader cannot open {}. Empty list returned.'.format(type(exception).__name__, path))

        imgs = self.transform_pre(imgs)
        imgs = self.transform_post(imgs)

        num_frames = len(imgs)

        if self.nclip > -1:
            num_frames_necessary = self.nframe * self.nclip * self.dstep_size
        else:
            num_frames_necessary = num_frames

        offset = 0
        if num_frames_necessary < num_frames:
            # If there are more frames, then sample a starting offset.
            diff = (num_frames - num_frames_necessary)
            offset = np.random.randint(0, diff)

        imgs = imgs[offset: num_frames_necessary + offset: self.dstep_size]

        if len(imgs) < (self.nframe * self.nclip):
            imgs.extend([imgs[-1]] * ((self.nframe * self.nclip) - len(imgs)))

        data = torch.stack(imgs)
        data = data.permute(1, 0, 2, 3)

        json_datum["image"] = data

        return json_datum

    def render(self, samples: List, parallel=False) -> Dict[str, Any]:

        if parallel:
            return parallel_map(self.render_sample, samples)
        else:
            return list(map(self.render_sample, tqdm(samples)))
