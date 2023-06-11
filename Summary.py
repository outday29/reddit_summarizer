from pathlib import Path

import streamlit as st
import yaml

# Create a Streamlit app
st.set_page_config(page_title="Reddit Summary")

# Set the path to the directory containing the top-level folders
report_path = Path("report")

col1, col2 = st.columns(2)

# Create a list of all the top-level folder names
top_folder_names = [folder.name for folder in report_path.iterdir() if folder.is_dir()]

# Create a dropdown menu to select the top-level folder
with col1:
    selected_top_folder = st.selectbox("Select datetime", top_folder_names)

# Get a list of all the middle-level folders in the selected top-level folder
middle_dir = report_path / selected_top_folder
middle_folder_names = [
    folder.name for folder in middle_dir.iterdir() if folder.is_dir()
]

# Create a dropdown menu to select the middle-level folder
with col2:
    selected_middle_folder = st.selectbox("Select subreddit", middle_folder_names)

# Get a list of all the YAML files in the selected middle-level folder
folder_path = middle_dir / selected_middle_folder
yaml_files = list(folder_path.glob("*.yaml"))

# Loop through each YAML file and display its contents in an article-like format
for yaml_file in yaml_files:
    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)
        st.write(f"### {data['title']}")
        st.write(f"##### User: {data['user']}")
        st.write(f"##### Link:")
        st.write(f"[{data['link']}]({data['link']})")
        st.write("\n")
        st.write(f"{data['description']}")
        st.write("---")
