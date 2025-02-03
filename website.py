import numpy as np
import pandas as pd
import pickle
import streamlit as st
import requests
import pickle

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)


file_url = "https://www.dropbox.com/scl/fi/gxffyb41qcs6j888439p3/combined_sim.pkl?rlkey=4oa8wupn59tqaskg5rbhuixx2&st=43s33n10&dl=1"


download_file(file_url, "combined_sim.pkl")


with open("combined_sim.pkl", "rb") as f:
    combined_sim = pickle.load(f)



songs = pickle.load(open('songs.pkl' , mode = 'rb'))
#print(songs)
songs = pd.DataFrame(songs)
#print(songs)

def song_rec(text):
    recommended_songs = []
    track_ids = []
    
    index = songs[songs['track_name']== text].index[0]
    distance = combined_sim[index]

    recs = sorted(list(enumerate(distance)) , reverse = True , key = lambda x : x[1])[1:11]
    
    for i in recs:
        # print(i[0])
        recommended_songs.append((songs.iloc[i[0]].track_name))
        track_ids.append(songs.iloc[i[0]].track_id)
    return recommended_songs,track_ids
    

import streamlit as st

col_l, col_cen , col_right = st.columns(3)
with col_cen:
    st.image('https://static.vecteezy.com/system/resources/previews/023/986/857/non_2x/spotify-logo-spotify-logo-transparent-spotify-icon-transparent-free-free-png.png')
st.title('Similar Songs Finder')


song = st.selectbox(label='Choose your song: ' ,options=list(songs['track_name'].values) )
btn = st.button(label='Recommend')

if btn:
    
    recs, track_ids = song_rec(song)
    
    
    for song_name, track_id in zip(recs, track_ids):
        # Create the Spotify embed URL for each track
        embed_url = f"https://open.spotify.com/embed/track/{track_id}"
        
        # Create the HTML iframe for embedding the Spotify player
        html_code = f"""
        <iframe src="{embed_url}" width="300" height="80" frameborder="0" 
            allowtransparency="true" allow="encrypted-media"></iframe>
        """
        
        # Display the song name and the embedded Spotify player
        st.write(song_name)
        st.markdown(html_code, unsafe_allow_html=True)

