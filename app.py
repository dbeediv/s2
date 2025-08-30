# Main Streamlit app code here
import streamlit as st
from modules import ocr_module, ml_module, recipe_module, chatbot_module, analytics_module
import sqlite3
import os
from PIL import Image

# Database setup
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS inventory
             (id INTEGER PRIMARY KEY, item TEXT, expiry_date TEXT, quantity INTEGER, spoilage_risk REAL)''')
conn.commit()

# Sidebar
st.sidebar.title("Smart Sustainable Food Assistant")
menu = ["Home", "Upload Image", "ML Prediction", "Recipe Recommender", "Chatbot", "Analytics"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.title("Welcome to Smart Sustainable Food Assistant")
    st.write("Use the menu to navigate through features.")

elif choice == "Upload Image":
    st.subheader("Upload Image for OCR")
    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        text = ocr_module.extract_text(image)
        st.write("Extracted Text:")
        st.text(text)
        # Optionally parse text to DB
        parsed_items = ocr_module.parse_inventory(text)
        for item, qty, expiry in parsed_items:
            c.execute("INSERT INTO inventory (item, expiry_date, quantity, spoilage_risk) VALUES (?, ?, ?, ?)",
                      (item, expiry, qty, 0))
        conn.commit()
        st.success("Items added to inventory!")

elif choice == "ML Prediction":
    st.subheader("Spoilage Risk Prediction")
    df = ml_module.get_inventory(conn)
    if df.empty:
        st.warning("Inventory is empty. Upload items first.")
    else:
        predictions = ml_module.predict_spoilage(df)
        st.dataframe(predictions)
        # Update DB with spoilage risk
        for idx, row in predictions.iterrows():
            c.execute("UPDATE inventory SET spoilage_risk=? WHERE id=?", (row['spoilage_risk'], row['id']))
        conn.commit()
        st.success("Predictions updated!")

elif choice == "Recipe Recommender":
    st.subheader("Recipes from Inventory")
    df = ml_module.get_inventory(conn)
    recipes = recipe_module.suggest_recipes(df)
    for rec in recipes:
        st.write(f"- {rec}")

elif choice == "Chatbot":
    st.subheader("Ask your assistant")
    user_input = st.text_input("Type your question")
    if user_input:
        response = chatbot_module.get_response(user_input, conn)
        st.write(response)

elif choice == "Analytics":
    st.subheader("Inventory Analytics")
    df = ml_module.get_inventory(conn)
    analytics_module.show_charts(df)
