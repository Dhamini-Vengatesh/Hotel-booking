import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Hotel Booking Analysis",
    layout="wide"
)

st.title("🏨 Hotel Booking Analysis Project")

# ---------------- Load Dataset Safely ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "hotel_bookings 2.csv")

if not os.path.exists(csv_path):
    st.error("❌ hotel_bookings 2.csv not found!")
    st.info("👉 Place the CSV file in the SAME folder as app.py")
    st.stop()

df = pd.read_csv(csv_path)

# ---------------- Data Preprocessing ----------------
df['reservation_status_date'] = pd.to_datetime(
    df['reservation_status_date'],
    errors='coerce'
)

df.drop(['company', 'agent'], axis=1, inplace=True, errors='ignore')
df.dropna(inplace=True)
df = df[df['adr'] < 5000]

# ---------------- Dataset Preview ----------------
st.subheader("📊 Dataset Preview")
st.dataframe(df.head())

# ---------------- Cancellation Percentage ----------------
st.subheader("❌ Reservation Cancellation Percentage")

cancelled_percent = df['is_canceled'].value_counts(normalize=True)

fig1, ax1 = plt.subplots(figsize=(5, 4))
ax1.bar(
    ['Not Cancelled', 'Cancelled'],
    df['is_canceled'].value_counts(),
    width=0.7
)
ax1.set_title("Reservation Status Count")
st.pyplot(fig1)

# ---------------- Hotel Type vs Cancellation ----------------
st.subheader("🏨 Reservation Status by Hotel Type")

fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.countplot(
    x='hotel',
    hue='is_canceled',
    data=df,
    palette='rocket',
    ax=ax2
)
ax2.set_xlabel("Hotel Type")
ax2.set_ylabel("Number of Reservations")
ax2.legend(['Not Canceled', 'Canceled'], bbox_to_anchor=(1, 1))
st.pyplot(fig2)

# ---------------- Average Daily Rate Trend ----------------
st.subheader("📈 Average Daily Rate (ADR) Trend")

resort_hotel = df[df['hotel'] == 'Resort Hotel']
city_hotel = df[df['hotel'] == 'City Hotel']

resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()

fig3, ax3 = plt.subplots(figsize=(20, 8))
ax3.plot(resort_hotel.index, resort_hotel['adr'], label='Resort Hotel')
ax3.plot(city_hotel.index, city_hotel['adr'], label='City Hotel')
ax3.set_title("Average Daily Rate in City and Resort Hotels", fontsize=20)
ax3.legend()
st.pyplot(fig3)

# ---------------- Reservation Status per Month ----------------
st.subheader("📅 Reservation Status per Month")

df['month'] = df['reservation_status_date'].dt.month

fig4, ax4 = plt.subplots(figsize=(16, 8))
sns.countplot(
    x='month',
    hue='is_canceled',
    data=df,
    palette='rocket',
    ax=ax4
)
ax4.set_xlabel("Month")
ax4.set_ylabel("Number of Reservations")
ax4.set_title("Reservation Status per Month")
ax4.legend(['Not Canceled', 'Canceled'], bbox_to_anchor=(1, 1))
st.pyplot(fig4)

# ---------------- Top 10 Countries with Cancellations ----------------
st.subheader("🌍 Top 10 Countries with Reservation Cancellations")

cancelled_data = df[df['is_canceled'] == 1]
top_10_country = cancelled_data['country'].value_counts()[:10]

fig5, ax5 = plt.subplots(figsize=(8, 8))
ax5.pie(
    top_10_country,
    labels=top_10_country.index,
    autopct='%.2f%%'
)
ax5.set_title("Top 10 Countries with Reservation Cancellations")
st.pyplot(fig5)
