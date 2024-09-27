import streamlit as st
import pymongo
import datetime
import calendar
import pandas as pd

# run command

# python3 -m streamlit run  "/home/dell/Documents/streamlit_app/code/first demo.py" --server.port 8585

# mongodb connection
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Localhost connection
db = client["diamond"]  # Replace with your desired database name
collection = db["diamond_data"]

# page configuration for page name, icon , full screen
st.set_page_config(
    page_title="My Awesome App",
    page_icon="🧊",  # Or a URL to an image
    layout="wide",  # Can be "centered" or "wide"
    initial_sidebar_state="expanded"  # Can be "auto", "expanded", or "collapsed"
)

# usernames and passwords
user_dict = {"admin": "admin"}

# all variables that will help to select report filters

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
        # """Formats a datetime object as dd-mm-yyyy.
        #   Args:
        #     date_object: The datetime object to format.
        #   Returns:
        #     A string representing the date in dd-mm-yyyy format.
        #   """
        return date_object.strftime("%d-%m-%Y")
      
      def load_data_from_mongodb(start_date,end_date):
        res = collection.find({"sale_date": {"$gte": start_date, "$lte": end_date}})
        return pd.DataFrame(list(res))
      
      row_data = load_data_from_mongodb(change_date_formate_dd_mm_yyy(selected_from), change_date_formate_dd_mm_yyy(selected_to))

      st_expander = st.expander("Data Filters")

      with st_expander:
        
        col1, col2, col3 = st.columns([1,1,1])
        
        with col1:
          selected_report = st.selectbox("Select Report Type:", report_list, index=0)
        
        with col2:
          selected_model = st.multiselect("Select Cars Models:", row_data["model"].unique(),placeholder="Select Car Models...")

        with col3:
          temp_data = row_data.loc[(row_data["model"].isin(selected_model))]
          selected_color = st.multiselect("Select Cars Color.", temp_data["color"].unique(),placeholder="Selec Car Color")

        get_report = st.button("Get Report")
      
      st.write("len",len(row_data))

      if get_report:

        def get_sale_report(data):
          # total_sale = sum(data["price"])-sum(data["purchase_price"])
          total_sale = sum(data["price"])
          print(total_sale)
          total_customer = len(data["name"].unique())
          total_sold_cars = len(data["name"])

          col1,col2,col3 = st.columns([1,1,1])
          with col1:
            st.write("Total Revenue: ", total_sale)
          with col2:
            st.write("Total Cutomers: ", total_customer)
          with col3:
            st.write("Total Cars: ", total_sold_cars)

        if selected_report == "Sale Report" and selected_report in report_list:
          sale_data = row_data.loc[(row_data["model"].isin(selected_model))]
          sale_data = sale_data.loc[(sale_data["color"].isin(selected_color))]
          get_sale_report(sale_data)
        st.write("selected Report: ", selected_report)
        st.write("from: ", change_date_formate_dd_mm_yyy(selected_from))
        st.write("To: ", change_date_formate_dd_mm_yyy(selected_to))

  else:
    st.error("Username and Password is not currect.")