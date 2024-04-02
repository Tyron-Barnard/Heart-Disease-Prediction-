import requests
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    # Send a GET request to the specified URL
    r = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if r.status_code != 200:
        # If not successful, return None
        return None
    # If successful, parse the JSON response and return it
    return r.json()

def display_lottie_animation():
    # URL of the Lottie animation
    lottie_url_hello = "https://lottie.host/0779af5d-1b85-4e28-b6b5-9249111bca39/cyv7hyH0rU.json"
    
    # Load the Lottie animation from the URL
    lottie_hello = load_lottieurl(lottie_url_hello)
    
    # Display the Lottie animation in the Streamlit app
    st_lottie(lottie_hello, key="hello")
