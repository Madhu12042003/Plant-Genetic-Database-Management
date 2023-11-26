
import streamlit as st
import mysql.connector
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

# Function to execute an SQL file
def execute_sql_file(file_path):
    with open(file_path, "r") as sql_file:
        queries = sql_file.read().split(';')
        for query in queries:
            if query.strip():
                try:
                    cursor.execute(query)
                except mysql.connector.Error as err:
                    print(f"Error executing query: {err}")
    conn.commit()

# Read the contents of the stored procedure SQL file
# Function to create tables and insert data from an SQL file
if 'sql_file_executed' not in st.session_state:
    execute_sql_file("Plant_Database1.sql")
    st.session_state.sql_file_executed = True

def plant_species_query(plant_species_id):
    
    cursor.callproc("GetPlantDetails", [plant_species_id])
    conn.commit()

    
    # Save selected entity for later use
    # Use stored_results to get the iterator over results
    results_iterator = cursor.stored_results()

    # Iterate over each result set
    for result_set in results_iterator:
        # Fetch the result set as a list of tuples
        result_data = result_set.fetchall()
        #st.write(result_data)
        #st.write(result_set.description)
        entities = [
        "Plant_Species", "Genome", "Chromosome", "Gene", "Allele",
        "DNA_Sequence", "Genetic_Variation", "Genotype", "Protein"
        ]
        
    # Display or process the result data as needed
        if result_data:
                columns = [desc[0] for desc in result_set.description]
                result_df = pd.DataFrame(result_data, columns=columns)
                st.table(result_df)
        else:
                st.write("No data found for the specified argument.")
        