import os
import numpy as np
import pandas as pd
import streamlit as st      # streamlit run app/app.py
import joblib
from preprocessing import encode_sleep_quality, encode_facility_rating, encode_exam_difficulty, generate_course_diff_column

model = joblib.load( 'artifacts/svm_pipeline.pkl' )
st.set_page_config( 'Exam Score Prediction', ':book:', 'wide' )

st.markdown( '<h1 style = "font-size:50px;color:green;font-family:times new roman;" >Exam Score Prediction using ML</h1>', unsafe_allow_html=True )

df = pd.read_csv( 'data/feature eng data/feature_eng_data.csv' )

box_11, box_12, box_13, box_14 =   st.columns( 4 )


# Row 1
gender = box_11.selectbox( 'Gender',
             options = df['gender'].unique())

course = box_12.selectbox( 'Course',
             options = df['course'].unique())

study_hours = box_13.slider( 'Study Hours',
          min_value= df['study_hours'].min(),
          max_value= df['study_hours'].max())

class_attendance = box_14.slider( 'class_attendance',
          min_value= df['class_attendance'].min(),
          max_value= df['class_attendance'].max())


box_21, box_22, box_23, box_24 =   st.columns( 4 )

internet_access = box_21.selectbox( 'internet_access',
             options = df['internet_access'].unique())

sleep_hours = box_22.slider( 'sleep_hours',
              min_value= df['sleep_hours'].min(),
              max_value= df['sleep_hours'].max())

sleep_quality = box_23.selectbox( 'sleep_quality',
          options = df['sleep_quality'].unique())

study_method = box_24.selectbox( 'study_method',
          options = df['study_method'].unique())


box_31, box_32 =   st.columns( 2 )

facility_rating = box_31.selectbox( 'facility_rating',
          options = df['facility_rating'].unique())

exam_difficulty = box_32.selectbox( 'exam_difficulty',
          options = df['exam_difficulty'].unique())

# Store user data in a row of 10 columns ----> shape -> ( 1, 10 )
data = pd.DataFrame( 
    [ [ gender, course, study_hours, class_attendance, internet_access,
       sleep_hours, sleep_quality, study_method, facility_rating, exam_difficulty ] ],
    columns = ['gender', 'course', 'study_hours', 'class_attendance',
       'internet_access', 'sleep_hours', 'sleep_quality', 'study_method',
       'facility_rating', 'exam_difficulty',]
)

# 1) generate course_diff
# 2) apply 3 function to perform label encoding

data = generate_course_diff_column( data )

data = encode_sleep_quality( data )
data = encode_facility_rating( data )
data = encode_exam_difficulty( data )

prediction = model.predict( data )[0]
prediction = round( prediction, 1 )

if prediction >= 50 :
   st.write( f'<h2 style = "color:green;" > {prediction} PASS ! </h2>', unsafe_allow_html=True )
   
else :
   st.write( f'<h2 style = "color:red;" > {prediction} FAIL ! </h2>', unsafe_allow_html=True )   