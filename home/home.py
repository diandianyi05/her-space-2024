import streamlit as st



from pathlib import Path as p
from home.get_empowerment_solution import get_empowerment_solution

try:
    get_empowerment_solution()

except Exception as error:
    st.error(f"An error occurred: {str(error)}")
    print(f"Debug: Error occurred - {str(error)}")
    import os

    current_directory = os.getcwd()
    print("Current working directory:", current_directory)

