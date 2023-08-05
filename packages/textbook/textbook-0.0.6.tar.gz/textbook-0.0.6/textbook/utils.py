#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-17 15:27:54
# @Author  : Chenghao Mou (mouchenghao@gmail.com)

import os

from dataclasses import dataclass
from typing import *
from pathlib import Path
import abc

import torch
import av
import torchvision

# @dataclass


class Renderer(abc.ABC):

    @abc.abstractmethod
    def render(self, json_datum: Dict[str, Any]) -> Dict[str, Any]:
        raise Exception("render function not implemented")


@dataclass
class TextRenderer(Renderer):

    tokenizer: object
    special_tokens: Dict[str, str]

    def __post_init__(self):
        """
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        model = GPT2Model.from_pretrained('gpt2')

        special_tokens_dict = {'cls_token': '<CLS>'}

        num_added_toks = tokenizer.add_special_tokens(special_tokens_dict)
        print('We have added', num_added_toks, 'tokens')
        model.resize_token_embeddings(len(tokenizer))  # Notice: resize_token_embeddings expect to receive the full size of the new vocabulary, i.e. the length of the tokenizer.

        assert tokenizer.cls_token == '<CLS>'

        """

        self.tokenizer.add_special_tokens(self.special_tokens)
        assert getattr(self.tokenizer, "cls_token") is not None, "cls token not found"
        assert getattr(self.tokenizer, "pad_token") is not None, "pad token not found"

        # TODO: resize model's embeddings

    def render(self, json_datum: Dict[str, Any]) -> Dict[str, Any]:

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


@dataclass
class VisionRenderer(Renderer):

    nframe: int
    nclip: int = 1
    nstep: int = 1
    transform_pre: Callable = None
    transform_post: Callable = None
    data_dir: Union[Path, str] = None

    def render(self, json_datum: Dict[str, Any]) -> Dict[str, Any]:

        path = os.path.join(self.data_dir, json_datum["image"] + ".webm")
        reader = av.open(path)

        try:
            imgs = []
            imgs = [f.to_rgb().to_ndarray() for f in reader.decode(video=0)]
        except (RuntimeError, ZeroDivisionError) as exception:
            print('{}: WEBM reader cannot open {}. Empty list returned.'.format(type(exception).__name__, path))

        imgs = self.transform_pre(imgs)
        imgs = self.transform_post(imgs)

        num_frames = len(imgs)

        if self.nclip > -1:
            num_frames_necessary = self.nframe * self.nclip * self.nstep
        else:
            num_frames_necessary = num_frames

        offset = 0
        if num_frames_necessary < num_frames:
            # If there are more frames, then sample a starting offset.
            diff = (num_frames - num_frames_necessary)
            offset = np.random.randint(0, diff)

        imgs = imgs[offset: num_frames_necessary + offset: self.nstep]

        if len(imgs) < (self.nframe * self.nclip):
            imgs.extend([imgs[-1]] * ((self.nframe * self.nclip) - len(imgs)))

        data = torch.stack(imgs)
        data = data.permute(1, 0, 2, 3)

        json_datum["image"] = data

        return json_datum


if __name__ == "__main__":

    from .config import *
    from transformers import *
    from .transforms_video import *

    text_renderer = TextRenderer(
        tokenizer=GPT2Tokenizer.from_pretrained('distilgpt2'),
        special_tokens={'cls_token': '[CLS]', 'pad_token': '[PAD]'},
    )

    # config_alphanli = Configuration(alphanli_config)
    # for datum in config_alphanli.load("data_cache/alphanli/eval.jsonl"):

    #     print(text_renderer.render(datum), end="\r")

    upscale_size = int(84 * 1.1)
    transform_pre = ComposeMix([
        [Scale(upscale_size), "img"],
        [RandomCropVideo(84), "vid"],
    ])

    transform_post = ComposeMix([
        [torchvision.transforms.ToTensor(), "img"],
    ])

    video_renderer = VisionRenderer(
        nframe=72,
        nclip=1,
        nstep=2,
        transform_pre=transform_pre,
        transform_post=transform_post,
        data_dir="data_cache/smthsmth/20bn-something-something-v2"
    )

    config_smthsmth = Configuration(smthsmth_config)
    for datum in config_smthsmth.load("data_cache/smthsmth/something-something-v2-validation.json"):
        d = video_renderer.render(text_renderer.render(datum))
        print(d['image'].shape, d.keys(), end='\r')
