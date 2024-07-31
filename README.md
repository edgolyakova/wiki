# Project Brief
The goal was to improve the translation quality of Wikipedia articles, given an English article text. The experiments were performed for English-Mandarin Chinese and English-French language pairs.

To achieve the goal we manually verified WikiMatrix corpus and constructed a subcorpus consisiting of:
- 1887 sentence pairs for English-French language pairs
- 2007 sentence pairs for English-Chinese

This corpus was later used to create several annotation types:
- No annotation
- Word alignment between source and target sentence
- PoS annotation 
  
The annotated corpora were then used to fine-tune [OPUS-mt](https://huggingface.co/Helsinki-NLP/opus-mt-en-mt) (T5-like) models.


# Results

For French:

| Annotation type    | BLEU |
| -------- | ------- |
| No annotation  | 22.7236 |
| Part of Speech| 22.4789  |
| Word alignment: target token ids    | 31.5155|


For Chinese:
| Annotation type    | BLEU |
| -------- | ------- |
| No annotation  | 21.6963 |
| Part of Speech| 21.5432 |
| Word alignment: target token ids    | 20.4420 |
