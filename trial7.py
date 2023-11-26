import streamlit as st
import mysql.connector
from streamlit import empty
import pandas as pd
from plant_species_crud import plant_species_crud
from genome_crud import genome_crud
from chromosome_crud import chromosome_crud
from gene_crud import gene_crud
from plant_species_query1 import plant_species_query

# Read the contents of the CSS file
with open("style.css", "r") as f:
    css_content = f.read()

# Inject CSS into the Streamlit app using st.markdown
st.markdown(
    f"""
    <style>
        {css_content}
    </style>
    """,
    unsafe_allow_html=True
)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Valliammai1#",
    database="plantdb3"
)
cursor = conn.cursor(buffered=True)

def execute_sql_file(file_path):
    print("hi")
    with open(file_path, "r") as sql_file:
        queries = sql_file.read().split(';')
        for query in queries:
            if query.strip():
                try:
                    cursor.execute(query)
                except mysql.connector.Error as err:
                    print(f"Error executing query: {err}")
    conn.commit()

# Function to create tables and insert data from an SQL file
if 'sql_file_executed' not in st.session_state:
    execute_sql_file("Plant_Database1.sql")
    st.session_state.sql_file_executed = True

# Function to execute SQL queries
def execute_query(query, data=None, fetch_all=False, column_types=None):
    cursor.execute(query, data)
    return cursor.fetchall()

# Function to display attribute table for an entity
def display_table(entity_name):
    query = f"SELECT * FROM {entity_name}"
    st.title(f"{entity_name} Table")
    table_data = execute_query(query)
    st.table(table_data)
 
# Function to create user table if not exists
def create_user_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_name VARCHAR(50) NOT NULL,
            password VARCHAR(50) NOT NULL,
            role VARCHAR(10) NOT NULL
        )
    ''')
    conn.commit()

# Function to register a new user
def register(user_name, password, role):
    if not user_name or not password and not role:
        st.error("Registration failed. Username, password and role cannot be empty.")
        return
    try:
        cursor.execute('''
            INSERT INTO users (user_name, password, role)
            VALUES (%s, %s, %s)
        ''', (user_name, password, role))
        conn.commit()
        st.success("Registration successful! You can now log in.")
    except mysql.connector.IntegrityError as e:
        st.error("Registration failed. Username already exists.")

# Function to authenticate a user
def authenticate(user_name, password):
    cursor.execute('''
        SELECT role FROM users
        WHERE user_name = %s AND password = %s
    ''', (user_name, password))
    result = cursor.fetchone()
    return result[0] if result else None



if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'selected_entity' not in st.session_state:
    st.session_state.selected_entity = ""

# Home page
if st.session_state.page == "home":
    st.title("PLANT GENETIC DATABASE MANAGEMENT")
    
    if st.button("Register"):
        st.session_state.page = "register"
        st.experimental_rerun()

    if st.button("login"):
        st.session_state.page = "login"
        st.experimental_rerun()

# Registration page
if st.session_state.page == "register":
    create_user_table()

    st.title("Registration Page")
    user_name = st.text_input("username:")
    password = st.text_input("password:", type="password")
    role = st.text_input("Role:")

    if st.button("register"):
        register(user_name, password, role)
        st.success("Registration successful! You can now log in.")
        st.session_state.page = "login"

# Login page
if st.session_state.page == "login":
    create_user_table()

    st.title("Login Page")
    user_name = st.text_input("Username:")
    password = st.text_input("Password:", type="password")


    if st.button("Login"):
        role = authenticate(user_name, password)
        if role:
            st.success("Login successful! Welcome, " + user_name + " with role: " + role)
            st.session_state.role = role  # Save the role in the session state
        if role == 'admin':
            st.session_state.page = "admin_view"
            st.experimental_rerun()
        elif role == 'user':
            st.session_state.page = "user_view"
            st.experimental_rerun()
        elif role != 'admin' and role != 'user':
            st.error("Invalid Role")
        else:
            st.error("Login failed. Invalid credentials")

# View page
if st.session_state.page == "admin_view":
    st.title("Admin page")

    entities = [
        "Plant_Species", "Genome", "Chromosome", "Gene", "Allele",
        "DNA_Sequence", "Genetic_Variation", "Genotype", "Protein"
    ]

    # Create buttons for each entity
    selected_entity = st.session_state.get("selected_entity", "")
    for entity in entities:
        if st.button(entity):
            selected_entity = entity
            st.session_state.selected_entity = selected_entity
            break  # Exit the loop once a button is clicked
        
    

    if selected_entity:
        if selected_entity == "Plant_Species":
            # Display the Plant_Species table with CRUD functionality
            plant_species_crud(selected_entity)
        elif selected_entity == "Genome":
            # Display the Genome table with CRUD functionality
            genome_crud(selected_entity)
        elif selected_entity == "Chromosome":
            chromosome_crud(selected_entity)
        elif selected_entity == "Gene":
            gene_crud(selected_entity)
        elif selected_entity in ["Allele",
                           "DNA_Sequence", "Genetic_Variation", "Genotype", "Protein"]:
        # You can add similar blocks for other entities
            display_table(selected_entity)

if st.session_state.page == "user_view":
    st.title("User page")
    entities = [
        "Plant_Species", "Genome", "Chromosome", "Gene", "Allele",
        "DNA_Sequence", "Genetic_Variation", "Genotype", "Protein"
    ]

    selected_entity = st.session_state.get("selected_entity", "")
    for entity in entities:
        if st.button(entity):
            selected_entity = entity
            st.session_state.selected_entity = selected_entity
            display_table(selected_entity)
            break  # Exit the loop once a button is clicked

    # Save selected entity for later use

    if selected_entity:
        if selected_entity == "Plant_Species":
            # Display the Plant_Species table with CRUD functionality
            display_table(selected_entity)
            species=st.text_input("Enter plant to query")
            if st.button("Enter plant to query:"):
                plant_species_query(species)
            # Execute the stored procedure
            st.subheader("Custom SQL Query:")
            custom_query = st.text_area("SQL query:")
            if st.button("Run Query"):
                try:
                    # Execute custom SQL query
                    query_result = execute_query(custom_query, fetch_all=True)

                    # Display query result in a table
                    if query_result:
                        st.table(query_result)  # The first row contains column names
                except mysql.connector.Error as err:
                    st.error(f"Error executing query: {err}")
                        
                        
            # Add SQL query input box
    
                
            



# Close MySQL connection
cursor.close()
conn.close()