import streamlit as st 

# st.title("<h1 style='color:green'>Welcome to BMI calculator</h1>")
st.markdown("<h1 style='color:green'>Welcome to BMI calculator</h1>", unsafe_allow_html=True)
weight = st.number_input("Enter your weight in kgs.")
sttus = st.radio('Select your height format:',('cms','m','feet'))
if (sttus == 'cms'):
    height = st.number_input("Enter your height in cms.")
    try: 
        bmi = weight / (height/100)**2
    except:
        st.write("Enter valid height.")
elif (sttus == 'm'):
    height = st.number_input("Enter your height in meters.")
    try: 
        bmi = weight / (height)**2
    except:
        st.write("Enter valid height.")

else: #(sttus == 'feet'):
    feet = st.number_input("Height (feet)")
    inches = st.number_input("Height (inches)")
    height_m = (feet*12 + inches) * 0.0254

    try: 
        bmi = weight / (height_m ** 2) ##1/3.28084 = 0.3048
    except:
        st.write("Enter valid height.")


if (st.button("Calculate BMI")):
    st.text(f"Your BMI is: {bmi:.2f}")
    if (bmi < 16.):
        st.text("You are severely underweight.")
    elif (bmi >= 16. and bmi < 18.5):
        st.warning("You are underweight.")
    elif (bmi >= 18.5 and bmi < 25.):
        st.success("You are healthy.")
    elif (bmi >= 25. and bmi < 30.):
        st.warning("You are overweight.")
    else:
        st.error("You are severely overweight.")