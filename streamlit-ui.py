import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta




# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="HCCDA AI Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.dashboard-title {
    font-size: 32px;
    font-weight: 700;
}

.dashboard-subtitle {
    color: #888;
    margin-bottom: 25px;
}

.activity-box {
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #ddd;
    margin-bottom: 8px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SAMPLE DATA
# =========================================================

@st.cache_data
def load_data():

    np.random.seed(42)

    total_students = 200

    names = [
        f"Student {i}"
        for i in range(1, total_students + 1)
    ]

    courses = np.random.choice(
        [
            "Python",
            "Artificial Intelligence",
            "Machine Learning",
            "Deep Learning"
        ],
        total_students
    )

    cities = np.random.choice(
        [
            "Lahore",
            "Karachi",
            "Islamabad",
            "Faisalabad",
            "Multan"
        ],
        total_students
    )

    scores = np.random.randint(
        40,
        100,
        total_students
    )

    attendance = np.random.randint(
        50,
        101,
        total_students
    )

    study_hours = np.random.randint(
        1,
        10,
        total_students
    )

    dates = [
        datetime.today()
        - timedelta(
            days=np.random.randint(0, 90)
        )
        for _ in range(total_students)
    ]

    status = np.where(
        scores >= 50,
        "Pass",
        "Fail"
    )

    data = pd.DataFrame({
        "Name": names,
        "Course": courses,
        "City": cities,
        "Score": scores,
        "Attendance": attendance,
        "Study Hours": study_hours,
        "Status": status,
        "Registration Date": dates
    })

    return data


df = load_data()


# =========================================================
# SESSION STATE
# =========================================================

if "activities" not in st.session_state:

    st.session_state.activities = [
        "Dashboard started",
        "Student dataset loaded",
        "AI analytics initialized"
    ]


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🤖 HCCDA AI")

st.sidebar.caption(
    "Artificial Intelligence Learning Dashboard"
)

st.sidebar.divider()


page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Students",
        "AI Prediction",
        "Analytics",
        "Activity",
        "About"
    ]
)


st.sidebar.divider()


# =========================================================
# GLOBAL FILTERS / SLICERS
# =========================================================

st.sidebar.subheader("Filters")


selected_course = st.sidebar.multiselect(
    "Course",
    options=df["Course"].unique(),
    default=df["Course"].unique()
)


selected_city = st.sidebar.multiselect(
    "City",
    options=df["City"].unique(),
    default=df["City"].unique()
)


score_range = st.sidebar.slider(
    "Score Range",
    min_value=int(df["Score"].min()),
    max_value=int(df["Score"].max()),
    value=(
        int(df["Score"].min()),
        int(df["Score"].max())
    )
)


attendance_range = st.sidebar.slider(
    "Attendance %",
    min_value=0,
    max_value=100,
    value=(50, 100)
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    (df["Course"].isin(selected_course))
    &
    (df["City"].isin(selected_city))
    &
    (
        df["Score"].between(
            score_range[0],
            score_range[1]
        )
    )
    &
    (
        df["Attendance"].between(
            attendance_range[0],
            attendance_range[1]
        )
    )
]


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.markdown(
        '<div class="dashboard-title">'
        'HCCDA AI Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Student performance and AI learning analytics'
        '</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    total_students = len(filtered_df)

    average_score = (
        filtered_df["Score"].mean()
        if total_students > 0
        else 0
    )

    average_attendance = (
        filtered_df["Attendance"].mean()
        if total_students > 0
        else 0
    )

    pass_rate = (
        (
            filtered_df["Status"] == "Pass"
        ).mean() * 100
        if total_students > 0
        else 0
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Students",
            total_students
        )


    with col2:

        st.metric(
            "Average Score",
            f"{average_score:.1f}"
        )


    with col3:

        st.metric(
            "Attendance",
            f"{average_attendance:.1f}%"
        )


    with col4:

        st.metric(
            "Pass Rate",
            f"{pass_rate:.1f}%"
        )


    st.divider()


    # -----------------------------------------------------
    # CHART ROW
    # -----------------------------------------------------

    chart_col1, chart_col2 = st.columns(2)


    # BAR CHART
    with chart_col1:

        st.subheader("Students by Course")

        course_data = (
            filtered_df["Course"]
            .value_counts()
            .reset_index()
        )

        course_data.columns = [
            "Course",
            "Students"
        ]

        fig_course = px.bar(
            course_data,
            x="Course",
            y="Students",
            title="Course Distribution"
        )

        st.plotly_chart(
            fig_course,
            use_container_width=True
        )


    # PIE CHART
    with chart_col2:

        st.subheader("Students by City")

        city_data = (
            filtered_df["City"]
            .value_counts()
            .reset_index()
        )

        city_data.columns = [
            "City",
            "Students"
        ]

        fig_city = px.pie(
            city_data,
            names="City",
            values="Students",
            hole=0.4
        )

        st.plotly_chart(
            fig_city,
            use_container_width=True
        )


    # -----------------------------------------------------
    # SECOND CHART ROW
    # -----------------------------------------------------

    chart_col3, chart_col4 = st.columns(2)


    # HISTOGRAM
    with chart_col3:

        st.subheader("Score Distribution")

        fig_score = px.histogram(
            filtered_df,
            x="Score",
            nbins=15
        )

        st.plotly_chart(
            fig_score,
            use_container_width=True
        )


    # SCATTER CHART
    with chart_col4:

        st.subheader(
            "Study Hours vs Score"
        )

        fig_scatter = px.scatter(
            filtered_df,
            x="Study Hours",
            y="Score",
            color="Course",
            size="Attendance",
            hover_data=["Name"]
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )


    # -----------------------------------------------------
    # TABLE
    # -----------------------------------------------------

    st.subheader("Student Records")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# STUDENTS PAGE
# =========================================================

elif page == "Students":

    st.title("👨‍🎓 Student Management")


    tab1, tab2 = st.tabs(
        [
            "Student List",
            "Add Student"
        ]
    )


    # -----------------------------------------------------
    # STUDENT LIST
    # -----------------------------------------------------

    with tab1:

        search = st.text_input(
            "Search Student"
        )


        student_data = filtered_df.copy()


        if search:

            student_data = student_data[
                student_data["Name"]
                .str.contains(
                    search,
                    case=False
                )
            ]


        st.write(
            f"Records found: {len(student_data)}"
        )


        st.dataframe(
            student_data,
            use_container_width=True,
            hide_index=True
        )


        # CSV DOWNLOAD

        csv = student_data.to_csv(
            index=False
        )


        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="students.csv",
            mime="text/csv"
        )


    # -----------------------------------------------------
    # ADD STUDENT
    # -----------------------------------------------------

    with tab2:

        st.subheader(
            "Register New Student"
        )


        with st.form(
            "student_registration"
        ):

            name = st.text_input(
                "Student Name"
            )


            course = st.selectbox(
                "Course",
                [
                    "Python",
                    "Artificial Intelligence",
                    "Machine Learning",
                    "Deep Learning"
                ]
            )


            city = st.selectbox(
                "City",
                [
                    "Lahore",
                    "Karachi",
                    "Islamabad",
                    "Faisalabad",
                    "Multan"
                ]
            )


            score = st.slider(
                "Score",
                0,
                100,
                50
            )


            attendance = st.slider(
                "Attendance",
                0,
                100,
                80
            )


            submit = (
                st.form_submit_button(
                    "Register Student"
                )
            )


        if submit:

            if name.strip():

                st.success(
                    f"{name} registered successfully"
                )

                st.session_state.activities.insert(
                    0,
                    f"New student registered: {name}"
                )

            else:

                st.warning(
                    "Please enter student name."
                )


# =========================================================
# AI PREDICTION
# =========================================================

elif page == "AI Prediction":

    st.title("🧠 AI Prediction")

    st.write(
        "Predict student performance based on study behaviour."
    )


    col1, col2 = st.columns(2)


    with col1:

        study_hours = st.slider(
            "Study Hours Per Day",
            0.0,
            12.0,
            4.0,
            0.5
        )


    with col2:

        attendance = st.slider(
            "Attendance %",
            0,
            100,
            80
        )


    assignment_score = st.slider(
        "Assignment Score",
        0,
        100,
        70
    )


    if st.button(
        "Run Prediction",
        type="primary"
    ):

        predicted_score = (
            study_hours * 4
            +
            attendance * 0.35
            +
            assignment_score * 0.30
        )


        predicted_score = min(
            predicted_score,
            100
        )


        st.subheader(
            "Prediction Result"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Predicted Score",
                f"{predicted_score:.1f}%"
            )


        with col2:

            if predicted_score >= 50:

                st.success(
                    "Likely to PASS"
                )

            else:

                st.error(
                    "Risk of FAIL"
                )


        st.progress(
            int(predicted_score)
        )


        st.session_state.activities.insert(
            0,
            "AI student prediction executed"
        )


# =========================================================
# ANALYTICS PAGE
# =========================================================

elif page == "Analytics":

    st.title("📊 Advanced Analytics")


    tab1, tab2, tab3 = st.tabs(
        [
            "Performance",
            "Attendance",
            "Courses"
        ]
    )


    # -----------------------------------------------------
    # PERFORMANCE
    # -----------------------------------------------------

    with tab1:

        performance = (
            filtered_df
            .groupby("Course")["Score"]
            .mean()
            .reset_index()
        )


        fig = px.bar(
            performance,
            x="Course",
            y="Score",
            title="Average Score by Course"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # -----------------------------------------------------
    # ATTENDANCE
    # -----------------------------------------------------

    with tab2:

        attendance_data = (
            filtered_df
            .groupby("Course")[
                "Attendance"
            ]
            .mean()
            .reset_index()
        )


        fig = px.line(
            attendance_data,
            x="Course",
            y="Attendance",
            markers=True
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # -----------------------------------------------------
    # COURSE
    # -----------------------------------------------------

    with tab3:

        course_status = (
            filtered_df
            .groupby(
                [
                    "Course",
                    "Status"
                ]
            )
            .size()
            .reset_index(
                name="Students"
            )
        )


        fig = px.bar(
            course_status,
            x="Course",
            y="Students",
            color="Status",
            barmode="group"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# ACTIVITY PAGE
# =========================================================

elif page == "Activity":

    st.title("🔔 Recent Activity")


    if st.button(
        "Clear Activity"
    ):

        st.session_state.activities = []


    if not st.session_state.activities:

        st.info(
            "No recent activities."
        )


    for activity in (
        st.session_state.activities
    ):

        st.markdown(
            f"""
            <div class="activity-box">
                🔹 {activity}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# ABOUT
# =========================================================

elif page == "About":

    st.title("ℹ️ About Application")


    st.write("""
    ### HCCDA AI Learning Dashboard

    This application demonstrates:

    - Python
    - Streamlit
    - Pandas
    - NumPy
    - Plotly
    - Data Analysis
    - Interactive Filters
    - AI Prediction
    - Dashboard Development
    """)


    st.info(
        "Developed as part of HCCDA AI learning."
    )