from flask import Flask, request, render_template, jsonify
import pandas as pd 
from query_corpus import *

app = Flask(__name__, static_url_path='/static')

CORPUS = "sample-content/corpus.csv"
df = pd.read_csv(CORPUS)
df['embedding'] = df.embedding.apply(eval).apply(np.array)

# Define the first endpoint
@app.route("/")
def index():
    return render_template("index.html")

# Define the second endpoint
@app.route("/query", methods=["POST"])
def query():
    prompt = request.json["prompt"]
    seds = generate_sorted_embedding_distances_from_prompt(df, prompt, n=3)
    context = generate_context_from_seds(seds, prompt)
    answer = issue_query(context, prompt)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7777)