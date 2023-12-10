import streamlit as st
from datetime import datetime
from spelling_correction import correctSentence


st.title('Correct your sentence ')


data_sentence = st.text_input(label="Enter your sentence:", value="", max_chars=None, key=None, type="default", label_visibility="visible")


submit = st.button('Show Result')

if submit:
    st.success('Corrected Sentence')
    # st.balloons()
    if data_sentence:
        final_sentence = correctSentence(data_sentence)
        st.title(final_sentence)