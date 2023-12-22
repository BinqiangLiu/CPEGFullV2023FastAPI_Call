import streamlit as st
import requests
import json
import timeit
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Open AI China PEG Chat Assistant - Open Source Version", layout="wide")
st.subheader("Welcome to Open AI China PEG Chat Assistant: Life Enhancing with AI!")
st.write("Important notice: This Open AI China PEG Chat Assistant is offered for information and study purpose only and by no means for any other use. Check it out to see whether it could help you on your understanding of the CPEP (China Patent Examination Guideline). Any user should never interact with the AI Assistant in any way that is against any related promulgated regulations. The user is the only entity responsible for interactions taken between the user and the AI Chat Assistant.")

css_file = "main.css"
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)  

HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

def query_fastapi(question, texts_filename, db_embeddings_filename):
    url = "https://binqiangliu-cpegfullv2023fastapi.hf.space/aisitechat"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"
    }

    data = {
        "user_question": question,
        "texts_filename": texts_filename,
        "db_embeddings_filename": db_embeddings_filename        
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error from API: {response.status_code}")

texts_filename=""
db_embeddings_filename=""

with st.sidebar:
    file_name_choice = st.selectbox("Select the part of CPEG to AI Chat", ("Part 1：初步审查","Part 2：实质审查","Part 3：进入国家阶段的国际申请的审查","Part 4：复审与无效请求的审查","Part 5：专利申请及事务处理","Part 6：外观设计国际申请","Part 7：总目录与索引"))
    if file_name_choice == "Part 1：初步审查":
        texts_filename  = "texts_part01.txt"
        db_embeddings_filename ="final_db_embeddings_part01.pt"        
    elif file_name_choice == "Part 2：实质审查":
        texts_filename  = "texts_part02.txt"
        db_embeddings_filename ="final_db_embeddings_part02.pt"    
    elif file_name_choice == "Part 3：进入国家阶段的国际申请的审查":
        texts_filename  = "texts_part03.txt"
        db_embeddings_filename ="final_db_embeddings_part03.pt"    
    elif file_name_choice == "Part 4：复审与无效请求的审查":
        texts_filename  = "texts_part04.txt"
        db_embeddings_filename ="final_db_embeddings_part04.pt"    
    elif file_name_choice == "Part 5：专利申请及事务处理":
        texts_filename  = "texts_part05.txt"
        db_embeddings_filename ="final_db_embeddings_part05.pt"    
    elif file_name_choice == "Part 6：外观设计国际申请":
        texts_filename  = "texts_part06.txt"
        db_embeddings_filename ="final_db_embeddings_part06.pt"    
    elif file_name_choice == "Part 7：总目录与索引":
        texts_filename  = "texts_TOCINDEX.txt"
        db_embeddings_filename ="final_db_embeddings_TOCINDEX.pt"    
    current_datetime = datetime.datetime.now()
    print("Content selected - info from sidebar section: "+texts_filename)
    print(f'Content selected: {texts_filename} @ {current_datetime}') 

question = st.text_input("Enter your question:")

if st.button('Get AI Response'):
    with st.spinner('Fetching AI response...'):       
        try:
            ai_response = query_fastapi(question, texts_filename, db_embeddings_filename)
            ai_response_content=ai_response['response']
            st.write("AI Response:")            
            st.write(ai_response_content)    
            print("AI Response:", ai_response_content)            
        except Exception as e:
            print(e)
