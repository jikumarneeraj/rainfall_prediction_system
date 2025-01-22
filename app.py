import numpy as np
import pickle
import streamlit as st

# Load the model with error handling
try:
    with open("rainfall_prediction_model.pkl", "rb") as file:
        loaded_data = pickle.load(file)
        # Check if the loaded data is a dictionary and extract the model if needed
        if isinstance(loaded_data, dict) and 'model' in loaded_data:
            loaded_model = loaded_data['model']
        else:
            loaded_model = loaded_data  # Assume it's directly the model
except FileNotFoundError:
    st.error("Model file not found. Please check if 'rainfall_prediction_model.pkl' is present.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")
    st.stop()

def rain_prediction(input_data):
    try:
        # Convert input to numpy array and reshape for prediction
        input_data_as_numpy_array = np.asarray(input_data, dtype=float)
        input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

        # Predict using the loaded model
        prediction = loaded_model.predict(input_data_reshaped)

        # Map prediction result
        if prediction[0] == 1:
            return 'Rainfall'
        else:
            return 'No Rainfall'
    except Exception as e:
        return f"Error during prediction: {e}"

def main():
    # Title
    st.title('Rainfall Prediction Web App')

    # Input fields
    pressure = st.text_input('Pressure')
    dewpoint = st.text_input('Dewpoint')
    humidity = st.text_input('Humidity')
    cloud = st.text_input('Cloud')
    sunshine = st.text_input('Sunshine')
    winddirection = st.text_input('Wind Direction')
    windspeed = st.text_input('Wind Speed')

    # Prediction result
    diagnosis = ''

    # Prediction button
    if st.button('Rainfall Test Result'):
        try:
            # Convert inputs to float and predict
            inputs = [float(pressure), float(dewpoint), float(humidity), 
                      float(cloud), float(sunshine), float(winddirection), float(windspeed)]
            diagnosis = rain_prediction(inputs)
        except ValueError:
            diagnosis = "Please enter valid numeric values for all fields."

        st.success(diagnosis)

if __name__ == '__main__':
    main()