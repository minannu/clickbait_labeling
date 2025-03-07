import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Load dataframe
@st.cache_data
def load_data():
    # Example dataframe loading (replace with your dataset path)
    df = pd.read_csv("dataset.csv")
    return df

# Create a new dataframe to store labeled data
if "labeled_df" not in st.session_state:
    st.session_state.labeled_df = pd.DataFrame(columns=["channel_id", "image", "title", "description", "label"])

# Function to load and display image using matplotlib
def load_image(image_path):
    image = mpimg.imread(image_path)
    return image

# Function to save labeled dataframe to CSV
def save_to_csv():
    if not st.session_state.labeled_df.empty:
        st.session_state.labeled_df.to_csv("labeled_dataset.csv", index=False)
        st.success("Labeled data saved successfully!")

# Display content and handle button click
def main():
    st.title("Dataset Review App")
    df = load_data()
    
    # Session state to keep track of current index
    if "index" not in st.session_state:
        st.session_state.index = 0

    index = st.session_state.index
    
    if index >= len(df):
        st.write("No more items to review.")
        st.write("Labeled Data:")
        st.dataframe(st.session_state.labeled_df)
        save_to_csv()
        return

    row = df.iloc[index]
    
    image = load_image(row["local_thumbnail_path"])
    st.image(image, caption=row["title"], use_column_width=True)
    st.write(f"**Title:** {row['title']}")
    st.write(f"**Description:** {row['description']}")
    st.write(' Now provide your opinion Clickbait or not:')
    
    col1, col2 = st.columns(2)
    def save_label(label):
        new_row = row.copy()
        new_row["label"] = label
        st.session_state.labeled_df = pd.concat([st.session_state.labeled_df, pd.DataFrame([new_row])], ignore_index=True)
        st.session_state.index += 1
        save_to_csv()
        st.rerun()

    with col1:
        if st.button("Yes"):
            save_label("Yes")
    with col2:
        if st.button("No"):
            save_label("No")

if __name__ == "__main__":
    main()