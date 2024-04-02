import pickle
import numpy as np

# Function to load a pre-trained model from a file
def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

# Function to make a prediction using the pre-trained model
def predict_heart_disease(model, input_data):
    # Convert the input data to a NumPy array
    input_data_as_numpy_array = np.asarray(input_data)
    # Reshape the array for compatibility with the model's expected input format
    input_reshape = input_data_as_numpy_array.reshape(1, -1)
    # Use the model to make a prediction
    prediction = model.predict(input_reshape)
    return prediction
