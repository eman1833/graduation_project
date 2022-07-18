from ast import Not
import sys
from sys import path
from unittest import result
from flask import (
    Flask,
    redirect,
    url_for,
    render_template,
    request,
    jsonify,
    flash,
    json,
)
from sqlalchemy import false
from flask_restful import Resource, Api
import pickle
import pandas as pd
from flask_cors import CORS
import numpy as np
import joblib
import sklearn
import keras
from keras.utils import load_img
import tensorflow
from keras.models import load_model

app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///patient_progict2.db"
# app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://kyyzppwvaovkjz:cfabd755a9edaadb0b3523c0ee144d4edcb9b4d7fb06836905c88b0b60b54998@ec2-52-205-61-230.compute-1.amazonaws.com:5432/d74m70novnouqt'

db = SQLAlchemy(app)


class Patient(db.Model):
    #  yellowing_of_the_whites_of_the_eyes=db.Column(db.String)
    #  yellowing_of_the_whites_of_the_eyes

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=false)
    age = db.Column(db.String)
    phone = db.Column(db.Integer)
    AFP = db.Column(db.Integer)
    MCV = db.Column(db.Integer)
    Albumin = db.Column(db.Integer)
    Platelets = db.Column(db.Integer)
    ALP = db.Column(db.Integer)
    Iron = db.Column(db.Integer)
    result = db.Column(db.Integer)


model = joblib.load(r"C:\Users\fagr\Downloads\Telegram Desktop\rf_model.pickle")
# img_model=pickle.load(open(r'C:\Users\fagr\Downloads\Telegram Desktop\model.sav','rb'))

# "AFP":"95",
# "MCV":"150",
# "Albumin":"3.4",
# "Platelets":"99",
# "ALP":"150",
# "Iron":"52.5"
#  result1=db.Column(db.Integer)
def __repr__(self):
    return f"""{self.yellowing_of_the_whites_of_the_eyes}{self.Anorexia}
        {self.A_mass_in_the_flank_of_the_abdomen}{self.Yellowing_of_the_skin}{self. Unexplained_weight_loss}
        {self.name}-{self.age}-{self.phone}{self.AFP}
        {self.MCV}{self.Albumin}{self.Platelets}
        {self.ALP}{self.Iron}{self.result}
        """


admins = ["0109200"]


def patient_result(AFP, MCV, Albumin, Platelets, ALP, Iron):
    data = {
        "AFP": AFP,
        "MCV": MCV,
        "Albumin": Albumin,
        "Platelets": Platelets,
        "ALP": ALP,
        "Iron": Iron,
    }
    query_df = pd.DataFrame(data)
    pationt_result = model.predict(query_df)
    return pationt_result


@app.route("/", methods=["POST", "GET"])
def home():
    admin_id = "0109200"
    # user_name="eman318"
    # id = request.form["id"]
    if request.method == "POST":
        if request.form["id"] in admins:
            return render_template("admin.html")
        else:

            return redirect(url_for("get_pat", id=request.form["id"]))


@app.route("/patient")
def get_id():
    patients = Patient.query.all()
    output = []
    for patient in patients:
        pat_data = {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "phone": patient.phone,
            "AFP": patient.AFP,
            "MCV": patient.MCV,
            "Albumin": patient.Albumin,
            "Platelets": patient.Platelets,
            "ALP": patient.ALP,
            "Iron": patient.Iron,
            "result": patient.result,
        }
        output.append(pat_data)
    return {"patients": output}


@app.route("/patient/<id>", methods=["GET"])
def get_pat(id):
    patient = Patient.query.get(id)
    if patient is None:
        return {"error": "not found"}
    else:
        return {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "phone": patient.phone,
            "AFP": patient.AFP,
            "MCV": patient.MCV,
            "Albumin": patient.Albumin,
            "Platelets": patient.Platelets,
            "ALP": patient.ALP,
            "Iron": patient.Iron,
            "result": patient.result,
        }


@app.route("/check", methods=["POST"])
def check_pat():
    counter = 0
    # id=request.json['id']

    # patient=Patient.query.get(id)
    if request.method == "POST":

        # if patient is None:
        yellowing_of_the_whites_of_the_eyes = request.json[
            "yellowing_of_the_whites_of_the_eyes"
        ]
        if yellowing_of_the_whites_of_the_eyes == True:
            counter += 1

        else:
            counter

        Anorexia = request.json["Anorexia"]
        if Anorexia == True:
            counter += 1
            counter
        else:
            counter
        A_mass_in_the_flank_of_the_abdomen = request.json[
            "A_mass_in_the_flank_of_the_abdomen"
        ]
        if A_mass_in_the_flank_of_the_abdomen == True:
            counter += 1
            counter
        else:
            counter
        Yellowing_of_the_skin = request.json["Yellowing_of_the_skin"]
        if Yellowing_of_the_skin == True:
            counter += 1

        else:
            counter
        Unexplained_weight_loss = request.json["Unexplained_weight_loss"]
        if Unexplained_weight_loss == True:
            counter += 1

        else:
            counter
        print(counter)
        if counter >= 3:
            return {"massage": "do this analysis MCV,ALP,AFP,Albumin,Platelets,Iron"}

        else:
            return {"massage": "not patient "}


@app.route("/patient", methods=["POST"])
def add_pat():
    id = request.json["id"]
    patient = Patient.query.get(id)
    if request.method == "POST":
        admin_id = request.json["admin_id"]
        if patient is None:
            AFP = request.json["AFP"]
            MCV = request.json["MCV"]
            Albumin = request.json["Albumin"]
            Platelets = request.json["Platelets"]
            ALP = request.json["ALP"]
            Iron = request.json["Iron"]
            result = patient_result(AFP, MCV, Albumin, Platelets, ALP, Iron)
            if admin_id in admins:
                patient = Patient(
                    id=request.json["id"],
                    name=request.json["name"],
                    age=request.json["age"],
                    phone=request.json["phone"],
                    AFP=request.json["AFP"],
                    MCV=request.json["MCV"],
                    Albumin=request.json["Albumin"],
                    Platelets=request.json["Platelets"],
                    ALP=request.json["ALP"],
                    Iron=request.json["Iron"],
                    result=result,
                )

                db.session.add(patient)
                db.session.commit()

                return {"id": patient.id, "massage": "the patient is added"}
            else:
                return {"massage": "please enter a valid admin id"}

        else:
            return {"error": "already  found"}


# @app.route("/prediction",methods=['POST'])
# def prediction():
#       json_=request.json
#       query_df=pd.DataFrame(json_)
#       prediction=model.predict(query_df)
#       return jsonify({"prediction":list(prediction)})

# @app.route("/img_prediction", methods=["POST"])
# def img_prediction():
#     image=request.files['img']
#     image=keras.utils.load_img( path ,target_size=(200,200))
#     image=keras.utils.img_to_array(image)
#     image=np.expand_dims(image,axis=0)
#     label=img_model.predict(image)
#     return label


@app.route("/patient/<id>", methods=["DELETE"])
def delete_pat(id):
    patient = Patient.query.get(id)
    if patient is None:
        return {"error": "not found"}
    db.session.delete(patient)
    db.session.commit()
    return {"massage": "the patient is deleted"}


@app.route("/patient/<id>", methods=["PUT"])
def updata_pat(id):
    patient = Patient.query.get(id)
    if patient is None:
        return {"error": "not found"}
    else:
        id = request.json["id"]
        name = request.json["name"]
        age = request.json["age"]
        phone = request.json["phone"]
        AFP = request.json["AFP"]
        MCV = request.json["MCV"]
        Albumin = request.json["Albumin"]
        Platelets = request.json["Platelets"]
        ALP = request.json["ALP"]
        Iron = request.json["Iron"]
        # patient.id=id
        result = patient_result(AFP, MCV, Albumin, Platelets, ALP, Iron)
        patient.name = name
        patient.age = age
        patient.phone = phone

        patient.AFP = AFP
        patient.MCV = MCV
        patient.Albumin = Albumin
        patient.Platelets = Platelets
        patient.ALP = ALP
        patient.Iron = Iron
        patient.result = result
        # db.session.updata(drink)
        db.session.commit()
        # return{'id':patient.id,'name':patient.name,'age':patient.age}
        return {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "phone": patient.phone,
            "AFP": patient.AFP,
            "MCV": patient.MCV,
            "Albumin": patient.Albumin,
            "Platelets": patient.Platelets,
            "ALP": patient.ALP,
            "Iron": patient.Iron,
            "result": result,
            "massage": "the patient is updated",
        }


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=9000)
