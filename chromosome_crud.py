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

def chromosome_crud(entity_name):
    st.title(f"{entity_name} Table")

    # Display the Chromosome table
    table_data = execute_query(f"SELECT * FROM {entity_name}", fetch_all=True)
    st.table(table_data)

    # CRUD operations
    st.subheader("CRUD Operations:")
    crud_operation = st.radio("Select CRUD Operation:", ["Create", "Read", "Update", "Delete"])

    if crud_operation == "Create":
        # Create operation code for Chromosome
        genome_id = st.text_input("Genome ID:")
        chromosome_number = st.text_input("Chromosome Number:")
        length = st.text_input("Length:")
        genes_count = st.text_input("Genes Count:")

        if st.button("Create"):
            # Insert new chromosome into the database
            cursor.execute(
                "INSERT INTO Chromosome(Genome_ID, Chromosome_Number, Length, Genes_Count) VALUES (%s, %s, %s, %s)",
                (genome_id, chromosome_number, length, genes_count)
            )
            conn.commit()
            st.success("New chromosome created successfully!")
            st.experimental_rerun()
            
    elif crud_operation == "Update":
        # Update operation code for Chromosome
        chromosome_id = st.text_input("Enter Chromosome ID to Update:")
        new_genome_id = st.text_input("New Genome ID:")
        new_chromosome_number = st.text_input("New Chromosome Number:")
        new_length = st.text_input("New Length:")
        new_genes_count = st.text_input("New Genes Count:")

        if st.button("Update"):
            # Update chromosome in the database
            cursor.execute(
                "UPDATE Chromosome SET Genome_ID = %s, Chromosome_Number = %s, Length = %s, Genes_Count = %s WHERE Chromosome_ID = %s",
                (new_genome_id, new_chromosome_number, new_length, new_genes_count, chromosome_id)
            )
            conn.commit()
            st.success("Chromosome updated successfully!")
            st.experimental_rerun()

    elif crud_operation == "Delete":
        # Delete operation code for Chromosome
        chromosome_id_to_delete = st.text_input("Enter Chromosome ID to Delete:")

        if st.button("Delete"):
            # Delete chromosome from the database
            query = "DELETE FROM Chromosome WHERE Chromosome_ID = %s"
            data = (chromosome_id_to_delete,)

            try:
                cursor.execute(query, data)
                conn.commit()
                st.success("Chromosome deleted successfully!")
                st.experimental_rerun()
            except mysql.connector.Error as err:
                st.error(f"Error deleting chromosome: {err}")

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
