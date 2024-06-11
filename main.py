import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# set page configuration
st.set_page_config(page_title="Data Visualizer",
                   layout="centered",
                   page_icon="📊")

# Title
st.title("📊 Data Visualizer 72 - Web App")

# Upload a CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Dropdown for pre-existing files in the data folder
working_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = f"{working_dir}/data"
files_list = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

# Include an option to select a file from the folder or upload a new one
selected_file = st.selectbox("Or select a file from the folder", ["None"] + files_list)

df = None

def read_csv_file(file):
    encodings = ['utf-8', 'iso-8859-1', 'latin1']
    for encoding in encodings:
        try:
            return pd.read_csv(file, encoding=encoding), encoding
        except UnicodeDecodeError:
            continue
        except pd.errors.EmptyDataError:
            return None, None
    return None, None

if uploaded_file is not None:
    df, encoding = read_csv_file(uploaded_file)
    if df is not None:
        st.success(f"Uploaded {uploaded_file.name} successfully with encoding {encoding}!")
    else:
        st.error("There was an error reading the file. Please ensure it is a valid CSV file and not empty.")

elif selected_file != "None":
    # Read the file from the folder
    file_path = os.path.join(folder_path, selected_file)
    df, encoding = read_csv_file(file_path)
    if df is not None:
        st.success(f"Selected {selected_file} successfully with encoding {encoding}!")
    else:
        st.error("There was an error reading the file. Please ensure it is a valid CSV file and not empty.")

if df is not None:
    col1, col2 = st.columns(2)
    columns = df.columns.tolist()

    with col1:
        st.write("")
        st.write(df.head())

    with col2:
        # User selection of df columns
        x_axis = st.selectbox("Select the X-Axis", options=columns + ["None"])
        y_axis = st.selectbox("Select the Y-Axis", options=columns + ["None"])

        plot_list = ["Line Plot", "Bar Chart", "Scatter Plot", "Distribution Plot", "Count Plot"]

        selected_plot = st.selectbox("Select a Plot", options=plot_list)
        st.write(x_axis)
        st.write(y_axis)
        st.write(selected_plot)

    # Button to generate plots
    if st.button("Generate Plot"):
        fig, ax = plt.subplots(figsize=(6, 4))
        if selected_plot == "Line Plot":
            sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)

        elif selected_plot == "Bar Chart":
            sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)

        elif selected_plot == "Scatter Plot":
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)

        elif selected_plot == "Distribution Plot":
            sns.histplot(df[x_axis], kde=True, ax=ax)

        elif selected_plot == "Count Plot":
            sns.countplot(x=df[x_axis], ax=ax)

        # Adjust label sizes
        ax.tick_params(axis="x", labelsize=10)
        ax.tick_params(axis="y", labelsize=10)

        plt.title(f"{selected_plot} of {y_axis} vs {x_axis}", fontsize=12)
        plt.xlabel(x_axis, fontsize=10)
        plt.ylabel(y_axis, fontsize=10)

        st.pyplot(fig)

