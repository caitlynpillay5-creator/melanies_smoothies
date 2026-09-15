# Import Python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title("🥤 Customise your Smoothie! 🥤")

st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)


# Name of smoothie
name_on_order = st.text_input("Name of Smoothie")

st.write(
    "The name of your smoothie will be:",
    name_on_order
)


# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()


# Get fruit options
my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select(
    col("FRUIT_NAME")
)


# Choose ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)


# If ingredients have been selected
if ingredients_list:

    ingredients_string = ""

    # Loop through each selected fruit
    for fruit_chosen in ingredients_list:

        ingredients_string += fruit_chosen + " "

        # Get nutrition information for this fruit
        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + fruit_chosen
        )

        # Display nutrition information
        st.write("Nutrition information for:", fruit_chosen)

        sf_df = st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )


    # Create the INSERT statement
    my_insert_stmt = """
        INSERT INTO smoothies.public.orders
        (ingredients, name_on_order)
        VALUES ('""" + ingredients_string + """',
                '""" + name_on_order + """')
    """

    st.write(my_insert_stmt)


    # Submit order button
    time_to_insert = st.button("Submit Order")


    if time_to_insert:

        session.sql(my_insert_stmt).collect()

        st.success(
            "Your Smoothie is ordered! 🥤",
            icon="✅"
        )
