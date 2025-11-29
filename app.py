import streamlit as st
import pandas as pd
from joblib import load

# 👇 IMPORTANT: import custom transformer so unpickling works
from custom_transformers import YearToAgeTransformer

# ============================================================
# Load the pipeline
# ============================================================
@st.cache_resource
def load_pipeline():
    pipe = load("car_price_pipeline.pkl")   # same folder
    return pipe

pipeline = load_pipeline()

# ============================================================
# Streamlit UI
# ============================================================
st.title("🚗 Used Car Price Estimator (Demo MLOps Pipeline)")
st.write(
    "This app uses a saved sklearn **pipeline (.pkl)** with preprocessing "
    "(feature engineering, KNN imputation, scaling, encoding) + model to "
    "predict the selling price of a used car."
)

st.markdown("---")

# -------- Inputs from user --------
col1, col2 = st.columns(2)

with col1:
    year = st.number_input("Model Year", min_value=1995, max_value=2025, value=2014, step=1)
    present_price = st.number_input(
        "Present Price (New car price in Lakhs)", min_value=0.0, max_value=50.0, value=6.87, step=0.1
    )
    kms_driven = st.number_input(
        "Kms Driven", min_value=0, max_value=500000, value=42450, step=500
    )

with col2:
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
    seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
    owner = st.selectbox("Number of Previous Owners", [0, 1, 2, 3])

st.markdown("---")

if st.button("Predict Selling Price"):
    # Build a single-row DataFrame matching training feature names
    input_df = pd.DataFrame(
        [{
            "Year": year,
            "Present_Price": present_price,
            "Kms_Driven": kms_driven,
            "Fuel_Type": fuel_type,
            "Seller_Type": seller_type,
            "Transmission": transmission,
            "Owner": owner,
        }]
    )

    # Raw model prediction from pipeline
    raw_pred = pipeline.predict(input_df)[0]

    # Optional: clamp suggestion to a reasonable range (demo/business rule)
    lower_bound = 0.4 * present_price
    upper_bound = present_price
    suggested_price = max(lower_bound, min(raw_pred, upper_bound))

    st.subheader("🔮 Model Output")
    st.write(f"**Raw model prediction:** `{raw_pred:.2f} Lakhs`")

    st.subheader("💡 Suggested Selling Price Range (with business rule)")
    st.write(
        f"- Lower bound (40% of Present Price): `{lower_bound:.2f} Lakhs`\n"
        f"- Upper bound (100% of Present Price): `{upper_bound:.2f} Lakhs`\n"
        f"- **Suggested price (clamped):** `{suggested_price:.2f} Lakhs`"
    )

    st.caption(
        "Note: This is a toy model trained on a small dataset, mainly for demonstrating "
        "end-to-end MLOps (pipeline → .pkl → app → Docker → CI/CD → Azure)."
    )
