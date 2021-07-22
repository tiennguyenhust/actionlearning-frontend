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
   "gfg.jpg")

# from app import about
from PIL import Image
image = Image.open('gfg.jpg')
st.sidebar.title("ACTION LEARNING PROJECT")
st.sidebar.success("TEAM: **ARTIFICIAL INTELLIGENCE SYSTEM** (Group 2)!")
st.sidebar.image(image, width=250)
st.sidebar.title('Team member: ')
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

    top10Words = res[1]
    
    st.markdown("**Top 10 words: ** {}".format(top10Words))
    st.dataframe(pd.DataFrame(tickets.json()).set_index('Number'))



"""
To cover
- Please enter the Description
"""

#file = st.file_uploader("Upload the file")

#if file:
#    dataframe = pd.read_csv(file, sep=",")
#    if option == 'Top 2':
#        result = dataframe.head(2)
#        df = pd.DataFrame(result)
#        st.dataframe(df)
#        # st.write(result)
##    elif option == 'Top 5':
#        result = dataframe.head(5)
#        st.write(result)
#    elif option == 'Top 10':
#        result = dataframe.head(10)
#        st.write(result)

"""
These are the similar tickets found from the previous records....!
"""