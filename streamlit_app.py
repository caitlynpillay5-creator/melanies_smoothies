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
)
# Convert the Snowflake data into a Python list
fruit_rows = my_dataframe.collect()
fruit_list = [row["FRUIT_NAME"] for row in fruit_rows]
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
        ingredients_string += fruit_chosen + " "
    # Remove the extra space at the end
    ingredients_string = ingredients_string.strip()
    # -----------------------------------------------------
    # SUBMIT BUTTON
    # -----------------------------------------------------
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        if name_on_order == "":
            
            st.warning("Please enter a name for your smoothie.")
        else:
            # Insert the ingredients and name into Snowflake
            my_insert_stmt = """
                INSERT INTO smoothies.public.orders
                (ingredients, name_on_order)
                VALUES (?, ?)
            """
            session.sql(
                my_insert_stmt,
                params=[
                    ingredients_string,
                    name_on_order
                ]
            ).collect()
            st.success(
                "Your Smoothie is ordered! 🥤",
                icon="✅"
            )
# ---------------------------------------------------------
# SMOOTHIEFROOT API
# ---------------------------------------------------------
st.subheader("🍉 SmoothieFroot Information")
smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)
# Display API response
st.write(smoothiefroot_response.json())
