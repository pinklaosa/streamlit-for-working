import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="Document Management System",
    page_icon="📄",
    layout="wide"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Product Filter"

def navigate_to(page):
    st.session_state.current_page = page

# Filter products without factory code
def filter_products(data):
    if "รหัสสินค้า" in data.columns:
        return data[~data["รหัสสินค้า"].str.contains(r"^[^-]*-[^-]*-[^-]*", na=False)]
    return pd.DataFrame()

# Filter by SKU
def filter_by_sku(data, selected_skus):
    if "SKU" in data.columns and selected_skus:
        return data[data["SKU"].str[:6].isin(selected_skus)]
    return pd.DataFrame()

# Sidebar
with st.sidebar:
    st.title("Document Management")
    
    # Simple navigation buttons
    pages = ["Product Filter", "SKU Search", "Report"]
    for page in pages:
        if st.button(page, key=f"nav_{page}", use_container_width=True):
            st.session_state.current_page = page
    

# Main content based on selected page
if st.session_state.current_page == "Product Filter":
    st.title("📑 Product Code Filter")
    st.write("Filter products without factory codes")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"], key="product_file")
    if uploaded_file:
        try:
            data = pd.read_csv(uploaded_file, encoding="utf-8-sig")
        except UnicodeDecodeError:
            data = pd.read_csv(uploaded_file, encoding="iso-8859-11")
            
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("📌 Original Data:")
            st.dataframe(data.head(), use_container_width=True)
        
        if "รหัสสินค้า" in data.columns:
            filtered_data = filter_products(data)
            with col2:
                st.write("✅ Filtered Results:")
                st.dataframe(filtered_data, use_container_width=True)
            
            # Download button
            csv = filtered_data.to_csv(index=False, encoding="utf-8-sig")
            st.download_button(
                label="⬇️ Download Filtered Data",
                data=csv,
                file_name="filtered_data.csv",
                mime="text/csv",
            )
        else:
            st.error("⚠️ Column 'รหัสสินค้า' not found")

elif st.session_state.current_page == "SKU Search":
    st.title("🔍 SKU Search")
    st.write("Search and filter by SKU")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"], key="sku_file")
    if uploaded_file:
        try:
            data = pd.read_csv(uploaded_file, encoding="utf-8-sig")
        except UnicodeDecodeError:
            data = pd.read_csv(uploaded_file, encoding="iso-8859-11")
            
        if "SKU" in data.columns:
            col1, col2 = st.columns([1, 2])
            with col1:
                unique_skus = data["SKU"].dropna().str[:6].unique().tolist()
                selected_skus = st.multiselect("🛒 Select SKUs:", options=unique_skus)
            
            if selected_skus:
                filtered_data = filter_by_sku(data, selected_skus)
                with col2:
                    st.write("✅ Search Results:")
                    st.dataframe(filtered_data, use_container_width=True)
                
                # Download button
                csv = filtered_data.to_csv(index=False, encoding="utf-8-sig")
                st.download_button(
                    label="⬇️ Download Results",
                    data=csv,
                    file_name="sku_results.csv",
                    mime="text/csv",
                )
        else:
            st.error("⚠️ Column 'SKU' not found")

elif st.session_state.current_page == "Overview":
    st.title("📊 System Overview")
    
    # Sample metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Products", "1,250", "15%")
    with col2:
        st.metric("Processed Files", "45", "5")
    with col3:
        st.metric("Active Users", "12", "2")
    with col4:
        st.metric("Success Rate", "98.5%", "0.5%")

    # Recent activity table
    st.subheader("Recent Activity")
    activity_data = pd.DataFrame({
        'Time': pd.date_range(start=datetime.now() - timedelta(days=7), periods=5, freq='D'),
        'User': ['User A', 'User B', 'User C', 'User A', 'User B'],
        'Action': ['File Upload', 'Product Filter', 'SKU Search', 'Download', 'File Upload'],
        'Status': ['Completed', 'Completed', 'Completed', 'Completed', 'In Progress']
    })
    st.dataframe(activity_data, use_container_width=True)

elif st.session_state.current_page == "Report":
    st.title("📈 Reports")
    st.write("System usage and performance reports will be shown here.")