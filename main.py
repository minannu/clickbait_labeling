import streamlit as st
import pandas as pd
import os
import matplotlib.image as mpimg

# Set the password for session
PASSWORD = "ruetcse"

# Load dataframe
@st.cache_data
def load_data():
    # Example dataframe loading (replace with your dataset path)
    df = pd.read_csv("dataset.csv")
    return df

# Create a new dataframe to store labeled data if it doesn't exist
def load_labeled_data():
    if os.path.exists("labeled_dataset.csv"):
        return pd.read_csv("labeled_dataset.csv")
    else:
        return pd.DataFrame(columns=['video_id', 'label', 'title', 'description', 'view_count', 'like_count',
                                     'thumbnail_url', 'local_thumbnail_path', 'duration', 'upload_date',
                                     'channel_id', 'channel_name', 'video_url'])

# Function to load and display image using matplotlib
def load_image(image_path):
    image = mpimg.imread(image_path)
    return image

# Function to save labeled dataframe to CSV using Unicode encoding
def save_to_csv():
    if not st.session_state.labeled_df.empty:
        st.session_state.labeled_df.to_csv("labeled_dataset.csv", index=False, encoding='utf-8-sig')
        with open("current_index.txt", "w", encoding='utf-8-sig') as f:
            f.write(str(st.session_state.index))
        st.success("Labeled data and current index saved successfully!")

# Function to load saved index
def load_index():
    try:
        if os.path.exists("current_index.txt"):
            with open("current_index.txt", "r", encoding='utf-8-sig') as f:
                index = int(f.read())
                return index
    except Exception as e:
        st.error(f"Error loading index: {e}")
    return 0

# Password protection
def check_password():
    """Check if the user enters the correct password."""
    password = st.text_input("Enter password:", type="password")
    if password == PASSWORD:
        return True
    elif password:
        st.error("Incorrect password!")
    return False

# Display content and handle button click
def main():
    # Password protection at the start
    if not check_password():
        return
    
    # Load dataframe
    df = load_data()

    # Load previous labeled data
    if "labeled_df" not in st.session_state:
        st.session_state.labeled_df = load_labeled_data()

    # Load previous index if available
    if "index" not in st.session_state:
        st.session_state.index = load_index()

    index = st.session_state.index

    # Display current status in an expander
    with st.expander("Current Status", expanded=True):
        st.write(f"Current Row Number: {index + 1}")
        if index >= len(df):
            st.write("No more items to review.")
            st.write("Labeled Data:")
            st.dataframe(st.session_state.labeled_df)
            save_to_csv()
            return

    # Get the current row to display
    row = df.iloc[index]

    # Image display section
    with st.expander(f"Video: {row['title']}", expanded=True):
        image = load_image(row["local_thumbnail_path"])
        st.image(image, caption=row["title"], use_column_width=True)
        st.write(f"**Title:** {row['title']}")
        st.write(f"**Description:** {row['description']}")

    # Labeling options
    with st.expander("Labeling", expanded=True):
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
