import streamlit as st
import pandas as pd
from streamlit_markmap import markmap

# Pengaturan halaman Streamlit
st.set_page_config(page_title="Generate Mind Map from CSV", layout="wide")

# Fungsi untuk mengubah DataFrame menjadi format markdown untuk mind map
def df_to_markdown(df):
    markdown = "# Mind Map\n"
    
    # Mengelompokkan data berdasarkan Cluster Name
    cluster_groups = df.groupby('Cluster Name')
    
    for cluster_name, cluster_group in cluster_groups:
        markdown += f"## {cluster_name}\n"  # Level Cluster Name
        
        # Mengelompokkan data berdasarkan Parent Keyword di dalam Cluster Name
        parent_groups = cluster_group.groupby('Parent Keyword')
        
        for parent_keyword, parent_group in parent_groups:
            markdown += f"### {parent_keyword}\n"  # Level Parent Keyword
            
            # Menambahkan setiap Cluster Member di bawah Parent Keyword
            for keyword in parent_group['Cluster Member'].unique():
                markdown += f"- {keyword}\n"  # Level Cluster Member
    
    return markdown

# Upload CSV di sidebar
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    # Membaca CSV ke DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Membersihkan spasi tambahan di nama kolom
    df.columns = df.columns.str.strip()
    
    # Mendapatkan daftar cluster yang tersedia
    available_clusters = df['Cluster Name'].unique()
    default_selection = available_clusters[:5]  # Memilih 5 cluster pertama sebagai default
    
    # Checkbox untuk "Select All"
    select_all = st.sidebar.checkbox("Select All Clusters", value=False)
    
    # Jika "Select All" dipilih, pilih semua cluster, jika tidak, gunakan multiselect
    if select_all:
        selected_clusters = available_clusters.tolist()
    else:
        selected_clusters = st.sidebar.multiselect(
            "Pilih Cluster untuk ditampilkan:",
            options=available_clusters,
            default=default_selection
        )
    
    # Filter DataFrame berdasarkan cluster yang dipilih
    filtered_df = df[df['Cluster Name'].isin(selected_clusters)]
    
    # Membuat Tabs
    tab1, tab2 = st.tabs(["🌐 Mind Map", "📄 Data"])
    
    # Tab 1: Menampilkan Mind Map
    with tab1:
        # Mengonversi DataFrame yang sudah difilter menjadi markdown
        markdown_data = df_to_markdown(filtered_df)
        st.write("### Mind Map")
        markmap(markdown_data, height=600)  # Menambah tinggi untuk tampilan yang lebih besar
    
    # Tab 2: Menampilkan Data
    with tab2:
        st.write("### Data dari CSV (Filtered)")
        st.write(filtered_df)
else:
    st.sidebar.write("Silakan upload file CSV untuk membuat mind map.")
