import streamlit as st
import pandas as pd
from datetime import date, datetime
import os


st.markdown(
    """
    <style>
    /* Global app background and text */
    .stApp {
        background-color: #FAFAF8;
    }

    * {
        color: #1F2933 !important;
    }

    h1, h2, h3 {
        color: #4F6F52 !important;
    }

    /* Basic inputs (text, textarea, native select) */
    input, textarea, select {
        background-color: #FFFFFF !important;
        color: #1F2933 !important;
        caret-color: #1F2933 !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #6B7280 !important;
        opacity: 1 !important;
    }

    label {
        color: #374151 !important;
        font-weight: 500;
    }

    button {
        background-color: #6B8E6E !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        border: none !important;
    }

    button:hover {
        background-color: #4F6F52 !important;
    }

    /* === DROPDOWNS: selectbox + multiselect (control + options list) === */

    /* Main closed control for selectbox/multiselect */
    [data-testid="stSelectbox"] > div:first-child,
    [data-testid="stMultiselect"] > div:first-child {
        background: #FFFFFF !important;
        color: #111827 !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
        min-height: 40px !important;
        padding: 6px 10px !important;
        box-shadow: none !important;
    }

    /* Text and icons inside control */
    [data-testid="stSelectbox"] [role="combobox"],
    [data-testid="stMultiselect"] [role="combobox"],
    [data-testid="stSelectbox"] svg,
    [data-testid="stMultiselect"] svg {
        background: transparent !important;
        color: #111827 !important;
        fill: #111827 !important;
    }

    /* Dropdown popover and options list */
    [data-baseweb="popover"],
    [role="listbox"] {
        background: #FFFFFF !important;
        color: #111827 !important;
        box-shadow: 0 6px 18px rgba(15,23,42,0.08) !important;
    }

    /* Individual options: light background + dark text */
    [role="option"] {
        background: #FFFFFF !important;
        color: #111827 !important;
    }

    [role="option"]:hover,
    [role="option"][aria-selected="true"] {
        background: #F3F4F6 !important;
        color: #111827 !important;
    }

    /* Multiselect chips inside control */
    [data-testid="stMultiselect"] span[data-baseweb="tag"] {
        background: #F87171 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        padding: 4px 8px !important;
        box-shadow: none !important;
        margin-right: 4px !important;
    }

    /* === FILE UPLOADER: light background + dark text === */

    /* Whole uploader block */
    [data-testid="stFileUploader"] {
        background: #FFFFFF !important;
        color: #111827 !important;
    }

    /* Dropzone surface */
    [data-testid="stFileUploaderDropzone"] {
        background: #FFFFFF !important;
        color: #111827 !important;
        border: 1px dashed #D1D5DB !important;
        border-radius: 10px !important;
    }

    /* Dropzone text */
    [data-testid="stFileUploaderDropzone"] * {
        background: transparent !important;
        color: #111827 !important;
    }

    /* Uploaded file rows */
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] {
        background: #FFFFFF !important;
        color: #111827 !important;
        border-radius: 8px !important;
    }

    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] * {
        background: transparent !important;
        color: #111827 !important;
    }

    /* Keep remove/clear buttons readable */
    [data-testid="stFileUploader"] button {
        background-color: #6B8E6E !important;
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <style>
    /* === FORCE ALL DROPDOWN CONTROLS + OPTION LISTS LIGHT === */

    /* Closed controls: selectbox, multiselect, date, etc. */
    [data-testid="stSelectbox"] * ,
    [data-testid="stMultiselect"] * ,
    [data-testid="stDateInput"] * {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        box-shadow: none !important;
    }

    /* The visible bars for selectbox/multiselect/date */
    [data-testid="stSelectbox"] > div:first-child,
    [data-testid="stMultiselect"] > div:first-child,
    [data-testid="stDateInput"] > div:first-child {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
    }

    /* Any dropdown popover and options */
    [data-baseweb="popover"],
    [data-baseweb="popover"] * ,
    [role="listbox"],
    [role="listbox"] * ,
    [role="option"] {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        box-shadow: none !important;
    }

    [role="option"]:hover,
    [role="option"][aria-selected="true"] {
        background-color: #F3F4F6 !important;
        color: #111827 !important;
    }

    /* === DATEPICKER POPUP (react-datepicker) LIGHT === */

    .react-datepicker,
    .react-datepicker * {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        box-shadow: none !important;
    }

    .react-datepicker__header {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        border-bottom: 1px solid #E5E7EB !important;
    }

    .react-datepicker__day,
    .react-datepicker__day-name {
        background-color: #FFFFFF !important;
        color: #111827 !important;
    }

    .react-datepicker__day:hover {
        background-color: #F3F4F6 !important;
        color: #111827 !important;
    }

    .react-datepicker__day--selected,
    .react-datepicker__day--keyboard-selected,
    .react-datepicker__day--today {
        background-color: #F87171 !important;
        color: #FFFFFF !important;
        border-radius: 90% !important;
    }

    /* === FILE UPLOADER STAYS LIGHT === */

    [data-testid="stFileUploader"],
    [data-testid="stFileUploader"] * {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        box-shadow: none !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        border: 1px dashed #D1D5DB !important;
        border-radius: 90px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)




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
                ~filtered["ingredients"]
                .str.lower()
                .str.contains(item.strip().lower())
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
defaults = {
    "weekly_plan": None,
    "submitted": False,
    "client_name": "",
    "client_email": "",
    "client_phone": "",
    "start_date": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------
# Client info
# -----------------------------
st.subheader("Your details")

st.session_state.client_name = st.text_input(
    "Full name", value=st.session_state.client_name
)
st.session_state.client_email = st.text_input(
    "Email", value=st.session_state.client_email
)
st.session_state.client_phone = st.text_input(
    "Phone number", value=st.session_state.client_phone
)
st.session_state.start_date = st.date_input(
    "Preferred start date",
    min_value=date.today(),
    value=st.session_state.start_date or date.today()
)

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
# Generate plan
# -----------------------------
if generate:
    filtered = filter_meals(meals_df, diet_type, calorie_range, dislikes)

    if filtered.empty:
        st.warning("No meals match your preferences.")
        st.session_state.weekly_plan = None
    else:
        st.session_state.weekly_plan = score_meals(filtered).head(meals_per_week)
        st.session_state.submitted = False

# -----------------------------
# Display plan
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
        submission_time = datetime.now()

        plan_to_save = weekly_plan.copy()
        plan_to_save["client_name"] = st.session_state.client_name
        plan_to_save["client_email"] = st.session_state.client_email
        plan_to_save["client_phone"] = st.session_state.client_phone
        plan_to_save["start_date"] = st.session_state.start_date
        plan_to_save["service_type"] = service_type
        plan_to_save["cooking_days"] = ",".join(cooking_days)
        plan_to_save["cooking_time"] = cooking_time
        plan_to_save["submission_date"] = submission_time.date().isoformat()
        plan_to_save["submitted_at"] = submission_time.isoformat()

        file_exists = os.path.exists("submitted_plans.csv")

        plan_to_save.to_csv(
            "submitted_plans.csv",
            mode="a",
            index=False,
            header=not file_exists
        )

        st.session_state.submitted = True

# -----------------------------
# Confirmation
# -----------------------------
if st.session_state.submitted:
    st.success("✅ Your plan has been submitted to the chef.")
    st.info("You’ll receive confirmation once availability is reviewed.")

# -----------------------------
# Debug
# -----------------------------
with st.expander("See available meals"):
    st.dataframe(meals_df, use_container_width=True)
