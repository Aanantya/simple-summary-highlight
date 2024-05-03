import streamlit as st
import main as m1

st.title("Simple Summary Highlights")


url = st.text_input('Paste your URL below')

if st.button("GO"):
    data = m1.main(url=url)
    
    for d in data:
        for key, val in d.items():

            if key == 'title':
                st.title(val)
    
            if key == 'h1':
                st.header(val)

            if (key == 'h2') or (key == 'h3'):
                st.subheader(val)
    
            if key == 'p':
                val = ' '.join(val)
                st.write(val)