from flask import Flask, render_template, request
import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user= "root",
    password = "SQL12345#",
    database = "PEOPLE_FAIR"
)

mycursor = db.cursor()
# mycursor.execute("CREATE TABLE DATA (NAME VARCHAR(50), age smallint UNSIGNED , personID int PRIMARY KEY AUTO_INCREMENT ,  )")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def diabetes_risk_checker():
    if request.method == "POST":
        try:
            # Collect form data
            name = request.form.get("name", "").strip()
            age = int(request.form.get("age", 0))
            waist_circumference = int(request.form.get("waist_circumference", 0))
            physical_activity = request.form.get("physical_activity", "").upper()
            family_history = request.form.get("family_history", "").upper()
            gender = request.form.get("gender", "").upper()
            mycursor.execute("INSERT INTO DATA (NAME,age,Waist,Gender,Family) VALUES (%s, %s, %s, %s, %s)" , (name,age,waist_circumference,gender,family_history))
            db.commit()

            with open("USERS.txt", "a") as f:
                f.write(f"Name: {name}, Age: {age}, Waist: {waist_circumference}, Family: {family_history} , Gender : {gender}\n")


            # Validate inputs
            if not (name and age and waist_circumference and physical_activity and family_history and gender):
                raise ValueError("Missing fields")

            # Initialize score
            score = 0

            # Age Scoring
            if age < 35:
                score += 0
            elif 35 <= age <= 49:
                score += 20
            else:
                score += 30

            # Abdominal Obesity Scoring
            if gender == "MALE":
                if waist_circumference < 90:
                    score += 0
                elif 90 <= waist_circumference <= 99:
                    score += 10
                else:  # > 100
                    score += 20
            elif gender == "FEMALE":
                if waist_circumference < 80:
                    score += 0
                elif 80 <= waist_circumference <= 89:
                    score += 10
                else:  # > 90
                    score += 20

            # Physical Activity Scoring
            if physical_activity == "H":
                score += 0
            elif physical_activity == "M":
                score += 20
            else:
                score += 30

            # Family History Scoring
            if family_history == "N":
                score += 0
            elif family_history == "M":
                score += 10
            else:
                score += 20

            # Assessment based on score
            if score <= 20:
                risk = "Low Risk"
            elif 21 <= score <= 50:
                risk = "Moderate Risk"
            else:
                risk = "High Risk"

            return render_template("result.html", name=name, score=score, risk=risk)
        except ValueError:
            return render_template("ndex.html", error="Invalid input. Please check your data.")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5500)

