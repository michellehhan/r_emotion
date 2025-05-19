import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned CSV
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_remotion_data.csv")
    return df

df = load_data()

st.title("📒 ReMotion Journaling Survey Dashboard")
st.write("Explore participant preferences and attitudes around journaling and AI support.")

# Filter: Region
region_options = ['All'] + sorted(df['Region'].dropna().unique().tolist())
selected_region = st.selectbox("Filter by Region:", region_options)

filtered_df = df if selected_region == 'All' else df[df['Region'] == selected_region]

# Section: Reasons for Journaling (Q61)
st.subheader("📝 Why Do People Journal?")

q61_clean = filtered_df['Q61'].dropna().astype(str)
q61_split = q61_clean.str.split(',').explode().str.strip()
q61_counts = q61_split.value_counts().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=q61_counts.values, y=q61_counts.index, ax=ax, color="#4c72b0")
ax.set_title("Reasons for Journaling")
ax.set_xlabel("Count")
st.pyplot(fig)

# Section: AI Comfort (Q71)
st.subheader("🤖 AI Comfort Level")

q71_map = {
    -2: 'Strongly Disagree', -1: 'Somewhat Disagree', 0: 'Neutral',
     1: 'Somewhat Agree', 2: 'Strongly Agree'
}
q71_counts = filtered_df['Q71'].value_counts().sort_index().rename(index=q71_map)

fig2, ax2 = plt.subplots()
sns.barplot(x=q71_counts.values, y=q71_counts.index, ax=ax2, palette="coolwarm")
ax2.set_title("Comfort with AI Analyzing Entries")
ax2.set_xlabel("Count")
st.pyplot(fig2)
