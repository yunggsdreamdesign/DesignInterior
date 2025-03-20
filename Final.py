import os
import streamlit as st
from openai import OpenAI
#from dotenv import load_dotenv

#load_dotenv()

openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)

def user_ai(msg):
    system_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """ You are a best interior designer. You'll suggest the user which design and decoration are suitable with their theme and place. You will also tell them what is the best brand and place that they can purchase the item. please make it in 200 words and converse in professional way as interior designer. """
            },
            {
                "role": "user",
                "content": f'{msg}'
            }
        ],
        max_tokens=500,
        temperature=1.3
    )

    role = system_response.choices[0].message.content
    return role

def cover_ai(msg):
    cover_response = client.images.generate(
        model="dall-e-3",
        prompt=msg,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = cover_response.data[0].url
    return image_url

def design_ai(msg):
    design_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You will generate a detailed image prompt to design a place that user request. Image prompt should follow the theme, colour, suitable furniture and accessories. Can list the recommendation where to buy all the furniture and accessories and what is the best brand."""
            },
            {
                "role": "user",
                "content": f'{msg}'
            }
        ],
        max_tokens=100,
        temperature=1.3
    )

    design_prompt = design_response.choices[0].message.content
    return design_prompt

def interior_design_ai(user_prompt):
    idesign = user_ai(user_prompt)
    design = design_ai(idesign)
    image = cover_ai(design)

    st.image(image, caption="Generated Image")  # Display the generated image
    st.write("Design Prompt:", design)  # Display the design prompt

# Streamlit app UI
st.markdown(
    """
    <div style="text-align:center">
        <h1>🌥 Dream to Real ID AI 🌥</h1>
        <h2>👩🏽‍💻: Hey, you are now an ID. Express your dream on this app!</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Selection for the place
place_options = ["House", "Office", "Shop", "Hotel"]
place = st.selectbox("What is your place?", place_options)

# Room options based on the chosen place
if place:
    if place == "House":
        room_options = ["Bedroom", "Living Room", "Kitchen", "Toilet", "Powder Room", "Laundry Room", "Yard"]
    elif place == "Office":
        room_options = ["Office Room", "Meeting Room", "Lobby", "Pantry", "Toilet"]
    elif place == "Shop":
        room_options = ["Dining Area", "Counter Area", "Shop Entrance", "Toilet"]
    elif place == "Hotel":
        room_options = ["Guest Rooms and Suites", "Lobby and Reception", "Restaurants and Dining", "Bars and Lounges", "Conference and Event Spaces", "Spa and Wellness Centers", "Fitness Centers and Recreational Spaces", "Hallways, Elevators, and Public Restrooms"]
    else:
        room_options = []

    # Room selection based on the chosen place
    if room_options:
        selected_room = st.selectbox(f"Select a room for {place}:", room_options)

    # Input for color
    color = st.text_input("Enter the desired color:")

    # Suggested themes for the design
    themes = [
        "Modern", "Vintage", "Minimalist", "Rustic", "Scandinavian",
        "Innovative", "Contemporary", "Professional", "Elegant", "Cozy",
        "Industrial", "Chic", "Luxurious", "Resort-style"
    ]

    selected_theme = st.selectbox("Suggest Suitable Themes", themes)

    # Check if all necessary inputs are provided to generate the design
    if selected_room and color:
        user_input = st.text_area("Describe the room and design preferences:", height=100)
        if st.button("Generate Design"):
            if user_input:
                interior_design_ai(f"I want to design a {place.lower()} {selected_room.lower()} with {color} theme. {user_input}")
            else:
                st.warning("Please provide a description with suggestion to generate the design.")
