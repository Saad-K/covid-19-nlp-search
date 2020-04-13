import os
import pickle
from typing import List

import pandas as pd
import scipy.spatial
import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger
from sentence_transformers import SentenceTransformer

app = FastAPI(title="COVID-19 AI")

NUM_OF_RESULTS = 5
DATA_DIR = os.path.join(os.getcwd(), "data")

covid_sentences_df = pd.read_csv(os.path.join(DATA_DIR, "covid_sentences.csv"), index_col=0)
covid_full_sentences_df = pd.read_csv(
    os.path.join(DATA_DIR, "covid_full_sentences.csv"), index_col=0
)

df_sentences = covid_sentences_df["paper_id"].to_dict()
df_sentences_list = list(df_sentences.keys())

# Convert everything to string and that's our sentence text corpus
corpus = [str(d) for d in df_sentences_list]

corpus_embeddings = pickle.load(open(os.path.join(DATA_DIR, "corpus_embeddings_base_2.pkl"), "rb"))

embedder = SentenceTransformer("bert-base-nli-stsb-mean-tokens")

logger.info("--- Finished Loading All Files --- Accepting Requests Now")


@app.get("/")
async def read_root():
    return {"app_name": "COVID-19 AI"}


async def calculate_cosine_similarity(question_embedding):
    distances = scipy.spatial.distance.cdist([question_embedding], corpus_embeddings, "cosine")[0]

    return distances


@app.post("/predict")
async def predict(questions: List[str]):

    logger.info(f"Questions: {questions}")
    logger.info("Questions Embeddings Started")
    question_embeddings = embedder.encode(questions, show_progress_bar=True)
    logger.info("Questions Embedding Finished")

    logger.info(" Displaying the top 5 closest set of sentences to the question:")
    for question, question_embedding in zip(questions, question_embeddings):

        distances = await calculate_cosine_similarity(question_embedding)

        sorted_distances = sorted(zip(range(len(distances)), distances), key=lambda x: x[1])

        results = []
        for idx, distance in sorted_distances[0:NUM_OF_RESULTS]:
            row_dict = covid_full_sentences_df.loc[
                covid_full_sentences_df.index == corpus[idx]
            ].to_dict()

            paper_info = {
                "score": f"{1 - distance:.4f}",
                "set_of_sentences": f"{corpus[idx].strip()}",
                "paper_id": f'{row_dict["paper_id"][corpus[idx]]}',
                "title": f'{row_dict["title"][corpus[idx]]}',
                "abstract": f'{row_dict["abstract"][corpus[idx]]}',
                "abstract_summary": f'{row_dict["abstract_summary"][corpus[idx]]}',
            }

            results.append(paper_info)

    logger.info(results)

    return results
