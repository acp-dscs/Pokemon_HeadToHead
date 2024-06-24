import streamlit as st
import pandas as pd
import requests
import random

st.title(":rainbow[Pokemon] Explorer Head to Head Comparison!")

# User to pick a Pokemon by number using the Slider
pokemon_number = st.slider("Choose your Pokemon for battle!", 1, 155)

# Get data on User Pokemon
pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_number}"
response = requests.get(pokemon_url).json() 

# Program to to randomly select another Pokemon for compasrison
pokemon_number_random = random.randint(1, 151)
pokemon_url_random = f"https://pokeapi.co/api/v2/pokemon/{pokemon_number_random}"
response_random = requests.get(pokemon_url_random).json()

# Isolate specific facts about the Users Pokemon
pokemon_name = response['name']
pokemon_height = response['height']
pokemon_weight = response['weight']
pokemon_sprites = response['sprites']['front_default']
pokemon_cries = f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{pokemon_number}.ogg"
pokemon_moves_count = len(response['moves'])
pokemon_moves = [move['move']['name'].capitalize() for move in response['moves']]
pokemon_stats = response['stats']

# Isolate specific facts about the Randomly Selected Pokemon
pokemon_name_random = response_random['name']
pokemon_height_random = response_random['height']
pokemon_weight_random = response_random['weight']
pokemon_sprites_random = response_random['sprites']['front_default']
pokemon_cries_random = f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{pokemon_number_random}.ogg"
pokemon_moves_count_random = len(response_random['moves'])
pokemon_moves_random = response_random['moves']

# Display Users Pokemon Details 
st.title(pokemon_name.title())
st.image(pokemon_sprites)
st.audio(pokemon_cries)
st.write(f"{pokemon_name.title()} is {pokemon_height}m tall and has a weight of {pokemon_weight}kg!")
st.write(f"Count of moves to pick from: {pokemon_moves_count}")

# Display Randomly Selected Pokemon Details 
st.title(pokemon_name_random.title())
st.image(pokemon_sprites_random)
st.audio(pokemon_cries_random)
st.write(f"{pokemon_name_random.title()} is {pokemon_height_random}m tall and has a weight of {pokemon_weight_random}kg!")
st.write(f"Count of moves to pick from: {pokemon_moves_count_random}")

st.title(f":rainbow[HEAD TO HEAD]")
st.title(f"{pokemon_name.title()} VS {pokemon_name_random.title()}")

# Display Key Stats of the User Pokemon in a table
st.header(f"List of Stats for your :rainbow[Pokemon: {pokemon_name.title()}]")

# Create a DataFrame for the location encounters
stats_data = [{'Key Stat': stat['stat']['name'].capitalize(), 'Base Value': stat['base_stat'], 'Effort': stat['effort']} for stat in pokemon_stats]
df_stats = pd.DataFrame(stats_data)

# Display the DataFrame as a table
st.write(df_stats)

# Create the Dropdown Widget
selected_move = st.selectbox('Choose an option:', pokemon_moves)

# Display the Option Selected by the User
st.subheader(f"{pokemon_name.title()} will challenge {pokemon_name_random.title()} with the move you selected: {selected_move}.")
st.title(f":rainbow[POW!!!] {pokemon_name.title()} WINS")
st.title(f"K.O. {selected_move} is a Kick Ass move!")
st.write('Press the button below to gift your Pokemon some balloons to celebrate!')

# Button with balloons for fun
if 'counter' not in st.session_state.keys():
    st.session_state['counter'] = 0

if st.button("Gift your Pokemon some Balloons!"):
    st.balloons()
    st.session_state['counter'] += 1
st.write(f"You have gifted your Pokemon {st.session_state['counter']} balloons!")

# Create DataFrame for the Bar Chart
bar_data = {
    'Category': ['Height', 'Weight', 'Height', 'Weight'],
    'Value': [pokemon_height, pokemon_weight, pokemon_height_random, pokemon_weight_random],
    'Pokemon': [pokemon_name, pokemon_name, pokemon_name_random, pokemon_name_random]
}
df_pokemon_bar = pd.DataFrame(bar_data)

# Display the DataFrame
st.write(df_pokemon_bar)

# Create Pivot Table for data to read into the Bar Chart
df_pivot_bar = df_pokemon_bar.pivot(index='Category', columns='Pokemon', values='Value')

# Display Bar Chart
st.subheader('Head to Head Height Vs Weight')
st.bar_chart(df_pivot_bar)