#!venv/bin/python
import utils
import sys
import os
import re
import yaml
import markdown
import pandas as pd 
import numpy as np
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity

CORPUS = "sample-content/corpus.csv"

def load_markdown_file(df, file_name):
  with open(file_name, 'r') as f:
      markdown_text = f.read()
  plain_text = markdown.markdown(markdown_text)
  clean_text = re.sub(r'\*{1,2}|_{1,2}|`{1,3}|~{1,2}|#{1,6}|[!\[\]\(\)]\([^\)]*\)|<[^>]*>', '', plain_text)
  df = df.append({
    "id": len(df)+1,
    "title": f'Markdown file {os.path.basename(file_name)}',
    "body": clean_text,
  }, ignore_index=True)
  return df

def load_openapi_file(df, file_name):
  with open(file_name, 'r') as f:
    yaml_content = f.read()
  yaml_content = re.sub(r"[\n\t]", " ", yaml_content)
  yaml_content = re.sub(r"\s{2,}", " ", yaml_content)

  df = df.append({
    "id": len(df)+1,
    "title": f'OpenAPI spec {os.path.basename(file_name)}',
    "body": yaml_content,
  }, ignore_index=True)
  return df

def load_csv_file(df, file_name): 
  # load csv file with columns id, title, body
  temp_df = pd.read_csv(file_name)
  df = df.append(temp_df, ignore_index=True)
  return df

def create_and_save_embeddings(output_file):
  df = pd.DataFrame(columns=['id', 'title', 'body'])
  with open("corpus_source_files.txt", "r") as f:
    for line in f:
        file_name = line.strip() 
        if file_name[0] == '#':
          # source files that are commented out will be skipped
          continue

        ext = os.path.splitext(file_name)[1]
        if ext == '.csv':
          df = load_csv_file(df, file_name)
        elif ext == ".md":
          df = load_markdown_file(df, file_name)
        elif ext == ".yaml":
          df = load_openapi_file(df, file_name)
        else:
          print(f"file type not supported: {file_name}")
  print(df)

  df["raw"] = (
      "Title: " + df.title.str.strip() + "; Body: " + df.body.str.strip()
  )

  df['embedding'] = df.raw.apply(lambda x: utils.get_embedding(x, model='text-embedding-ada-002'))
  df.to_csv(output_file, index=False)


create_and_save_embeddings(CORPUS)
