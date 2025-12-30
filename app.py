import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Meal Prep AI Assistant",
    layout="centered"
)

st.title("🥗 First Course AI Assistant")
st.caption("Weekly meal planning for busy professionals & families")

@st.cache_data
def load_meals():
    return pd.read_csv("meals.csv")

meals_df = load_meals()

st.divider()
st.subheader("Tell us about your preferences")

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
        options=["Any", "Under $13", "$13–$15", "$15+"]
    )

    submitted = st.form_submit_button("Generate my weekly plan")
    if submitted:
        filtered = filter_meals(
            meals_df,
            diet_type,
            calorie_range,
            dislikes
        )

        st.divider()
        st.subheader("Your Weekly Meal Plan")

        if filtered.empty:
            st.warning("No meals match your preferences. Try adjusting filters.")
        else:
            scored = score_meals(filtered)
            weekly_plan = generate_weekly_plan(scored, meals_per_week)

            st.write(
                f"Here’s a {meals_per_week}-meal plan optimized for higher protein."
            )

            st.dataframe(
                weekly_plan[
                    [
                        "meal_name",
                        "calories",
                        "protein_g",
                        "diet_type",
                        "price_estimate",
                    ]
                ],
                use_container_width=True
            )

st.divider()
st.subheader("Available Meals")

st.dataframe(
    meals_df,
    use_container_width=True
)
