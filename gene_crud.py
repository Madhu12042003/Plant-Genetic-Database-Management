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

def gene_crud(entity_name):
    st.title(f"{entity_name} Table")

    # Display the Gene table
    table_data = execute_query(f"SELECT * FROM {entity_name}", fetch_all=True)
    st.table(table_data)

    # CRUD operations
    st.subheader("CRUD Operations:")
    crud_operation = st.radio("Select CRUD Operation:", ["Create", "Read", "Update", "Delete"])

    if crud_operation == "Create":
        # Create operation code for Gene
        chromosome_id = st.text_input("Chromosome ID:")
        gene_name = st.text_input("Gene Name:")
        gene_description = st.text_input("Gene Description:")
        start_position = st.text_input("Start Position:")
        end_position = st.text_input("End Position:")
        strand = st.text_input("Strand:")

        if st.button("Create"):
            # Insert new gene into the database
            cursor.execute(
                "INSERT INTO Gene(Chromosome_ID, Gene_Name, Gene_Description, Start_Position, End_Position, Strand) VALUES (%s, %s, %s, %s, %s, %s)",
                (chromosome_id, gene_name, gene_description, start_position, end_position, strand)
            )
            conn.commit()
            st.success("New gene created successfully!")
            st.experimental_rerun()
            
    elif crud_operation == "Update":
        # Update operation code for Gene
        gene_id = st.text_input("Enter Gene ID to Update:")
        new_chromosome_id = st.text_input("New Chromosome ID:")
        new_gene_name = st.text_input("New Gene Name:")
        new_gene_description = st.text_input("New Gene Description:")
        new_start_position = st.text_input("New Start Position:")
        new_end_position = st.text_input("New End Position:")
        new_strand = st.text_input("New Strand:")

        if st.button("Update"):
            # Update gene in the database
            cursor.execute(
                "UPDATE Gene SET Chromosome_ID = %s, Gene_Name = %s, Gene_Description = %s, Start_Position = %s, End_Position = %s, Strand = %s WHERE Gene_ID = %s",
                (new_chromosome_id, new_gene_name, new_gene_description, new_start_position, new_end_position, new_strand, gene_id)
            )
            conn.commit()
            st.success("Gene updated successfully!")
            st.experimental_rerun()

    elif crud_operation == "Delete":
        # Delete operation code for Gene
        gene_id_to_delete = st.text_input("Enter Gene ID to Delete:")

        if st.button("Delete"):
            # Delete gene from the database
            query = "DELETE FROM Gene WHERE Gene_ID = %s"
            data = (gene_id_to_delete,)

            try:
                cursor.execute(query, data)
                conn.commit()
                st.success("Gene deleted successfully!")
                st.experimental_rerun()
            except mysql.connector.Error as err:
                st.error(f"Error deleting gene: {err}")

    # Custom SQL query section
    st.subheader("Custom SQL Query:")
    custom_query = st.text_area("Enter your SQL query:")
    
    if st.button("Run Query"):
        try:
            # Execute custom SQL query
            query_result = execute_query(custom_query, fetch_all=True)
            st.table(query_result)
        except mysql.connector.Error as err:
            st.error(f"Error executing query: {err}")

# Usage example for Gene entity
#gene_crud("Gene")
