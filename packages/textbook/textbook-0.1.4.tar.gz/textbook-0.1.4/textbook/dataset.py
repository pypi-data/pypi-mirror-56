#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-17 18:09:14
# @Author  : Chenghao Mou (mouchenghao@gmail.com)
# @Link    : link
# @Version : 1.0.0

# pylint: disable=unused-wildcard-import
# pylint: disable=no-member
# pylint: disable=invalid-sequence-index

import os
import random
import json
from typing import *
from pathlib import Path
from .configurations import *
from .utilities import *
from dataclasses import dataclass

import torch
from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence
from transformers import PreTrainedTokenizer
from itertools import zip_longest


@dataclass
class BatchTool:

    tokenizer: PreTrainedTokenizer
    max_seq_len: int = 512
    mlm: bool = False
    mlm_probability: float = 0.15
    source: str = ""

    def collate_fn(self, samples: List[Dict[str, Any]]) -> Dict[str, Any]:

        template: Dict = {
            "input_ids": [],
            "labels": [],
            "attentions": [],
            "images": [],
            "token_type_ids": [],
            "source": self.source
        }

        for sample in samples:

            template["input_ids"].append(torch.LongTensor(sample["input_id"]).transpose(0, 1))
            template["attentions"].append(torch.LongTensor(sample["attention"]).transpose(0, 1))
            template["token_type_ids"].append(torch.LongTensor(sample["token_type_id"]).transpose(0, 1))
            if sample["image"] is not None:
                template["images"].append(sample["image"])
            if sample["label"] is not None:
                template["labels"].append(sample["label"])

        template["input_ids"] = pad_sequence(template["input_ids"], batch_first=True).transpose(1, 2)
        template["attentions"] = pad_sequence(template["attentions"], batch_first=True).transpose(1, 2)
        template["token_type_ids"] = pad_sequence(template["token_type_ids"], batch_first=True).transpose(1, 2)

        template["input_ids"] = template["input_ids"][..., :self.max_seq_len]
        template["attentions"] = template["attentions"][..., :self.max_seq_len]
        template["token_type_ids"] = template["token_type_ids"][..., :self.max_seq_len]

        template["images"] = torch.stack(template["images"]) if template["images"] else None

        if template["labels"] != []:
            template["labels"] = torch.LongTensor(template["labels"])
        if self.mlm == True:
            batch_size, num_choice, seq_length = template["input_ids"].shape
            template["input_ids"], template["labels"] = self.mask_tokens(
                template["input_ids"].reshape(-1, seq_length))
            template["input_ids"] = template["input_ids"].reshape(batch_size, num_choice, seq_length)
            template["labels"] = template["labels"].reshape(batch_size, num_choice, seq_length)

        return template

    def mask_tokens(self, input_ids):
        labels = input_ids.clone()
        probability_matrix = torch.full(labels.shape, self.mlm_probability)
        special_tokens_mask = [self.tokenizer.get_special_tokens_mask(val, already_has_special_tokens=True) for val in labels.tolist()]
        probability_matrix.masked_fill_(torch.tensor(special_tokens_mask, dtype=torch.bool), value=0.0)
        masked_indices = torch.bernoulli(probability_matrix).bool()
        labels[~masked_indices] = -1  # We only compute loss on masked tokens

        # 80% of the time, we replace masked input tokens with tokenizer.mask_token ([MASK])
        indices_replaced = torch.bernoulli(torch.full(labels.shape, 0.8)).bool() & masked_indices
        input_ids[indices_replaced] = self.tokenizer.mask_token_id

        # 10% of the time, we replace masked input tokens with random word
        indices_random = torch.bernoulli(torch.full(labels.shape, 0.5)).bool() & masked_indices & ~indices_replaced
        random_words = torch.randint(len(self.tokenizer), labels.shape, dtype=torch.long)
        input_ids[indices_random] = random_words[indices_random]

        # The rest of the time (10% of the time) we keep the masked input tokens unchanged
        return input_ids, labels

    @classmethod
    def uncollate_fn(cls, samples: List):

        assert len(samples) == 1

        return samples[0]


class TextDataset(Dataset):

    def __init__(self, path: Union[Path, str], config: Configuration, renderers: List[Renderer], is_train=True, parallel=True):

        with open(path) as f:
            if parallel:
                samples = parallel_map(config.transform, f.readlines(), ordered=is_train)
            else:
                samples = list(map(config.transform, f.readlines()))
            rendered_samples = samples
            for renderer in renderers:
                rendered_samples = renderer.render(rendered_samples, parallel)

        self.data: List = rendered_samples

    def __len__(self):

        return len(self.data)

    def __getitem__(self, index):

        return self.data[index]


class VideoDataset(Dataset):

    def __init__(self, path: Union[Path, str], config: Configuration, renderers: List[Renderer], is_train=True, parallel=True):

        with open(path) as f:
            if parallel:
                samples = parallel_map(config.transform, json.loads(f.read()), ordered=is_train)
            else:
                samples = list(map(config.transform, json.loads(f.read())))
            rendered_samples = samples
            for renderer in renderers:
                rendered_samples = renderer.render(rendered_samples, parallel)

        self.data: List = rendered_samples

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]


class MultiTaskDataset(Dataset):

    def __init__(self, dataloaders, shuffle: bool = True):

        self.data: List = []

        for loader in dataloaders:
            for batch in loader:
                self.data.append(batch)
        if shuffle:
            random.shuffle(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]
