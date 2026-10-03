import streamlit as st 


st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
st.image("https://www.w3schools.com/w3images/lights.jpg", caption="Beautiful Lights")
st.write("This is a sample Streamlit app that demonstrates how to embed video, audio, and images.")
barchart=st.bar_chart([1, 5, 2, 6, 2, 1])
print(barchart)
linechart = st.line_chart([1, 5, 2, 6, 2, 1])
print(linechart)
area_chart = st.area_chart([1, 5, 2, 6, 2, 1])
print(area_chart)
