import streamlit as st
import pandas as pd
from datetime import date, datetime
import os

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="First Course — Meal Prep",
    layout="centered"
)

st.title("🥗 First Course")
st.caption("Thoughtful weekly meal planning, made personal.")

# -----------------------------
# Load meals
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
        for item in dislikes.split(","):
            filtered = filtered[
                ~filtered["ingredients"].str.lower().str.contains(item.strip().lower())
            ]

    return filtered

def score_meals(df):
    scored = df.copy()
    scored["score"] = scored["protein_g"]
    return scored.sort_values("score", ascending=False)

def generate_grocery_list(df):
    ingredients = []
    for row in df["ingredients"].dropna():
        ingredients.extend([i.strip().lower() for i in row.split(",")])

    grocery_df = pd.Series(ingredients).value_counts().reset_index()
    grocery_df.columns = ["ingredient", "quantity"]
    return grocery_df

# -----------------------------
# Session state initialization
# -----------------------------
if "weekly_plan" not in st.session_state:
    st.session_state.weekly_plan = None

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# -----------------------------
# Client info
# -----------------------------
st.subheader("Your details")

client_name = st.text_input("Full name")
client_email = st.text_input("Email")
client_phone = st.text_input("Phone number")
start_date = st.date_input("Preferred start date", min_value=date.today())

# -----------------------------
# Service type
# -----------------------------
st.subheader("Service type")

service_type = st.radio(
    "",
    ["Meal delivery", "In-home cooking"]
)

if service_type == "In-home cooking":
    cooking_days = st.multiselect(
        "Preferred cooking days",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )

    cooking_time = st.selectbox(
        "Preferred cooking time",
        ["Morning (8–12)", "Afternoon (12–4)", "Evening (4–8)"]
    )
else:
    cooking_days = []
    cooking_time = ""

# -----------------------------
# Preferences form
# -----------------------------
st.subheader("Meal preferences")

with st.form("preferences_form"):
    meals_per_week = st.selectbox("Meals per week", [3, 5, 7, 10])
    diet_type = st.selectbox("Diet type", ["Any", "Omnivore", "Vegetarian", "Vegan"])
    calorie_range = st.slider(
        "Calories per meal", 300, 800, (400, 600), step=50
    )
    dislikes = st.text_input("Ingredients to avoid")

    generate = st.form_submit_button("Generate my plan")

# -----------------------------
# Generate meal plan
# -----------------------------
if generate:
    filtered = filter_meals(meals_df, diet_type, calorie_range, dislikes)

    if filtered.empty:
        st.warning("No meals match your preferences.")
        st.session_state.weekly_plan = None
    else:
        st.session_state.weekly_plan = score_meals(filtered).head(meals_per_week)
        st.session_state.submitted = False  # reset submission

# -----------------------------
# Display generated plan
# -----------------------------
if st.session_state.weekly_plan is not None:
    weekly_plan = st.session_state.weekly_plan
    grocery_list = generate_grocery_list(weekly_plan)

    st.subheader("Your weekly meal plan")
    st.dataframe(
        weekly_plan[
            ["meal_name", "calories", "protein_g", "diet_type", "price_estimate"]
        ],
        use_container_width=True
    )

    st.subheader("🛒 Grocery list")
    st.dataframe(grocery_list, use_container_width=True)

    st.divider()
    st.subheader("Submit to chef")

    if st.button("Submit plan"):
        submission_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        plan_to_save = weekly_plan.copy()
        plan_to_save["submission_id"] = submission_id
        plan_to_save["client_name"] = client_name
        plan_to_save["client_email"] = client_email
        plan_to_save["client_phone"] = client_phone
        plan_to_save["start_date"] = start_date
        plan_to_save["service_type"] = service_type
        plan_to_save["cooking_days"] = ",".join(cooking_days)
        plan_to_save["cooking_time"] = cooking_time
        plan_to_save["submitted_at"] = datetime.now().isoformat()

        file_exists = os.path.exists("submitted_plans.csv")

        plan_to_save.to_csv(
            "submitted_plans.csv",
            mode="a",
            index=False,
            header=not file_exists
        )

        st.session_state.submitted = True

# -----------------------------
# Confirmation message (PERSISTS)
# -----------------------------
if st.session_state.submitted:
    st.success("✅ Your plan has been submitted to the chef.")
    st.info(
        "You’ll receive a confirmation once the chef reviews availability."
    )

# -----------------------------
# Debug section
# -----------------------------
with st.expander("See available meals"):
    st.dataframe(meals_df, use_container_width=True)
