
import streamlit as st
import pandas as pd

# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="FoodFlow | Smart Grocery Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    div[data-testid="stMetric"] {
        background: #172033;
        border: 1px solid #29364d;
        padding: 18px;
        border-radius: 12px;
    }

    div[data-testid="stMetricLabel"] {
        color: #94A3B8;
    }

    div[data-testid="stMetricValue"] {
        color: #38BDF8;
    }

    .hero {
        background: linear-gradient(120deg, #172033, #1e3a5f);
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }

    .hero h1 {
        color: #F8FAFC;
        font-size: 42px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #CBD5E1;
        font-size: 17px;
    }

    .section-title {
        color: #38BDF8;
        font-size: 22px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    customer_df = pd.read_csv(
        "data/customer_recommendations.csv",
        escapechar="\\",
        engine="python"
    )

    product_df = pd.read_csv(
        "data/top_product_insights.csv",
        escapechar="\\",
        engine="python"
    )

    department_df = pd.read_csv(
        "data/department_insights.csv",
        escapechar="\\",
        engine="python"
    )

    # Clean data types
    customer_df["user_id"] = pd.to_numeric(
        customer_df["user_id"], errors="coerce"
    )
    customer_df["rank"] = pd.to_numeric(
        customer_df["rank"], errors="coerce"
    )
    customer_df["product_id"] = pd.to_numeric(
        customer_df["product_id"], errors="coerce"
    )
    customer_df["reorder_probability"] = pd.to_numeric(
        customer_df["reorder_probability"], errors="coerce"
    )

    product_df["recommendation_count"] = pd.to_numeric(
        product_df["recommendation_count"], errors="coerce"
    )
    product_df["avg_probability"] = pd.to_numeric(
        product_df["avg_probability"], errors="coerce"
    )

    department_df["total_recommendations"] = pd.to_numeric(
        department_df["total_recommendations"], errors="coerce"
    )
    department_df["customers_reached"] = pd.to_numeric(
        department_df["customers_reached"], errors="coerce"
    )
    department_df["avg_reorder_probability"] = pd.to_numeric(
        department_df["avg_reorder_probability"], errors="coerce"
    )

    return customer_df, product_df, department_df


try:
    customer_df, product_df, department_df = load_data()

except Exception as e:
    st.error(f"Dataset loading failed: {e}")
    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("# 🛒 FoodFlow")
st.sidebar.caption("SMART GROCERY ANALYTICS")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Home",
        "Customer Recommendations",
        "Product Intelligence",
        "Department Insights",
        "Action Centre",
        "Model Performance"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### Project Information")
st.sidebar.caption("Big Data Analytics")
st.sidebar.caption("Predictive Analytics")
st.sidebar.caption("Machine Learning")

st.sidebar.divider()
st.sidebar.caption("FoodFlow | Decision Support System")


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def format_probability(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:.2%}"


# =========================================================
# HOME
# =========================================================

if page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>🛒 FoodFlow</h1>
        <p>Turning grocery purchase data into intelligent decisions.</p>
        <p>Large-Scale Grocery Demand Analytics & Predictive Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Platform Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Purchase Records",
        "32.43 Million"
    )

    col2.metric(
        "Candidate Coverage",
        "68.31%"
    )

    col3.metric(
        "Validation PR-AUC",
        "0.3116"
    )

    col4.metric(
        "Recommendation Model",
        "Logistic Regression"
    )

    st.divider()

    st.markdown("## Explore FoodFlow")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👤 Customer Intelligence")
        st.write(
            "Discover personalized product recommendations "
            "for individual customers."
        )

        st.markdown("### 📦 Product Intelligence")
        st.write(
            "Explore product popularity, recommendation frequency "
            "and predicted reorder probabilities."
        )

    with col2:
        st.markdown("### 🏢 Department Analytics")
        st.write(
            "Compare grocery departments using recommendation "
            "volume and customer reach."
        )

        st.markdown("### 💡 Business Action Centre")
        st.write(
            "Translate analytical findings into indicative "
            "business recommendations."
        )

    st.divider()

    st.markdown("## Predictive Analytics Snapshot")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top 5 Recommended Products")

        top_products = product_df.nlargest(
            5, "recommendation_count"
        )

        st.bar_chart(
            top_products.set_index("product_name")[
                "recommendation_count"
            ],
            horizontal=True
        )

    with col2:
        st.markdown("#### Department Recommendation Volume")

        top_departments = department_df.nlargest(
            7, "total_recommendations"
        )

        st.bar_chart(
            top_departments.set_index("department")[
                "total_recommendations"
            ],
            horizontal=True
        )

    st.info(
        "FoodFlow uses precomputed predictions from historical grocery "
        "transactions. It is a decision-support prototype, not a live "
        "inventory or streaming system."
    )


# =========================================================
# CUSTOMER RECOMMENDATIONS
# =========================================================

elif page == "Customer Recommendations":

    st.title("👤 Customer Recommendations")
    st.write("Explore personalized product recommendations.")

    st.divider()

    customer_ids = sorted(
        customer_df["user_id"].dropna().unique().tolist()
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_customer = st.selectbox(
            "Select Customer ID",
            customer_ids
        )

    with col2:
        top_n = st.selectbox(
            "Number of Recommendations",
            [5, 10],
            index=1
        )

    # Customer filter
    customer_data = customer_df[
        customer_df["user_id"] == selected_customer
    ].copy()

    # Additional interactive controls
    col1, col2 = st.columns(2)

    with col1:
        min_probability = st.slider(
            "Minimum Predicted Probability",
            min_value=0,
            max_value=100,
            value=0,
            step=5
        )

    with col2:
        sort_option = st.selectbox(
            "Sort Recommendations",
            [
                "Highest Probability",
                "Lowest Probability",
                "Original Rank"
            ]
        )

    customer_data = customer_data[
        customer_data["reorder_probability"]
        >= min_probability / 100
    ]

    if sort_option == "Highest Probability":
        customer_data = customer_data.sort_values(
            "reorder_probability", ascending=False
        )

    elif sort_option == "Lowest Probability":
        customer_data = customer_data.sort_values(
            "reorder_probability", ascending=True
        )

    else:
        customer_data = customer_data.sort_values("rank")

    customer_data = customer_data.head(top_n)

    st.divider()

    # Dynamic KPIs
    total = len(customer_data)

    average = customer_data[
        "reorder_probability"
    ].mean()

    highest = customer_data[
        "reorder_probability"
    ].max()

    col1, col2, col3 = st.columns(3)

    col1.metric("Products Displayed", total)
    col2.metric("Average Probability", format_probability(average))
    col3.metric("Highest Probability", format_probability(highest))

    st.divider()

    st.markdown(
        f"### Top Recommendations for Customer {int(selected_customer)}"
    )

    if customer_data.empty:

        st.warning(
            "No recommendations match the selected probability filter."
        )

    else:

        display_data = customer_data[
            ["rank", "product_name", "reorder_probability"]
        ].copy()

        display_data["reorder_probability"] = (
            display_data["reorder_probability"] * 100
        ).round(2)

        display_data = display_data.rename(columns={
            "rank": "Rank",
            "product_name": "Product",
            "reorder_probability": "Predicted Probability (%)"
        })

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Recommendation Probability")

        chart_data = customer_data.set_index(
            "product_name"
        )["reorder_probability"]

        st.bar_chart(
            chart_data,
            horizontal=True
        )

    st.caption(
        "Predicted probabilities are model estimates, not guaranteed "
        "future purchases."
    )


# =========================================================
# PRODUCT INTELLIGENCE
# =========================================================

elif page == "Product Intelligence":

    st.title("📦 Product Intelligence")
    st.write("Explore product-level recommendation patterns.")

    st.divider()

    # Product search
    search_text = st.text_input(
        "🔍 Search for a product",
        placeholder="Enter a product name..."
    )

    filtered_products = product_df.copy()

    if search_text:
        filtered_products = filtered_products[
            filtered_products["product_name"]
            .str.contains(search_text, case=False, na=False)
        ]

    col1, col2 = st.columns(2)

    with col1:
        top_n = st.selectbox(
            "Display Top Products",
            [5, 10, 20, 50],
            index=2
        )

    with col2:
        minimum_count = st.number_input(
            "Minimum Recommendation Count",
            min_value=0,
            value=0,
            step=100
        )

    filtered_products = filtered_products[
        filtered_products["recommendation_count"] >= minimum_count
    ]

    filtered_products = filtered_products.nlargest(
        top_n,
        "recommendation_count"
    )

    st.divider()

    # KPIs
    if not filtered_products.empty:

        total = int(
            filtered_products["recommendation_count"].sum()
        )

        leading_product = filtered_products.iloc[0]["product_name"]

        average_probability = filtered_products[
            "avg_probability"
        ].mean()

        col1, col2, col3 = st.columns(3)

        col1.metric("Recommendations in Selection", f"{total:,}")
        col2.metric("Leading Product", leading_product)
        col3.metric(
            "Average Predicted Probability",
            format_probability(average_probability)
        )

        st.divider()

        st.markdown("### Product Recommendation Ranking")

        st.bar_chart(
            filtered_products.set_index("product_name")[
                "recommendation_count"
            ],
            horizontal=True
        )

        st.markdown("### Product Performance Table")

        display_products = filtered_products[
            [
                "product_name",
                "recommendation_count",
                "avg_probability"
            ]
        ].copy()

        display_products["avg_probability"] = (
            display_products["avg_probability"] * 100
        ).round(2)

        display_products = display_products.rename(columns={
            "product_name": "Product",
            "recommendation_count": "Recommendation Count",
            "avg_probability": "Average Probability (%)"
        })

        st.dataframe(
            display_products,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Frequency vs Probability")

        st.scatter_chart(
            filtered_products,
            x="recommendation_count",
            y="avg_probability",
            x_label="Recommendation Count",
            y_label="Average Predicted Probability"
        )

    else:

        st.warning("No products match your filters.")


# =========================================================
# DEPARTMENT INSIGHTS
# =========================================================

elif page == "Department Insights":

    st.title("🏢 Department Insights")
    st.write("Explore grocery department recommendation patterns.")

    st.divider()

    departments = sorted(
        department_df["department"].dropna().unique().tolist()
    )

    selected_department = st.selectbox(
        "Select Department",
        ["All Departments"] + departments
    )

    if selected_department == "All Departments":
        selected_data = department_df.copy()
    else:
        selected_data = department_df[
            department_df["department"] == selected_department
        ].copy()

    st.divider()

    if not selected_data.empty:

        total_recommendations = int(
            selected_data["total_recommendations"].sum()
        )

        total_customer_reach = int(
            selected_data["customers_reached"].sum()
        )

        avg_probability = (
            selected_data["avg_reorder_probability"].mean()
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Recommendation Volume",
            f"{total_recommendations:,}"
        )

        col2.metric(
            "Cumulative Customer Reach",
            f"{total_customer_reach:,}"
        )

        col3.metric(
            "Average Predicted Probability",
            format_probability(avg_probability)
        )

        st.caption(
            "Cumulative customer reach may count the same customer "
            "in multiple departments."
        )

        st.divider()

        st.markdown("### Department Recommendation Comparison")

        if selected_department == "All Departments":

            chart_data = selected_data.sort_values(
                "total_recommendations",
                ascending=False
            )

            st.bar_chart(
                chart_data.set_index("department")[
                    "total_recommendations"
                ],
                horizontal=True
            )

        else:

            st.metric(
                f"{selected_department.title()} Recommendations",
                f"{total_recommendations:,}"
            )

        st.divider()

        st.markdown("### Department Performance Details")

        display_data = selected_data.copy()

        display_data["avg_reorder_probability"] = (
            display_data["avg_reorder_probability"] * 100
        ).round(2)

        display_data = display_data.rename(columns={
            "department": "Department",
            "total_recommendations": "Total Recommendations",
            "customers_reached": "Customers Reached",
            "avg_reorder_probability": "Average Probability (%)"
        })

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )

        if selected_department == "All Departments":

            st.markdown("### Average Probability by Department")

            st.bar_chart(
                chart_data.set_index("department")[
                    "avg_reorder_probability"
                ],
                horizontal=True
            )


# =========================================================
# ACTION CENTRE
# =========================================================

elif page == "Action Centre":

    st.title("💡 FoodFlow Action Centre")

    st.write(
        "Explore indicative business suggestions based on "
        "the predictive analytics results."
    )

    st.divider()

    suggestion_type = st.radio(
        "Choose an insight category",
        [
            "Department Analysis",
            "Product Analysis"
        ],
        horizontal=True
    )

    if suggestion_type == "Department Analysis":

        department_names = sorted(
            department_df["department"].dropna().unique().tolist()
        )

        selected_department = st.selectbox(
            "Choose a Department",
            department_names
        )

        row = department_df[
            department_df["department"] == selected_department
        ].iloc[0]

        st.markdown("### Department Performance")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Recommendations",
            f"{int(row['total_recommendations']):,}"
        )

        col2.metric(
            "Customers Reached",
            f"{int(row['customers_reached']):,}"
        )

        col3.metric(
            "Average Probability",
            format_probability(row["avg_reorder_probability"])
        )

        st.divider()

        if row["total_recommendations"] == department_df[
            "total_recommendations"
        ].max():

            st.success(
                "This is the department with the highest recommendation volume."
            )

            st.markdown("""
            **Suggested action:**

            Consider reviewing product availability and merchandising
            priorities in this department.
            """)

        if row["avg_reorder_probability"] == department_df[
            "avg_reorder_probability"
        ].max():

            st.success(
                "This department has the highest average predicted probability."
            )

            st.markdown("""
            **Suggested action:**

            Investigate whether targeted promotions or personalized
            product placements could be useful.
            """)

        st.info(
            "These suggestions are indicative. The dataset does not "
            "contain inventory, pricing or supplier information."
        )

    else:

        product_names = sorted(
            product_df["product_name"].dropna().unique().tolist()
        )

        selected_product = st.selectbox(
            "Choose a Product",
            product_names
        )

        row = product_df[
            product_df["product_name"] == selected_product
        ].iloc[0]

        st.markdown("### Product Performance")

        col1, col2 = st.columns(2)

        col1.metric(
            "Recommendation Count",
            f"{int(row['recommendation_count']):,}"
        )

        col2.metric(
            "Average Predicted Probability",
            format_probability(row["avg_probability"])
        )

        st.divider()

        if row["recommendation_count"] == product_df[
            "recommendation_count"
        ].max():

            st.success(
                "This is the most frequently recommended product."
            )

            st.markdown("""
            **Suggested action:**

            Consider monitoring product availability and placement
            in relevant product categories.
            """)

        if row["avg_probability"] == product_df[
            "avg_probability"
        ].max():

            st.success(
                "This product has the highest average predicted probability."
            )

        st.markdown("""
        **Suggested action:**

        Investigate this product's historical reorder patterns and
        consider personalized recommendation strategies.
        """)

    st.divider()

    st.caption(
        "FoodFlow business suggestions are rule-based interpretations "
        "of historical recommendation data and model scores. They are "
        "not proven causal effects or operational inventory decisions."
    )
    
# =========================================================
# MODEL PERFORMANCE
# =========================================================

elif page == "Model Performance":

    st.title("🧠 Model Performance")
    st.write(
        "Evaluate the FoodFlow Logistic Regression model "
        "using validation metrics and recommendation quality."
    )

    st.divider()

    # Model overview
    st.subheader("Model Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Algorithm", "Logistic Regression")
    col2.metric("Feature Vector Size", "164")
    col3.metric("Validation PR-AUC", "0.3116")

    st.divider()

    # Classification metrics
    st.subheader("Classification Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric("Precision", "11.79%")
    col2.metric("Recall", "84.78%")
    col3.metric("F1 Score", "20.70%")

    st.caption(
        "These metrics were obtained at the default classification "
        "threshold of 0.50 on the validation dataset."
    )

    st.divider()

    # Threshold comparison
    st.subheader("Threshold Tuning Analysis")

    threshold_data = pd.DataFrame({
        "Threshold": [0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
        "Precision": [0.1018, 0.1072, 0.1179, 0.1394, 0.1801, 0.2542],
        "Recall": [0.8739, 0.8670, 0.8478, 0.7992, 0.6982, 0.5361],
        "F1 Score": [0.1824, 0.1908, 0.2070, 0.2374, 0.2864, 0.3448]
    })

    selected_threshold = st.selectbox(
        "Select Classification Threshold",
        [0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
        index=5
    )

    selected_metrics = threshold_data[
        threshold_data["Threshold"] == selected_threshold
    ].iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Precision",
        f"{selected_metrics['Precision']:.2%}"
    )

    col2.metric(
        "Recall",
        f"{selected_metrics['Recall']:.2%}"
    )

    col3.metric(
        "F1 Score",
        f"{selected_metrics['F1 Score']:.2%}"
    )

    st.markdown("### Threshold Comparison")

    st.dataframe(
        threshold_data.style.format({
            "Threshold": "{:.1f}",
            "Precision": "{:.2%}",
            "Recall": "{:.2%}",
            "F1 Score": "{:.2%}"
        }),
        use_container_width=True,
        hide_index=True
    )

    chart_data = threshold_data.set_index("Threshold")[
        ["Precision", "Recall", "F1 Score"]
    ]

    st.line_chart(chart_data)

    st.info(
        "Among the tested thresholds, 0.80 produced the highest F1 score. "
        "It increased precision while reducing recall compared with 0.50. "
        "This threshold was selected using validation results."
    )

    st.divider()

    # Confusion matrix
    st.subheader("Confusion Matrix")

    confusion_matrix = pd.DataFrame(
        [
            [5156847, 1206341],
            [28944, 161265]
        ],
        index=["Actual Negative", "Actual Positive"],
        columns=["Predicted Negative", "Predicted Positive"]
    )

    st.dataframe(
        confusion_matrix,
        use_container_width=True
    )

    st.caption(
        "Validation results at threshold 0.50. "
        "Rows represent actual classes and columns represent predictions."
    )

    st.divider()

    # Top-K recommendation performance
    st.subheader("Top-10 Recommendation Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric("Mean Precision@10", "23.64%")
    col2.metric("Mean Recall@10", "27.87%")
    col3.metric("Overall Recall@10", "25.52%")

    st.markdown("""
    **Interpretation:**

    - Mean Precision@10 measures the average proportion of relevant
      products among the ten recommendations for each customer.
    - Mean Recall@10 measures the average proportion of a customer's
      actual next-order products captured in the recommendations.
    - Overall Recall@10 measures the pooled proportion of actual
      next-order products captured across all validation customers.
    """)

    st.divider()

    # Class imbalance
    st.subheader("Class Imbalance Analysis")

    imbalance_data = pd.DataFrame({
        "Class": ["Positive", "Negative"],
        "Percentage": [2.89, 97.11]
    })

    st.bar_chart(
        imbalance_data.set_index("Class")
    )

    st.caption(
        "The dataset is highly imbalanced. Therefore, accuracy alone "
        "would be misleading. Precision, recall, F1 and PR-AUC provide "
        "more useful evaluation perspectives."
    )

    st.divider()

    # Final interpretation
    st.subheader("Model Evaluation Summary")

    st.success(
        "The model achieved 84.78% recall at threshold 0.50. "
        "Threshold 0.80 achieved a higher F1 score of 34.48%, "
        "with a precision of 25.42%."
    )

    st.warning(
        "The threshold comparison was performed on validation data. "
        "The selected threshold is provisional and should ideally be "
        "confirmed on an independent labelled test dataset. "
        "The official Instacart test split does not contain labels."
    )



# =========================================================
# FOOTER
# =========================================================

st.sidebar.divider()
st.sidebar.caption("© FoodFlow | Big Data Analytics Project")
