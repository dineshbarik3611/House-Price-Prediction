
import streamlit as st
import pandas as pd
import pickle
import os
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="House Price Prediction System",
    page_icon="🏠",
    layout="wide"
)

# ==========================================
# 2. LOAD TRAINED MODEL
# ==========================================

MODEL_PATH = "house_price_model.pkl"

try:
    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)

except FileNotFoundError:
    st.error("Model file not found! Check house_price_model.pkl")
    st.stop()

except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()


# ==========================================
# 3. SESSION STATE
# ==========================================

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None


# ==========================================
# 4. CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #f0f4f8;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

h1 {
    color: #173b65;
    font-weight: bold;
}

h2, h3 {
    color: #1e3a8a;
}

p {
    color: #475569;
}

.stButton > button {
    background-color: #2563eb;
    color: white;
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
    border: none;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

div[data-testid="stNumberInput"] input {
    border-radius: 8px;
}

div[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #dbeafe;
}

.result-card {
    background-color: #dbeafe;
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    border: 2px solid #2563eb;
    margin-top: 20px;
}

.result-price {
    color: #1d4ed8;
    font-size: 42px;
    font-weight: bold;
}

.footer {
    text-align: center;
    color: #64748b;
    padding: 25px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 5. SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🏠 House Predictor")

    st.write("Machine Learning Based Application")

    st.divider()

    st.subheader("Project Information")

    st.write("**Algorithm:** Linear Regression")

    st.write("**Dataset:** California Housing")

    st.write("**Framework:** Streamlit")

    st.write("**Language:** Python")

    st.divider()

    st.metric(
        "Total Predictions",
        len(st.session_state.prediction_history)
    )

    st.info("Enter house details to estimate its market value.")


# ==========================================
# 6. APPLICATION HEADER
# ==========================================

st.title("🏠 House Price Prediction System")

st.write(
    "Predict estimated house prices using a trained "
    "Machine Learning model."
)

st.divider()


# ==========================================
# 7. HOUSE INPUT FORM
# ==========================================

st.subheader("🏡 Enter House Details")

with st.form("house_prediction_form"):

    col1, col2 = st.columns(2)

    with col1:

        longitude = st.number_input(
            "Longitude",
            value=-122.23,
            format="%.5f"
        )

        latitude = st.number_input(
            "Latitude",
            value=37.88,
            format="%.5f"
        )

        housing_median_age = st.number_input(
            "Housing Median Age",
            min_value=1,
            value=41
        )

        total_rooms = st.number_input(
            "Total Rooms",
            min_value=1,
            value=880
        )

    with col2:

        total_bedrooms = st.number_input(
            "Total Bedrooms",
            min_value=1,
            value=129
        )

        population = st.number_input(
            "Population",
            min_value=1,
            value=322
        )

        households = st.number_input(
            "Households",
            min_value=1,
            value=126
        )

        median_income = st.number_input(
            "Median Income",
            min_value=0.0,
            value=8.3252,
            format="%.4f"
        )

    st.divider()

    predict_button = st.form_submit_button(
        "🔍 Predict House Price",
        use_container_width=True
    )


# ==========================================
# 8. PREDICTION LOGIC
# ==========================================

if predict_button:

    input_data = pd.DataFrame([[
        longitude,
        latitude,
        housing_median_age,
        total_rooms,
        total_bedrooms,
        population,
        households,
        median_income
    ]], columns=[
        "longitude",
        "latitude",
        "housing_median_age",
        "total_rooms",
        "total_bedrooms",
        "population",
        "households",
        "median_income"
    ])

    try:

        prediction = float(model.predict(input_data)[0])

        st.session_state.last_prediction = prediction

        # Save prediction history

        st.session_state.prediction_history.append({

            "Date": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            ),

            "Longitude": longitude,
            "Latitude": latitude,
            "House Age": housing_median_age,
            "Total Rooms": total_rooms,
            "Total Bedrooms": total_bedrooms,
            "Population": population,
            "Households": households,
            "Median Income": median_income,

            "Predicted Price": round(prediction, 2)

        })

        st.success("House price predicted successfully!")

    except Exception as e:

        st.error(f"Prediction failed: {e}")


# ==========================================
# 9. DISPLAY PREDICTION RESULT
# ==========================================
if st.session_state.last_prediction is not None:

    st.divider()
    st.subheader("🏡 House Price Prediction Result")

    st.markdown(
        f"""
<div class="result-card">
    <h3>Estimated House Price</h3>
    <div class="result-price">
        ${st.session_state.last_prediction:,.2f}
    </div>
    <p>Your house price prediction is ready!</p>
</div>
""",
        unsafe_allow_html=True
    )



# ==========================================
# 10. PREDICTION HISTORY
# ==========================================

st.divider()

st.subheader("📊 Prediction History")

if st.session_state.prediction_history:

    history_df = pd.DataFrame(
        st.session_state.prediction_history
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    # Download CSV

    csv = history_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Prediction History",
        data=csv,
        file_name="prediction_history.csv",
        mime="text/csv"
    )

    # Clear History

    if st.button("🗑️ Clear Prediction History"):

        st.session_state.prediction_history = []

        st.session_state.last_prediction = None

        st.rerun()

else:

    st.info("No prediction history available yet.")


# ==========================================
# 11. FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div class="footer">

        <h4>🏠 House Price Prediction System</h4>

        <p>Powered by Python, Machine Learning and Streamlit</p>

        <p>© 2026 House Price Prediction Project</p>

    </div>
    """,
    unsafe_allow_html=True
)
