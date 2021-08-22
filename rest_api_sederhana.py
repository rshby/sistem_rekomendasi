# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 09:58:01 2021

@author: ROG
"""


#import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_distances

#inisialiassi objek flask
app = Flask(__name__)

#inisiasi objek flask restful
api = Api(app)

#inisiasi objek flask cors
CORS(app)

#buat variabel dictionary kosongan
identitas = {}

#membuat kelas recourse
class ContohResource(Resource):
    def get(self):
        #response = {"msg" : "Haloo dunia"}
        return identitas

    def post(self):
        nama = request.form["nama"]
        umur = request.form["umur"]
        identitas["nama"] = nama
        identitas["umur"] = umur
        response = {"msg" : "OK"}
        return response
    
#setup resource
api.add_resource(ContohResource, "/api", methods=["GET", "POST"])

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5005)


