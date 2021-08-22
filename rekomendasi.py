# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 18:21:46 2021

@author: ROG
"""


#import beberapa library yang digunakan
import pandas as pd
from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
from sklearn.metrics.pairwise import cosine_distances
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer

#inisialisasi objek Flask
app = Flask(__name__)

#inisialisasi objek restful
api = Api(app)

#inisialisasi objek cors
CORS(app)

df = pd.read_csv("dataset/IMDb movies.csv", low_memory=False)
df.loc[df["year"] == "TV Movie 2019", "year"] = "2019"
df["year"] = df["year"].astype("int")
df.dropna(subset=["description"], inplace=True)

#buat bow untuk encode deksripsi
bow = CountVectorizer(stop_words="english", tokenizer=word_tokenize)
bank = bow.fit_transform(df["description"])

class RekomendasiHome(Resource):
    def get(self):
        rekomen = df[(df["year"] > 2019) & (df["avg_vote"] > 9)].sort_values(by="avg_vote", ascending=False).head(10)
        return rekomen.to_json(orient="records")
    
class Rekomendasikonten(Resource):
    def post(self):
        user_imdb_title_id = request.form["id_film_user"]
        konten = df.loc[df["imdb_title_id"] == user_imdb_title_id, "description"]
        code = bow.transform(konten)
        distance = cosine_distances(code, bank)
        rec_idx = distance.argsort()[0, 1:11]
        hasil_rekomendasi = df.loc[rec_idx]
        return hasil_rekomendasi.to_json(orient="records")
    
#setup api routing
api.add_resource(RekomendasiHome, "/halamanutama", methods=["GET"])
api.add_resource(Rekomendasikonten, "/konten", methods=["POST"])

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5005)