import streamlit as st
import mysql.connector
from streamlit import empty
import pandas as pd

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Valliammai1#",
    database="plantdb3"
)
cursor = conn.cursor(buffered=True)

# Function to execute SQL queries
def execute_query(query, data=None, fetch_all=False, column_types=None):
    cursor.execute(query, data)
    return cursor.fetchall()

def plant_species_crud(entity_name):
    st.title(f"{entity_name} Table")

    # Display the Plant_Species table
    table_data = execute_query(f"SELECT * FROM {entity_name}", fetch_all=True)
    st.table(table_data)

    # CRUD operations
    st.subheader("CRUD Operations:")
    crud_operation = st.radio("Select CRUD Operation:", ["Create", "Read(Display)", "Update", "Delete"])

    if crud_operation == "Create":
        st.subheader("Create New Plant Species:")
        common_name = st.text_input("Common Name:")
        scientific_name = st.text_input("Scientific Name:")
        family = st.text_input("Family:")

        if st.button("Create"):
            # Insert new plant species into the database
            #print(common_name)
            cursor.execute(
                "INSERT INTO Plant_Species(Common_Name, Scientific_Name, Family) VALUES (%s, %s, %s)",
                (common_name, scientific_name, family)
            )
            conn.commit()
            st.success("New plant species created successfully!")
            st.experimental_rerun()
            
    elif crud_operation == "Update":
        st.subheader("Update Plant Species:")
        plant_species_id = st.text_input("Enter Plant Species ID to Update:")
        new_common_name = st.text_input("New Common Name:")
        new_scientific_name = st.text_input("New Scientific Name:")
        new_family = st.text_input("New Family:")

        if st.button("Update"):
            # Update plant species in the database
            cursor.execute(
                "UPDATE Plant_Species SET Common_Name = %s, Scientific_Name = %s, Family = %s WHERE Species_ID = %s",
                (new_common_name, new_scientific_name, new_family, plant_species_id)
            )
            conn.commit()
            st.success("Plant species updated successfully!")
            st.experimental_rerun()

    elif crud_operation == "Delete":
        st.subheader("Delete Plant Species:")
        plant_species_id_to_delete = st.text_input("Enter Plant Species ID to Delete:")

        if st.button("Delete"):
            # Check if the plant_species_id_to_delete is not empty
            if not plant_species_id_to_delete:
                st.error("Please enter a valid Plant Species ID.")
            else:
                # Delete plant species from the database
                query = "DELETE FROM Plant_Species WHERE Species_ID = %s"
                data = (plant_species_id_to_delete,)

                try:
                    cursor.execute(query, data)
                    conn.commit()
                    st.success("Plant species deleted successfully!")
                    st.experimental_rerun()
                except mysql.connector.Error as err:
                    st.error(f"Error deleting plant species: {err}")

    elif crud_operation == "Read(Display)":
        # Display the Plant_Species table
        table_data = execute_query(f"SELECT * FROM {entity_name}", fetch_all=True)
        st.table(table_data)

    