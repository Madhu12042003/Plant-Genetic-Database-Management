import streamlit as st
import mysql.connector
from streamlit import empty
import pandas as pd

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Valliammai1#",
    database="plantdb2"
)
cursor = conn.cursor(buffered=True)

# Function to execute SQL queries
def execute_query(query, data=None, fetch_all=False, column_types=None):
    cursor.execute(query, data)
    return cursor.fetchall()

def genome_crud(entity_name):
    st.title(f"{entity_name} Table")

    # Display the Plant_Species table
    table_data = execute_query(f"SELECT * FROM {entity_name}", fetch_all=True)
    st.table(table_data)

    # CRUD operations
    st.subheader("CRUD Operations:")
    crud_operation = st.radio("Select CRUD Operation:", ["Create", "Read", "Update", "Delete"])

    if crud_operation == "Create":
        genome_id = st.text_input("Genome ID:")
        plant_species_id = st.text_input("Plant Species:")
        genome_size = st.text_input("Genome Size:")
        chromosome_count = st.text_input("Chromosome count:")

        if st.button("Create"):
            # Insert new plant species into the database
            #print(common_name)
            cursor.execute(
                "INSERT INTO Genome(Genome_ID, Species_ID, Genome_Size,Chromosome_Count) VALUES (%s, %s, %s, %s)",
                (genome_id, plant_species_id, genome_size, chromosome_count)
            )
            conn.commit()
            st.success("New genome created successfully!")
            st.experimental_rerun()
            
    elif crud_operation == "Update":
        st.subheader("Update Genome:")
        new_genome_id = st.text_input("Genome ID:")
        new_plant_species_id = st.text_input("Plant Species:")
        new_genome_size = st.text_input("Genome Size:")
        new_chromosome_count = st.text_input("Chromosome count:")

        if st.button("Update"):
            # Update plant species in the database
            cursor.execute(
                "UPDATE Genome SET Genome_ID = %s, Species_ID = %s, Genome_Size = %s WHERE Chromosome_Count = %s",
                (new_genome_id, new_plant_species_id, new_genome_size, new_chromosome_count)
            )
            conn.commit()
            st.success("Plant species updated successfully!")
            st.experimental_rerun()

    elif crud_operation == "Delete":
        st.subheader("Delete Genome:")
        genome_id_to_delete = st.text_input("Enter Genome ID to Delete:")

        if st.button("Delete"):
            # Check if the plant_species_id_to_delete is not empty
            if not genome_id_to_delete:
                st.error("Please enter a valid Genome ID.")
            else:
                # Delete plant species from the database
                query = "DELETE FROM Genome WHERE Genome_ID = %s"
                data = (genome_id_to_delete,)

                try:
                    cursor.execute(query, data)
                    conn.commit()
                    st.success("Genome deleted successfully!")
                    st.experimental_rerun()
                except mysql.connector.Error as err:
                    st.error(f"Error deleting genome: {err}")
                    
    # Add SQL query input box
    st.subheader("Custom SQL Query:")
    custom_query = st.text_area("Enter your SQL query:")
    
    if st.button("Run Query"):
        try:
            # Execute custom SQL query
            query_result = execute_query(custom_query, fetch_all=True)
            st.table(query_result)
        except mysql.connector.Error as err:
            st.error(f"Error executing query: {err}")