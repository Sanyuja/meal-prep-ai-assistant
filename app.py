import streamlit as st
import pandas as pd
import smtplib
from email.message import EmailMessage
import os

st.set_page_config(
    page_title="Meal Prep AI Assistant",
    layout="centered"
)

st.title("🥗 First Course AI Assistant")
st.caption("Weekly meal planning for busy professionals & families")

# -----------------------------
# Load meals dataset
# -----------------------------
@st.cache_data
def load_meals():
    return pd.read_csv("meals.csv")

meals_df = load_meals()

# -----------------------------
# Helper functions
# -----------------------------
def filter_meals(df, diet_type, calorie_range, dislikes):
    filtered = df.copy()
    if diet_type != "Any":
        filtered = filtered[filtered["diet_type"] == diet_type]

    filtered = filtered[
        (filtered["calories"] >= calorie_range[0]) & 
        (filtered["calories"] <= calorie_range[1])
    ]

    if dislikes:
        dislike_list = [d.strip().lower() for d in dislikes.split(",")]
        for item in dislike_list:
            filtered = filtered[~filtered["ingredients"].str.lower().str.contains(item)]

    return filtered

def score_meals(df):
    scored = df.copy()
    scored["score"] = scored["protein_g"]
    scored = scored.sort_values(by="score", ascending=False)
    return scored

def generate_weekly_plan(df, meals_per_week):
    return df.head(meals_per_week)

def generate_grocery_list(df):
    ingredients_series = df["ingredients"].dropna()
    all_ingredients = []
    for item in ingredients_series:
        parts = [i.strip().lower() for i in item.split(",")]
        all_ingredients.extend(parts)
    grocery_df = pd.Series(all_ingredients).value_counts().reset_index()
    grocery_df.columns = ["ingredient", "quantity"]
    return grocery_df

# -----------------------------
# Service type & schedule
# -----------------------------
service_type = st.radio(
    "Service type",
    ["Meal delivery", "In-home cooking"]
)

if service_type == "In-home cooking":
    st.info("Your chef will come to your home to cook meals.")

    cooking_days = st.multiselect(
        "Select preferred cooking days",
        options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )

    cooking_time = st.selectbox(
        "Preferred cooking time",
        options=["Morning (8am–12pm)", "Afternoon (12pm–4pm)", "Evening (4pm–8pm)"]
    )
else:
    cooking_days = []
    cooking_time = ""

# -----------------------------
# Preferences form
# -----------------------------
st.divider()
st.subheader("Tell us about your preferences")

with st.form("preferences_form"):
    meals_per_week = st.selectbox(
        "Meals per week",
        options=[3, 5, 7, 10]
    )

    diet_type = st.selectbox(
        "Diet preference",
        options=["Any", "Omnivore", "Vegetarian", "Vegan"]
    )

    calorie_range = st.slider(
        "Preferred calories per meal",
        min_value=300,
        max_value=800,
        value=(400, 600),
        step=50
    )

    dislikes = st.text_input(
        "Ingredients to avoid (comma-separated)",
        placeholder="e.g. mushrooms, peanuts"
    )

    budget = st.selectbox(
        "Budget per meal ($)",
        options=["Any", "Under $13", "$13–$15", "$15+"]  # optional filtering later
    )

    submitted = st.form_submit_button("Generate my weekly plan")

# -----------------------------
# After form submission
# -----------------------------
if submitted:
    filtered = filter_meals(meals_df, diet_type, calorie_range, dislikes)

    if filtered.empty:
        st.warning("No meals match your preferences. Try adjusting filters.")
    else:
        scored = score_meals(filtered)
        weekly_plan = generate_weekly_plan(scored, meals_per_week)

        st.divider()
        st.subheader("Your Weekly Meal Plan")
        st.dataframe(
            weekly_plan[["meal_name", "calories", "protein_g", "diet_type", "price_estimate"]],
            use_container_width=True
        )

        st.divider()
        st.subheader("🛒 Weekly Grocery List")
        grocery_list = generate_grocery_list(weekly_plan)
        st.dataframe(
            grocery_list,
            use_container_width=True
        )

        # Schedule display for in-home cooking
        if service_type == "In-home cooking":
            st.divider()
            st.subheader("🧑‍🍳 In-Home Cooking Schedule")
            st.write(f"Days: {', '.join(cooking_days) if cooking_days else 'No days selected'}")
            st.write(f"Time: {cooking_time}")
        else:
            st.info("Your meals will be delivered in containers for the week.")

        # -----------------------------
        # Submit to Chef button (outside form)
        # -----------------------------
        st.divider()
        st.subheader("Submit Plan to Chef")

        if st.button("Submit to Chef"):
            # Save plan
            plan_to_save = weekly_plan.copy()
            plan_to_save["service_type"] = service_type
            if service_type == "In-home cooking":
                plan_to_save["cooking_days"] = ",".join(cooking_days)
                plan_to_save["cooking_time"] = cooking_time

            header = not os.path.exists("submitted_plans.csv")
            plan_to_save.to_csv("submitted_plans.csv", mode="a", index=False, header=header)

            st.success("Plan submitted to chef! Waiting for confirmation...")

            # Example email logic (commented)
            chef_email = "chef_email@example.com"
            client_email = "client_email@example.com"
            body_chef = f"""
New meal plan submitted!

Meals:
{weekly_plan[['meal_name','calories','protein_g','diet_type','price_estimate']].to_string(index=False)}

Service type: {service_type}
Cooking Days: {', '.join(cooking_days) if service_type == 'In-home cooking' else 'N/A'}
Cooking Time: {cooking_time if service_type == 'In-home cooking' else 'N/A'}
"""

            body_client = f"""
Your meal plan has been submitted to the chef!

Service type: {service_type}
Cooking Days: {', '.join(cooking_days) if service_type == 'In-home cooking' else 'N/A'}
Cooking Time: {cooking_time if service_type == 'In-home cooking' else 'N/A'}

You will receive a confirmation once the chef confirms.
"""

            # send_email(chef_email, "New Meal Plan Submitted", body_chef)
            # send_email(client_email, "Your Meal Plan Submitted", body_client)

            st.info("Emails would be sent to chef and client here (uncomment send_email lines after adding credentials).")

# -----------------------------
# Display all available meals
# -----------------------------
st.divider()
st.subheader("Available Meals")
st.dataframe(
    meals_df,
    use_container_width=True
)
