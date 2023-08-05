#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-17 18:09:14
# @Author  : Chenghao Mou (mouchenghao@gmail.com)
# @Link    : link
# @Version : 1.0.0

import os
from typing import *
from pathlib import Path
from .config import *
from .utils import *

import torch
from torch.utils.data import Dataset, Sampler, DataLoader, IterableDataset
from torch.nn.utils.rnn import pad_sequence
from transformers import PreTrainedTokenizer
from itertools import zip_longest


def collate_fn(samples: List[Dict[str, Any]],
               image_size: Tuple[int, int, int, int] = (3, 72, 84, 84),
               max_seq_len: int = 512,
               mlm: bool = False,
               mlm_probability: float = 0.15,
               tokenizer: PreTrainedTokenizer = None,
               source: str = "name") -> Dict[str, Any]:

    template: Dict = {
        "input_ids": [],
        "labels": [],
        "attentions": [],
        "images": [],
        "token_type_ids": [],
        "source": source
    }

    for sample in samples:

        template["input_ids"].append(torch.LongTensor(sample["input_id"]).transpose(0, 1))
        template["attentions"].append(torch.LongTensor(sample["attention"]).transpose(0, 1))
        template["token_type_ids"].append(torch.LongTensor(sample["token_type_id"]).transpose(0, 1))
        template["images"].append(sample["image"] if sample["image"] is not None else torch.zeros(image_size))
        template["labels"].append(sample["label"])

    # for x in template["input_ids"]:
    #     print(x.shape)

    template["input_ids"] = pad_sequence(template["input_ids"], batch_first=True).transpose(1, 2)
    template["attentions"] = pad_sequence(template["attentions"], batch_first=True).transpose(1, 2)
    template["token_type_ids"] = pad_sequence(template["token_type_ids"], batch_first=True).transpose(1, 2)
    template["images"] = torch.stack(template["images"])

    if mlm == True:
        batch_size, num_choice, seq_length = template["input_ids"].shape
        template["input_ids"], template["label"] = mask_tokens(
            template["input_ids"].reshape(-1, seq_length),
            text_renderer.tokenizer, mlm_probability)
        template["input_ids"] = template["input_ids"].reshape(batch_size, num_choice, seq_length)
        template["label"] = template["label"].reshape(batch_size, num_choice, seq_length)

    return template


def mask_tokens(input_ids, tokenizer, mlm_probability: float = 0.15):
    """ Prepare masked tokens input_ids/labels for masked language modeling: 80% MASK, 10% random, 10% original. """
    labels = input_ids.clone()
    # We sample a few tokens in each sequence for masked-LM training (with probability args.mlm_probability defaults to 0.15 in Bert/RoBERTa)
    probability_matrix = torch.full(labels.shape, mlm_probability)
    special_tokens_mask = [tokenizer.get_special_tokens_mask(val, already_has_special_tokens=True) for val in labels.tolist()]
    probability_matrix.masked_fill_(torch.tensor(special_tokens_mask, dtype=torch.bool), value=0.0)
    masked_indices = torch.bernoulli(probability_matrix).bool()
    labels[~masked_indices] = -1  # We only compute loss on masked tokens

    # 80% of the time, we replace masked input tokens with tokenizer.mask_token ([MASK])
    indices_replaced = torch.bernoulli(torch.full(labels.shape, 0.8)).bool() & masked_indices
    input_ids[indices_replaced] = tokenizer.convert_tokens_to_ids(tokenizer.mask_token)

    # 10% of the time, we replace masked input tokens with random word
    indices_random = torch.bernoulli(torch.full(labels.shape, 0.5)).bool() & masked_indices & ~indices_replaced
    random_words = torch.randint(len(tokenizer), labels.shape, dtype=torch.long)
    input_ids[indices_random] = random_words[indices_random]

    # The rest of the time (10% of the time) we keep the masked input tokens unchanged
    return input_ids, labels


class DynamicBatchSampler(Sampler):

    def __init__(self, data_source, batch_size: int = 4096):
        self.batch_size = batch_size
        self.num_sample = len(data_source)
        self.indicies = torch.randperm(self.num_sample)
        self.data_source = [sum(map(len, data_source[self.indicies[i]]["input_id"])) for i in range(self.num_sample)]
        self.i = 0

    def __iter__(self):

        curr_batch = []
        curr_num_token = 0

        while True:

            while self.i < self.num_sample and curr_num_token <= self.batch_size:
                curr_batch.append(self.indicies[self.i])
                curr_num_token += self.data_source[self.indicies[self.i]]
                self.i += 1

            if curr_batch:
                yield curr_batch
            else:
                break


class ClassificationDataset(Dataset):

    def __init__(self, path: Union[Path, str], config: Configuration, renderers: List[Renderer]):

        self.data: List = []
        for datum in config.load(path):
            for renderer in renderers:
                datum = renderer.render(datum)
            self.data.append(datum)

    def __len__(self):

        return len(self.data)

    def __getitem__(self, index):

        return self.data[index]


class ClassificationVisionDataset(IterableDataset):

    def __init__(self, path: Union[Path, str], config: Configuration, renderers: List[Renderer]):

        self.data: List = []
        self.path = path
        self.config = config
        self.renderers = renderers

    def __len__(self):
        return int(float("inf"))

    def __iter__(self):

        def process(d):
            for renderer in self.renderers:
                d = renderer.render(d)
            return d

        return iter(process(d) for d in self.config.load(self.path))


class MultiTaskDataset(IterableDataset):

    def __init__(self, dataloaders):

        self.dataloaders = dataloaders
        self.i = 0

    def __len__(self):
        return int(float("inf"))

    def __iter__(self):

        return iter(x for y in zip_longest(*self.dataloaders) for x in y if x is not None)


if __name__ == "__main__":

    from .config import *
    from transformers import GPT2Tokenizer
    from .transforms_video import *

    text_renderer = TextRenderer(
        tokenizer=GPT2Tokenizer.from_pretrained('distilgpt2'),
        special_tokens={'cls_token': '[CLS]', 'pad_token': '[PAD]', 'mask_token': '[MASK]'},
    )

    config_alphanli = Configuration(alphanli_config)

    alphanli_dataset = ClassificationDataset("data_cache/alphanli/eval.jsonl", config_alphanli, [text_renderer])

    alphanli_dev_dataloader: DataLoader = iter(
        DataLoader(
            alphanli_dataset, batch_sampler=DynamicBatchSampler(alphanli_dataset),
            collate_fn=collate_fn))

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

    smthsmth_dataset = ClassificationVisionDataset(
        "data_cache/smthsmth/something-something-v2-validation.json", config_smthsmth, [text_renderer, video_renderer])

    smthsmth_dev_dataloader: DataLoader = iter(DataLoader(
        smthsmth_dataset, batch_size=16, collate_fn=lambda x: collate_fn(
            x, mlm=True, mlm_probability=0.15, tokenizer=text_renderer.tokenizer)))

    multitask_dataloader = MultiTaskDataset([alphanli_dev_dataloader, smthsmth_dev_dataloader])

    for batch in multitask_dataloader:
        print(batch["input_ids"].shape)
        print(batch["images"].shape)
