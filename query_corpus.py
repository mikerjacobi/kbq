#!venv/bin/python
import sys
import utils
import pandas as pd 
import numpy as np
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity

CORPUS = "sample-content/corpus.csv"
df = pd.read_csv(CORPUS)
df['embedding'] = df.embedding.apply(eval).apply(np.array)

def generate_sorted_embedding_distances_from_prompt(df, prompt, n=3):
   embedding = utils.get_embedding(prompt, model='text-embedding-ada-002')
   df['similarities'] = df.embedding.apply(lambda x: cosine_similarity(x, embedding))
   res = df.sort_values('similarities', ascending=False).head(n)
   return res

def generate_context_from_seds(seds, prompt):
  returns = []
  cur_len, max_len = 0, 2000

  for i, row in seds.iterrows():
      cur_len += len(row['raw'])
      if cur_len > max_len:
          break
      returns.append(row["raw"])
  return "\n\n###\n\n".join(returns)

def answer(
    context,
    prompt,
    model="text-davinci-003",
    max_len=1800,
    size="ada",
    max_tokens=1500,
    stop_sequence=None
):
  try:
    response = openai.Completion.create(
      prompt=f"""
Using the information provided in the context below, please answer the following question to the best of your ability. 
If the necessary information is not present or if the question is not applicable to the context, please respond with "I don't know".
If code is included in the response, please provide an explanation of the code's purpose and how it relates to the question at hand.

###

Context: {context}

###

Prompt: {prompt}

###

Answer:
""",
      temperature=1.0,
      max_tokens=max_tokens,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=stop_sequence,
      model=model,
    )
    return response["choices"][0]["text"].strip()
  except Exception as e:
    print(e)
    return ""

#prompt = 'what temperature water should you put eggs in when you boil them?' 
prompt = sys.argv[1]
seds = generate_sorted_embedding_distances_from_prompt(df, prompt, n=3)
context = generate_context_from_seds(seds, prompt)
resp = answer(context, prompt)
print(resp)
