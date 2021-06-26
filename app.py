from flask import Flask, render_template, request
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))


@app.route("/", methods=["GET"])
def Home():
    return render_template("site.html")


standard_to = StandardScaler()


@app.route("/predict", methods=["POST"])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == "POST":
        Year = int(request.form["Year"])
        car_age = 2021 - Year

        km_driven = int(request.form["Distance Driven"])
        seats = float(request.form["Seating Capacity"])
        mileage_num = float(request.form["Mileage"])
        engine_num = float(request.form["Engine CC"])
        max_power_num = float(request.form["Power HP"])

        owner = request.form["Owner"]
        if owner == "First Owner":
            owner_Second_Owner = 0
            owner_Third_Owner = 0
            owner_Test_Drive_Car = 0
            owner_Fourth_Above_Owner = 0
        if owner == "Second Owner":
            owner_Second_Owner = 1
            owner_Third_Owner = 0
            owner_Test_Drive_Car = 0
            owner_Fourth_Above_Owner = 0
        if owner == "Third Owner":
            owner_Second_Owner = 0
            owner_Third_Owner = 1
            owner_Test_Drive_Car = 0
            owner_Fourth_Above_Owner = 0
        if owner == "Fourth Owner":
            owner_Second_Owner = 0
            owner_Third_Owner = 0
            owner_Test_Drive_Car = 0
            owner_Fourth_Above_Owner = 1
        else:
            owner_Second_Owner = 0
            owner_Third_Owner = 0
            owner_Test_Drive_Car = 1
            owner_Fourth_Above_Owner = 0

        Fuel_Type = request.form["Fuel Type"]
        if Fuel_Type == "Petrol":
            fuel_Petrol = 1
            fuel_Diesel = 0
            fuel_LPG = 0
        elif Fuel_Type == "Diesel":
            fuel_Petrol = 0
            fuel_Diesel = 1
            fuel_LPG = 0
        elif Fuel_Type == "CNG":
            fuel_Petrol = 0
            fuel_Diesel = 0
            fuel_LPG = 0
        else:
            fuel_Petrol = 0
            fuel_Diesel = 0
            fuel_LPG = 1

        Seller_type = request.form["Seller Type"]
        if Seller_type == "Individual":
            seller_type_Individual = 1
            seller_type_Trustmark_Dealer = 0
        if Seller_type == "Dealer":
            seller_type_Individual = 0
            seller_type_Trustmark_Dealer = 0
        if Seller_type == "Trustmark Dealer":
            seller_type_Individual = 0
            seller_type_Trustmark_Dealer = 1

        transmission_Manual = request.form["Transmission Type"]
        if transmission_Manual == "Manual":
            transmission_Manual = 1
        else:
            transmission_Manual = 0

        predict_array = [
            km_driven,
            seats,
            car_age,
            mileage_num,
            engine_num,
            fuel_Diesel,
            fuel_LPG,
            fuel_Petrol,
            seller_type_Individual,
            seller_type_Trustmark_Dealer,
            transmission_Manual,
            owner_Fourth_Above_Owner,
            owner_Second_Owner,
            owner_Test_Drive_Car,
            owner_Third_Owner,
        ]
        prediction = model.predict([predict_array])
        output = prediction[0]

        return render_template(
            "site.html",
            prediction_text="Your car is estimated to sell at {}".format(output),
        )

    else:
        return render_template("site.html")


if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)
