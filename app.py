import numpy as np
import mysql.connector
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

#Load the machine learning model

import pickle
model = pickle.load(open('diabetic.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        no=float(request.form.get('ENTER ANY NO',0.0))
        age = float(request.form.get('AGE', 0.0))
        hypertension = float(request.form.get('HYPERTENSION', 0.0))
        heartdisease = float(request.form.get('HEART DISEASE', 0.0))
        bmi = float(request.form.get('BODY MASS INDEX (BMI)', 0.0))
        hba1c_level = float(request.form.get('HbA1c LEVEL', 0.0))
        glucose_level = float(request.form.get('BLOOD GLUCOSE LEVEL', 0.0))
        gender_male = float(request.form.get('GENDER MALE', 0.0))
        gender_female = float(request.form.get('GENDER FEMALE', 0.0))
        smoke_ever = float(request.form.get('SMOKE EVER', 0.0))
        smoke_former = float(request.form.get('SMOKE FORMER', 0.0))
        smoke_never = float(request.form.get('SMOKE NEVER', 0.0))
        smoke_current = float(request.form.get('SMOKE CURRENT', 0.0))
        
        input_features = np.array([[
            no,age, hypertension, heartdisease, bmi, hba1c_level, glucose_level,
            gender_male, gender_female, smoke_ever, smoke_former, smoke_never, smoke_current
        ]])
        
        #Storing data to Database

      

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Surya@4646",
        database="diabetis_prediction"
        )

        mycursor = mydb.cursor()
        #sql=" Insert into "
        sql = "INSERT INTO diabetis_prediction(NO, AGE,HYPERTENSION,HEARTDISEASE, BODYMASSINDEX,HbA1c,BLOODGLUCOSELEVEL, GENDERMALE,GENDERFEMALE,SMOKEEVER,SMOKEFORMER, SMOKENEVER, SMOKECURRENT) values(no,age,hypertension,heartdisease,bmi,hba1c_level,glucose_level,gender_male, gender_female,smoke_ever,smoke_former,smoke_never, smoke_current)"
        #val = ("John", "Highway 21")
        mycursor.execute(sql)

        mydb.commit()

        prediction = model.predict(input_features.reshape(1, -1))
        return redirect(url_for('show_result', result=int(prediction[0])))
    return render_template('index.html')

@app.route('/result/<result>')
def show_result(result):
    return render_template('name.html', prediction_text=int(result))

if __name__ == '__main__':
    app.run(debug=True)
