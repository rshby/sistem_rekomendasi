from flask import Flask, request
from sklearn.metrics.pairwise import cosine_distances
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("dataset/IMDb movies.csv")
df.loc[df["year"] == "TV Movie 2019", "year"] = "2019"
df["year"] = df["year"].astype("int")

df.dropna(subset=["description"], inplace=True)

bow = CountVectorizer(stop_words="english", tokenizer=word_tokenize)
bank = bow.fit_transform(df["description"])


@app.route("/rekomendasi")
def rekomendasi():
    rekomen = df[(df["year"] > 2019) & (df["avg_vote"] > 9)].sort_values(
        by="avg_vote", ascending=False).head(10).to_json(orient="records")
    return rekomen


@app.route("/onpage", methods=["POST"])
def onpage():
    user_imdb_title_id = request.form["id_film_user"]
    konten = df.reindex(columns=["description"], index=df[df["imdb_title_id"] == user_imdb_title_id].index)["description"]
    code = bow.transform(konten)
    distance = cosine_distances(code, bank)
    rec_idx = distance.argsort()[0, 1:11]
    hasil_rekomendasi = df.reindex(index=rec_idx).to_json(orient="records")
    return hasil_rekomendasi


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
