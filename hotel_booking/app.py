import streamlit as st
import pandas as pd
import os

# -------- Page Config --------
st.set_page_config(page_title="Hotel Booking Analysis", layout="wide")
st.title("🏨 Hotel Booking Analysis Project")

# -------- Load CSV Safely --------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "hotel_bookings 2.csv")

if not os.path.exists(csv_path):
    st.error("❌ hotel_bookings 2.csv not found!")
    st.info("Upload the CSV file to the same folder as app.py")
    st.stop()

df = pd.read_csv(csv_path)

# -------- Data Cleaning --------
df['reservation_status_date'] = pd.to_datetime(
    df['reservation_status_date'], errors='coerce'
)

df.drop(['company', 'agent'], axis=1, inplace=True, errors='ignore')
df.dropna(inplace=True)
df = df[df['adr'] < 5000]

# -------- Dataset Preview --------
st.subheader("📊 Dataset Preview")
st.dataframe(df.head())

# -------- Cancellation Rate --------
st.subheader("❌ Cancellation Rate")

cancel_rate = df['is_canceled'].value_counts(normalize=True)

st.bar_chart(cancel_rate)

# -------- Hotel-wise Cancellation --------
st.subheader("🏨 Cancellation by Hotel Type")

hotel_cancel = df.groupby('hotel')['is_canceled'].mean()
st.bar_chart(hotel_cancel)

# -------- Monthly Trend --------
st.subheader("📅 Monthly Reservation Trend")

df['month'] = df['reservation_status_date'].dt.month
monthly_data = df.groupby(['month', 'is_canceled']).size().unstack()
st.line_chart(monthly_data)

# -------- Top Countries --------
st.subheader("🌍 Top 10 Countries with Cancellations")

top_countries = (
    df[df['is_canceled'] == 1]['country']
    .value_counts()
    .head(10)
)

st.bar_chart(top_countries)
