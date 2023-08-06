# Textbook: Universal NLP Datasets

## Dependency

- `av==6.2.0`
- `jsonnet==0.14.0`
- `opencv_python==4.1.1.26`
- `torch==1.3.1`
- `torchvision==0.4.2`
- `numpy==1.17.4`
- `transformers=2.1.1`

## Download raw datasets

```bash
bash fetch.sh
```

It downloads `alphanli`, `hellaswag`, `physicaliqa` and `socialiqa` from AWS.
In case you want to use something-something, pelase download the dataset from 20bn's website

## Usage

```python
from transformers import BertTokenizer
from textbook import *

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
text_renderer = TextRenderer(tokenizer)

anli_tool = BatchTool(tokenizer, max_seq_len=128, source="anli")
anli_dataset = TextDataset(path='data_cache/alphanli/eval.jsonl',
                            config=ANLIConfiguration(), renderers=[text_renderer])
anli_iter = DataLoader(anli_dataset, batch_size=2, collate_fn=anli_tool.collate_fn)

hellaswag_tool = BatchTool(tokenizer, max_seq_len=128, source="hellaswag")
hellaswag_dataset = TextDataset(path='data_cache/hellaswag/eval.jsonl',
                                config=HellaswagConfiguration(), renderers=[text_renderer])
hellaswag_iter = DataLoader(hellaswag_dataset, batch_size=2, collate_fn=hellaswag_tool.collate_fn)

siqa_tool = BatchTool(tokenizer, max_seq_len=128, source="siqa")
siqa_dataset = TextDataset(path='data_cache/socialiqa/eval.jsonl',
                            config=SIQAConfiguration(), renderers=[text_renderer])
siqa_iter = DataLoader(siqa_dataset, batch_size=2, collate_fn=siqa_tool.collate_fn)

piqa_tool = BatchTool(tokenizer, max_seq_len=128, source="piqa")
piqa_dataset = TextDataset(path='data_cache/physicaliqa/eval.jsonl',
                            config=PIQAConfiguration(), renderers=[text_renderer])
piqa_iter = DataLoader(piqa_dataset, batch_size=2, collate_fn=piqa_tool.collate_fn)

# video_renderer = VideoRenderer(data_dir="data_cache/smthsmth/20bn-something-something-v2")
# smth_tool = BatchTool(tokenizer, max_seq_len=128, source="smth", mlm=True)
# smth_config = SMTHSMTHConfiguration()
# smth_dataset = VideoDataset("data_cache/smthsmth/something-something-v2-validation.json",
#                             smth_config, [text_renderer, video_renderer])
# smth_iter = DataLoader(smth_dataset, batch_size=2, collate_fn=smth_tool.uncollate_fn)

dataset = MultiTaskDataset([anli_iter, hellaswag_iter, siqa_iter, piqa_iter], shuffle=True)

for batch in tqdm(DataLoader(dataset, batch_size=1, collate_fn=BatchTool.uncollate_fn)):

    pass
```
