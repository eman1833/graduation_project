import joblib
import pandas as pd
from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import false

app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///patient_progict8.db"
# app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://kyyzppwvaovkjz:cfabd755a9edaadb0b3523c0ee144d4edcb9b4d7fb06836905c88b0b60b54998@ec2-52-205-61-230.compute-1.amazonaws.com:5432/d74m70novnouqt'

db = SQLAlchemy(app)


class Patient(db.Model):
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
    prediction = db.Column(db.Integer)


model = joblib.load(r"C:\Users\fagr\Downloads\Telegram Desktop\rf_model.pickle")


def __repr__(self):
    return f"""{self.yellowing_of_the_whites_of_the_eyes}{self.Anorexia}
        {self.A_mass_in_the_flank_of_the_abdomen}{self.Yellowing_of_the_skin}{self. Unexplained_weight_loss}
        {self.name}-{self.age}-{self.phone}{self.AFP}
        {self.MCV}{self.Albumin}{self.Platelets}
        {self.ALP}{self.Iron}{self.prediction}
        """


admins = ["0109200"]


def patient_result(AFP, MCV, Albumin, Platelets, ALP, Iron):
    data = [
        {
            "AFP": AFP,
            "MCV": MCV,
            "Albumin": Albumin,
            "Platelets": Platelets,
            "ALP": ALP,
            "Iron": Iron,
        }
    ]

    query_df = pd.DataFrame(data)
    prediction = model.predict(query_df)
    return prediction[0]


@app.route("/", methods=["POST", "GET"])
def home():
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
            "prediction": patient.prediction,
        }
        output.append(pat_data)
    return {"patients": output}


@app.route("/check", methods=["POST"])
def check_pat():
    counter = 0
    if request.method == "POST":

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
            prediction = patient_result(AFP, MCV, Albumin, Platelets, ALP, Iron)
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
                    prediction=prediction,
                )

                db.session.add(patient)
                db.session.commit()

                return {"id": patient.id, "massage": "the patient is added"}
            else:
                return {"massage": "please enter a valid admin id"}

        else:
            return {"error": "already  found"}


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
        prediction = patient_result(AFP, MCV, Albumin, Platelets, ALP, Iron)
        patient.name = name
        patient.age = age
        patient.phone = phone

        patient.AFP = AFP
        patient.MCV = MCV
        patient.Albumin = Albumin
        patient.Platelets = Platelets
        patient.ALP = ALP
        patient.Iron = Iron
        patient.prediction = prediction
        db.session.commit()
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
            "prediction": prediction,
            "massage": "the patient is updated",
        }


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
            "prediction": patient.prediction,
        }


@app.route("/patient/<id>", methods=["DELETE"])
def delete_pat(id):
    patient = Patient.query.get(id)
    if patient is None:
        return {"error": "not found"}
    db.session.delete(patient)
    db.session.commit()
    return {"massage": "the patient is deleted"}


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=9000)
