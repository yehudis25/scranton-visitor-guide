# program to run openai on my app

import streamlit as st
from openai import AzureOpenAI
from stored_scraped_data import get_all_activities, get_comments
from display import display

display()
# get the activities for the robot to use as data
def activities():
    data = get_all_activities()
    
    activities_string = ""
    # make each activity into a string; AI works well with strings
    for row in data:
        name = row[1]
        category = row[2]
        link = row[3]
        rating= row[4]
        comments = get_comments(row[0])
        activities_string += (
        f"- {name} ({category}) | rating: {rating} | link: {link} | comments: {comments}\n"
        )
    return activities_string

# connect to OpenAI
client = AzureOpenAI(
    api_key=st.secrets["AZURE_OPENAI_API_KEY"],
    api_version="2024-10-21",
    azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"]
)
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = st.secrets.get("AZURE_OPENAI_MODEL", "gpt-4o-mini")
if "messages" not in st.session_state:
    st.session_state["messages"] = []
# add a return to main menu btn
if st.button("Return to Main Menu"):
    st.switch_page("pages/main_menu.py")
st.title("🌦️ Smart Activity Planner")


# save the content of each chat
for message in st.session_state.messages:
    role = "👨‍👩‍👧‍👦 user" if message["role"] == "user" else "Robot"
    with st.chat_message(message["role"]):
        st.markdown(f"**{role}:** {message['content']}")

# first robot greeting
if not st.session_state.messages:
    greeting = "Planning Guide - input questions"
    st.session_state.messages.append({"role": "assistant", "content":
                                    greeting})
    with st.chat_message("assistant"):
        st.markdown(f"**Robot:** {greeting}")

# check for prompt
if prompt:= st.chat_input("Whats a good activity for a rainy day?🌧️"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"**👨‍👩‍👧‍👦 user:** {prompt}")
        
        # tell AI its job
        system_message = {
            "role": "system",
            "content": (
                "You are an AI activity recommendation assistant for Scranton, Pennsylvania. "
                "Your job is to suggest activities based on user input and weather hints.\n\n"
                "Rules:\n"
                "- Rainy/bad weather → prefer indoor activities\n"
                "- Sunny/good weather → prefer outdoor activities\n"
                "- Cold weather → prefer indoor or short outdoor activities\n\n"
                "Only use the activities provided below. Do NOT invent new ones.\n\n"
                "Available activities:\n"
                f"{activities()}\n\n"
                "Respond with 3-5 recommendations and explain why each fits."
            )
        }

        messages = [system_message] + st.session_state.messages[-6:]
        
        # tell AI to respond
        response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages
        )

        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content":
                                          reply})
        with st.chat_message("assistant"):
            st.markdown(f"Robot: {reply}")
