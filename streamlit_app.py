# Import Python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


# ---------------------------------------------------------
# APP TITLE
# ---------------------------------------------------------

st.title("🥤 Customise your Smoothie! 🥤")

st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)


# ---------------------------------------------------------
# NAME OF SMOOTHIE
# ---------------------------------------------------------

name_on_order = st.text_input("Name of Smoothie")

st.write(
    "The name of your smoothie will be:",
    name_on_order
)


# ---------------------------------------------------------
# CONNECT TO SNOWFLAKE
# ---------------------------------------------------------

cnx = st.connection("snowflake")

session = cnx.session()


# ---------------------------------------------------------
# GET FRUIT OPTIONS FROM SNOWFLAKE
# ---------------------------------------------------------

my_dataframe = (
    session
    .table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"))
    .collect()
)

# Convert Snowflake results into a Python list
fruit_list = [row["FRUIT_NAME"] for row in my_dataframe]


# ---------------------------------------------------------
# ALLOW USER TO SELECT INGREDIENTS
# ---------------------------------------------------------

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)


# ---------------------------------------------------------
# CREATE AND SUBMIT ORDER
# ---------------------------------------------------------

if ingredients_list:

    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients
