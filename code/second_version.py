import streamlit as st
import pymongo
import datetime
import calendar
import pandas as pd

# run command

# python3 -m streamlit run  "/home/dell/Documents/streamlit_app/code/second_version.py" --server.port 8585

client = pymongo.MongoClient("mongodb://localhost:27017/")  # Localhost connection
db = client["diamond"]  # Replace with your desired database name
collection = db["streamlit data"]

# page configuration for page name, icon , full screen
st.set_page_config(
    page_title="My Awesome App",
    page_icon="🧊",  # Or a URL to an image
    layout="wide",  # Can be "centered" or "wide"
    initial_sidebar_state="expanded"  # Can be "auto", "expanded", or "collapsed"
)

# usernames and passwords
user_dict = {"admin": "admin"}

# All Report that can be create from this app
report_list = ["Sale Report", "Stock Report", "Location wise sale","sale Person","Quick Sale", "Model wise Sale","Monthly Sale Comparison", "Data List", "customer List", "Vendor List"]

# show selection for value or count
data_value_type = ["Count", "Total Value"]

# user login
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

# checkbox to login
stay_loged_in = st.sidebar.checkbox("log In")


if stay_loged_in:
  
  # condition to check username and password is currect or not
    if username in user_dict and user_dict[username] == password:
        # from date to To date user input
        selected_from = st.sidebar.date_input("Select From")
        selected_to = st.sidebar.date_input("Select TO")

    # Check box to load data
    load_data = st.sidebar.checkbox("Load Data")

    if load_data:

        def change_date_formate_dd_mm_yyy(date_object):
            return date_object.strftime("%d-%m-%Y")
        
        def load_data_from_mongodb(start_date,end_date):
            res = collection.find({"sale_date": {"$gte": start_date, "$lte": end_date}})
            return pd.DataFrame(list(res))
        
        row_data = load_data_from_mongodb(change_date_formate_dd_mm_yyy(selected_from), change_date_formate_dd_mm_yyy(selected_to))

        st_expander = st.expander("Data Filters")
        st.write(len(row_data))
    else:
        st.error("Username and Password is not currect.")