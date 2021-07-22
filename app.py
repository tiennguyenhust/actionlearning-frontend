"""
You need to run the app from the root
To run the app
$ streamlit run app.py
"""

import json
import pandas as pd
import streamlit as st
from PIL import Image
import requests

import matplotlib.pyplot as plt

    
st.title('IT Service Management')

from PIL import Image
import urllib.request

URL = 'https://www.itarian.com/images/ticket-management-software.png'

with urllib.request.urlopen(URL) as url:
    with open('temp.jpg', 'wb') as f:
        f.write(url.read())

img = Image.open('temp.jpg')
# my_png = cv2.waitKey(0)
st.image(img)

urllib.request.urlretrieve(
  'https://www.epita.fr/wp-content/uploads/2019/06/majeure-image-formation-etudiants-entreprises-epita-ingenieurs-2019-02.jpg',
   "images/gfg.jpg")

# from app import about
from PIL import Image
image = Image.open('images/gfg.jpg')
st.sidebar.title("EPITA-AIS (Group 2)")
st.sidebar.image(image, width=300)
st.sidebar.title('Team members: ')
st.sidebar.success('**Alexander POPPE**')
st.sidebar.success('**Arun Singh SIVAPRAKASH**')
st.sidebar.success('**Pramod Kumar NAGARAJ**')
st.sidebar.success('**Van Tien NGUYEN**')

description = st.text_input('Description: ')

host = "https://actionlearning-backend.herokuapp.com"


#model = st.selectbox('Select your model: ',('LDA', 'K-means'))
option = st.selectbox('How much similar tickets you need?',('Top 2', 'Top 5', 'Top 10'))

nb_tickets = {'Top 2': 2, 'Top 5':5, 'Top 10':10}

model_names = {'LDA': 'LDA_models_50.pkl', 'K-means': 'kmeans_model_150.pkl'}

st.text("Selected Model: LDA")
predict_btn = st.button("Predict")
if predict_btn:
    if not description:
        st.warning('Please input the description!')
        st.stop()
        
    result = None
    #if model == 'LDA':
    result = requests.get(host + '/LDA_predict?model_name=LDA_models_50.pkl&data={}'.format(description))
    #else:
        #result = requests.get(host + '/predict?model_name=kmeans_model_150.pkl&data={}'.format(description))

    res = result.json().split(' - ')
    label = int(res[0])
    
    tickets = requests.get(host + '/similar_tickets?label={}&nb_tickets={}'.format(label, nb_tickets[option]))

    top10Words = res[1].replace(' ', ', ')
    
    st.markdown("**Top 10 words: ** {}".format(top10Words))
    st.dataframe(pd.DataFrame(tickets.json()).set_index('Number'))

    top_10_labels = [0, 3, 2, 5, 34, 33, 18, 22, 12, 41]
    top_10_clusters = requests.get(host + '/top_10_clusters').json().replace('[','').replace(']','').split('-')


    col1, col2 = st.beta_columns((5, 6))

    df_master = pd.DataFrame(top_10_labels, columns=['Cluster'])
    df_master['Top 10 Words'] = pd.DataFrame(top_10_clusters)
    df_master = df_master.set_index('Cluster')
    
    with col1:
        st.image('images/top_10.png')
    with col2:
        st.dataframe(df_master)
    
    
    scores = requests.get(host + '/get_score?text={}'.format(description)).json()
    final_score, noun_score, verb_score, readability = scores.split(', ')
    final_score = round(float(final_score), 3)
    noun_score  = round(float(noun_score), 3)
    verb_score  = round(float(verb_score), 3)
    readability = round(float(readability), 3)
    
    st.markdown("**Quality of text and the calculated scores: **")
    st.markdown("**Final Score: {}**".format(final_score))
    st.markdown("**Noun Score: ** {}".format(noun_score))
    st.markdown("**Verb Score: ** {}".format(verb_score))
    st.markdown("**Readability: ** {}".format(readability))

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(
        ["noun_score", "verb_score", "readability"],
        [noun_score, verb_score, readability]
    )
    ax.title.set_text('Scores per category')
    ax.set_xlabel('Categories')
    ax.set_ylabel('Score')
    
    
    
    st.pyplot(fig)