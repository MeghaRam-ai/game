import sys
import streamlit as st
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(parent_dir)
from backend.generator import regenerate, generate_new_game_sequence


st.subheader("Game generator")
game_duration = st.number_input("Game duration")
if game_duration is not None:
    duration = st.write("Game duration is:", game_duration)
    sequence = regenerate(game_duration)
    st.write("Game Sequence Generated:")
    st.dataframe(sequence)



st.subheader("Game generator using RNN")
game_duration_in_minutes = st.number_input("Game duration in minutes")
if game_duration_in_minutes is not None:
    duration = st.write("Game duration is:", game_duration_in_minutes)
    sequence = generate_new_game_sequence(game_duration_in_minutes)
    st.write("New Game Sequence Generated:")
    st.write(sequence)