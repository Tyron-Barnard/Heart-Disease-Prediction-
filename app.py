from streamlit_option_menu import option_menu
from ucimlrepo import fetch_ucirepo

import streamlit as st
import sqlite3
import numpy as np
import cv2
import pickle
import requests
from streamlit_lottie import st_lottie
import pandas as pd
from keras.models import load_model
from keras.applications.resnet import preprocess_input
import os
from database import init_db, create_user, authenticate_user
from utils import display_lottie_animation

# Initialize database
init_db()

# Read CSV file
df = pd.read_csv('C:/Users/tyron/Heart Care Assignment/heart.csv', delimiter=';')

# Connect to SQLite database
DB_NAME = r"C:\Users\tyron\Heart Care Assignment\app.db"
conn = sqlite3.connect(DB_NAME)

# Create table in SQLite database
df.to_sql('heart_data', conn, if_exists='replace', index=False)

# Fetch dataset
heart_disease = fetch_ucirepo(id=45)

# Data (as pandas dataframes)
X = heart_disease.data.features
y = heart_disease.data.targets

# Metadata
print(heart_disease.metadata)

# Variable information
print(heart_disease.variables)

# Configure the page settings
st.set_page_config(
    page_title="Heart Disease Diagnosis",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide the main menu and footer for a cleaner look
hide_menu_style = """
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Display the sidebar header
text = st.sidebar.error('Heart Disease Diagnosis')

# Sidebar options for login and signup
choice = st.sidebar.selectbox('LOGIN/SIGNUP', ['Login', 'Signup'])
email = st.sidebar.text_input('ENTER YOUR EMAIL ADDRESS')
password = st.sidebar.text_input('ENTER YOUR PASSWORD', type='password')

is_authenticated = False  # Variable to track authentication status

if choice == 'Signup':
    handle = st.sidebar.text_input("ENTER YOUR TITLE AND NAME")
    submit = st.sidebar.button('CREATE ACCOUNT')

    if submit:
        create_user(email, password, handle)
        st.sidebar.success('ACCOUNT CREATED SUCCESSFULLY')
        st.info(f'WELCOME -- {handle}')
        st.caption('THANKS FOR SIGNING UP, PLEASE LOGIN TO CONTINUE')

if choice == 'Login':
    login = st.sidebar.checkbox('Login')

    if login:
        user = authenticate_user(email, password)
        if user:
            is_authenticated = True
            st.sidebar.success('LOGGED IN SUCCESSFULLY')
        else:
            st.sidebar.error('Login Failed. Please check your credentials.')

# Check if the user is authenticated before displaying the main content
if is_authenticated:
    # Option menu for navigation
    selected2 = option_menu(None, ["Home", "PREDICT HEART DISEASE", 'REFERRAL TO SPECIALIST CARE'],
                            icons=['house', 'heart', "activity", 'envelope'],
                            menu_icon="cast", default_index=0, orientation="horizontal",
                            styles={
                                "container": {"padding": "0!important", "background-color": "#000000"},
                                "icon": {"color": "#149CFE", "font-size": "20px"},
                                "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px",
                                             "--hover-color": "#413839"},
                                "nav-link-selected": {"background-color": "#000000"},
                            })

    if selected2 == 'Home':
        # Display the overview section
        new_title = '<p style="font-family:Georgia; color:#149CFE; font-size: 28px; text-decoration: underline; text-decoration-color: white;">Overview of the Heart Disease Diagnosis Platform for Healthcare Providers</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.write(
            'Our Heart Disease Testing Platform equips healthcare professionals with advanced tools to evaluate and diagnose heart conditions, including coronary artery disease, efficiently. Designed with precision and ease of use in mind, this platform facilitates detailed patient assessments, enabling swift identification of potential heart-related health issues.')

        new_title = '<p style="font-family:Georgia; color:#149CFE; font-size: 28px; text-decoration: underline; text-decoration-color: white;">Lifestyle Recommendations for Patients</p>'
        st.markdown(new_title, unsafe_allow_html=True)

        # Display the lifestyle recommendations section
        st.write('🔵**Avoid Smoking and Tobacco Use:** Encourage patients to refrain from smoking and the use of tobacco products to improve cardiovascular health.')
        st.write('🔵**Manage Cholesterol, Hypertension, and Diabetes:** Regular monitoring and management of these conditions are crucial for preventing issues.')
        st.write('🔵**Heart-Healthy Diet:** Advise a diet rich in fruits, vegetables, whole grains, and lean proteins. Limit saturated fats, sugars, and salt.')
        st.write('🔵**Moderate Alcohol Consumption:** Recommend limiting alcohol intake to moderate levels.')
        st.write('🔵**Stress Management:** Teach stress reduction techniques such as meditation, yoga, or deep breathing exercises.')
        st.write('🔵**Regular Physical Activity:** Encourage at least 150 minutes of moderate aerobic activity or 75 minutes of vigorous activity each week.')
        st.write('🔵**Routine Exercise:** Suggest a daily routine of walking, cycling, or any form of exercise that keeps the body active.')
        st.write('🔵**Tobacco Cessation:** Advise patients to quit smoking and avoid tobacco use to significantly reduce heart disease risk.')
        st.write('🔵**Manage cholesterol:** and blood pressure: Promote regular monitoring and control through medication and lifestyle adjustments.')
        st.write('🔵**Healthy Diet:** Recommend a balanced diet rich in fruits, vegetables, whole grains, and lean proteins to support heart health.')
        st.write('🔵**Alcohol Moderation:** Advise limiting alcohol consumption to moderate levels as defined by health guidelines.')
        st.write('🔵**Stress Management:** Suggest techniques such as mindfulness, meditation, or counseling to manage stress effectively.')
        st.write('🔵**Physical Activity:** Promote regular physical activity, emphasizing the importance of staying active for overall cardiovascular health.')
        st.write('🔵**Prioritize exercise:** Aim for at least 150 minutes of moderate or 75 minutes of vigorous activity weekly to establish a consistent routine.')
        st.markdown("<br>", unsafe_allow_html=True)

        # Button to confirm advice given
        if st.button('Confirm Advice Given'):
            st.success('Advice confirmed and recorded.')
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Display the key insights on heart health section
        new_title = '<p style="font-family:Georgia; color:#149CFE; font-size: 28px; text-decoration: underline; text-decoration-color: white;">Key Insights on Heart Health</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.write('🔵**Heart Size and Function:** Despite its fist-size, the adult heart pumps over 7,500 liters (2,000 gallons) of blood daily.')
        st.write('🔵**Heartbeat Count:** An adult heart beats around 100,000 times a day, with variations depending on factors like age, gender, and physical fitness.')
        st.write('🔵**Gender Differences:** Women\'s hearts typically beat faster than men\'s, even when at rest, due to size and hormonal influences.')
        st.write('🔵**Vascular Network:** The human circulatory system, spanning 100,000 kilometers, could encircle the Earth more than twice.')
        st.write('🔵**Heart\'s Autonomy:** The heart has its own electrical impulse, allowing it to beat even outside the body, under the right conditions.')
        st.write('🔵**Stress Impact:** Chronic stress escalates heart disease risk, while positive emotions, like laughter, enhance vascular function.')
        st.write('🔵**Exercise and Heart Health:** Consistent physical activity is vital for heart health, enhancing circulation and reducing heart disease risk.')

        # Display the Lottie animation on the page
        display_lottie_animation()

    # Check if the user has selected the 'REFERRAL TO SPECIALIST CARE' option
    if selected2 == 'REFERRAL TO SPECIALIST CARE':
        new_title = '<p style="font-family:Georgia; color:#149CFE; font-size: 28px; text-decoration: underline; text-decoration-color: white;">Specialist Consultation Contacts</p>'
        st.markdown(new_title, unsafe_allow_html=True)

        # Sample data for the doctors
        doctor_data = {
            "Name": ["Dr. LB Osrin", "Dr. Mamaila M. Lebea", "Dr. Lehlohonolo Dongo", "Dr. Ashandren Naicke", "Dr. Vinod Thomas"],
            "Location": ["Pretoria", "Sandton", "Springs", "Durban", "Cape Town"],
            "Contact Number": ["+27 74-375-0723", "+27 81-391-0201", "+27 74-698-5341", "+27 82-290-0745", "+27 63-476-8234"],
            "Email": ["osrin@gmail.com", "mamaila@gmail.com", "dongo@egmail.com", "naicke@gmail.com", "thomas@gmail.com"],
            "Specialization": ["Cardiologist", "Pediatric Cardiologist", "Cardiac Surgeon", "Interventional Cardiologist", "Electrophysiologist"]}
       
        # Display the data as a table
        st.table(doctor_data)

    # Check if the user has selected the 'PREDICT HEART DISEASE' option
    if selected2 == 'PREDICT HEART DISEASE':
        loaded_model = pickle.load(open('heart_disease_model.pkl', 'rb'))

        def heart(input_data):
            # Convert all input data to float, extracting the first element of tuples for radio inputs
            input_data_as_float = [float(item[0]) if isinstance(item, tuple) else float(item) for item in input_data]

            # Convert the list to a NumPy array
            input_data_as_numpy_array = np.asarray(input_data_as_float).reshape(1, -1)

            # Make a prediction
            prediction = loaded_model.predict(input_data_as_numpy_array)

            if prediction[0] == 0:
                return st.success('This person has less chance of heart disease')
            else:
                return st.error('This person has more chance of heart disease')

        def main():
            # Set the title for the page
            new_title = '<p style="font-family:Georgia; color:#149CFE; font-size: 28px; text-decoration: underline; text-decoration-color: white;">Heart Disease Prediction</p>'
            st.markdown(new_title, unsafe_allow_html=True)

            # Apply custom styles to the radio buttons and add spacing between questions
            st.markdown("""
            <style>
                /* Style for the selected radio button */
                div.stRadio > div[role='radiogroup'] > label[data-baseweb='radio'] > div:first-child {
                    background-color: #149CFE !important;
                    border-color: #149CFE !important;
                }
                /* Style for the unselected radio button */
                div.stRadio > div[role='radiogroup'] > label[data-baseweb='radio'] > div:first-child > div {
                    background-color: white !important;
                    border-color: #149CFE !important;
                }
                /* Custom label style to match the dark theme */
                div.stRadio > div[role='radiogroup'] > label {
                    font-weight: bold;
                    color: #fff; /* White text color */
                    background-color: #333; /* Dark background color */
                    padding: 5px 10px;
                    border-radius: 10px;
                    margin-right: 10px;
                }
                /* Spacing between questions */
                .question-spacing {
                    margin-bottom: 20px;
                }
            </style>
            """, unsafe_allow_html=True)
        
            # Collect user input for various heart disease factors with added spacing
            st.markdown('<div class="question-spacing">', unsafe_allow_html=True)
            age = st.number_input('Age', min_value=0, step=1, format='%d')
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="question-spacing">', unsafe_allow_html=True)
            sex = st.radio("Sex", [('1', 'Male'), ('0', 'Female')])
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="question-spacing">', unsafe_allow_html=True)
            cp = st.radio("Chest Pain Type", [('1', 'Typical Angina'), ('2', 'Atypical Angina'), ('3', 'Non-Anginal Pain'), ('4', 'Asymptomatic')])
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="question-spacing">', unsafe_allow_html=True)
            trestbps = st.number_input('Resting Blood Pressure (in mm Hg)', min_value=0, step=1, format='%d')
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="question-spacing">', unsafe_allow_html=True)
            chol = st.number_input('Serum Cholesterol (in mg/dl)', min_value=0, step=1, format='%d')
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="question-spacing">', unsafe_allow_html=True)
            fbs = st.radio("Fasting Blood Sugar > 120 mg/dl", [('1', 'True'), ('0', 'False')])
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="question-spacing">', unsafe_allow_html=True)
            restecg = st.radio("Resting Electrocardiographic Results", [('0', 'Normal'), ('1', 'Abnormal'), ('2', 'Ventricular Hypertrophy')])
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="question-spacing">', unsafe_allow_html=True)
            thalach = st.number_input('Maximum Heart Rate Achieved', min_value=0, step=1, format='%d')
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="question-spacing">', unsafe_allow_html=True)
            exang = st.radio("Exercise Induced Angina", [('1', 'Yes'), ('0', 'No')])
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="question-spacing">', unsafe_allow_html=True)
            oldpeak = st.number_input('ST Depression Induced by Exercise Relative to Rest', min_value=0.0, step=0.1, format='%f')
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="question-spacing">', unsafe_allow_html=True)
            slope = st.radio("Slope of the Peak Exercise ST Segment", [('1', 'Upsloping'), ('2', 'Flat'), ('3', 'Downsloping')])
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="question-spacing">', unsafe_allow_html=True)
            ca = st.radio("Number of Major Vessels Colored by Flourosopy", [('0', 'None'), ('1', 'One'), ('2', 'Two'), ('3', 'Three')])
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="question-spacing">', unsafe_allow_html=True)
            thal = st.radio("Thalassemia", [('1', 'Normal'), ('2', 'Fixed Defect'), ('3', 'Reversible Defect')])
            st.markdown('</div>', unsafe_allow_html=True)

            # Adjust the layout of the radio buttons
            st.write('<style>div.row-widget.stRadio>div{flex-direction:row;}</style>', unsafe_allow_html=True)

            # Predict heart disease when the user clicks the "PREDICT" button
            if st.button('PREDICT'):
                diagnosis = heart([age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal])

        # Run the main function if this script is executed as the main program
        if __name__ == '__main__':
            main()
