import streamlit as st
import pandas as pd

from matcher import ProductMatcher
from pdf_processor import extract_text_from_pdf
from ai_service import (
    extract_product_information,
    explain_recommendation,
    compare_products,
    analyze_data_quality
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="InduX AI",
    page_icon="🏭",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }

    .product-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-bottom: 15px;
        background-color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD PRODUCT MATCHER
# =========================================================

@st.cache_resource
def load_matcher():
    return ProductMatcher()


# =========================================================
# LOAD PRODUCT DATA
# =========================================================

@st.cache_data
def load_products():

    return pd.read_csv(
        "data/processed_products.csv"
    )


# =========================================================
# INITIALIZE
# =========================================================

try:

    matcher = load_matcher()

    products = load_products()

except Exception as e:

    st.error(
        "Unable to load InduX AI data."
    )

    st.code(str(e))

    st.stop()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🏭 InduX AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'From fragmented product data to intelligent industrial decisions.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🏭 InduX AI")

st.sidebar.write(
    "Industrial Product Intelligence"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🔎 AI Product Finder",
        "📄 Datasheet Intelligence",
        "📊 Product Comparison",
        "🛡️ Data Quality"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Hackathon Prototype"
)

st.sidebar.caption(
    f"{len(products):,} products loaded"
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.header("🏠 Dashboard")

    st.success(
        "InduX AI Product Intelligence Engine is ready."
    )

    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Products Loaded",
            f"{len(products):,}"
        )

    with col2:

        categories = (
            products["category"]
            .dropna()
            .nunique()
        )

        st.metric(
            "Categories",
            f"{categories:,}"
        )

    with col3:

        products_with_description = (
            products["about"]
            .fillna("")
            .astype(str)
            .str.strip()
            .ne("")
            .sum()
        )

        st.metric(
            "Products with Information",
            f"{products_with_description:,}"
        )

    with col4:

        st.metric(
            "AI Search",
            "Ready"
        )

    st.divider()

    # -----------------------------------------------------
    # Pipeline
    # -----------------------------------------------------

    st.subheader(
        "🔄 InduX AI Intelligence Pipeline"
    )

    st.info(
        """
        Raw Product Data
                ↓
        Data Cleaning
                ↓
        Structured Product Information
                ↓
        Semantic Product Search
                ↓
        Requirement Matching
                ↓
        Explainable Recommendation
                ↓
        Product Comparison
        """
    )

    # -----------------------------------------------------
    # Dataset preview
    # -----------------------------------------------------

    st.subheader(
        "📦 Product Dataset"
    )

    display_columns = [
        "product_name",
        "brand",
        "category",
        "model",
        "price"
    ]

    available_columns = [
        column
        for column in display_columns
        if column in products.columns
    ]

    st.dataframe(
        products[
            available_columns
        ].head(10),
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# AI PRODUCT FINDER
# =========================================================

elif page == "🔎 AI Product Finder":

    st.header(
        "🔎 AI Product Finder"
    )

    st.write(
        "Describe what you need using normal language."
    )

    requirement = st.text_area(
        "Product Requirement",
        placeholder=(
            "Example: stainless steel industrial tool"
        ),
        height=120
    )

    search_button = st.button(
        "🔍 Find Matching Products",
        type="primary"
    )

    if search_button:

        if not requirement.strip():

            st.warning(
                "Please enter a product requirement."
            )

        else:

            with st.spinner(
                "AI is analyzing your requirement..."
            ):

                try:

                    # IMPORTANT:
                    # Uses your existing ProductMatcher
                    # instead of match_products()

                    results = matcher.search(
                        requirement,
                        top_k=5
                    )

                except Exception as e:

                    st.error(
                        "Product matching failed."
                    )

                    st.code(str(e))

                    results = []

            if results:

                st.success(
                    f"Found {len(results)} matching products."
                )

                st.subheader(
                    "🏆 Top Matching Products"
                )

                # Save results for comparison
                st.session_state[
                    "search_results"
                ] = results

                for index, product in enumerate(
                    results,
                    start=1
                ):

                    st.markdown(
                        '<div class="product-card">',
                        unsafe_allow_html=True
                    )

                    # -------------------------------------------------
                    # Product information
                    # -------------------------------------------------

                    product_name = str(
                        product.get(
                            "product_name",
                            "Unknown Product"
                        )
                    )

                    category = str(
                        product.get(
                            "category",
                            ""
                        )
                    )

                    brand = str(
                        product.get(
                            "brand",
                            ""
                        )
                    )

                    model = str(
                        product.get(
                            "model",
                            ""
                        )
                    )

                    score = float(
                        product.get(
                            "match_score",
                            product.get(
                                "score",
                                0
                            )
                        )
                    )

                    st.markdown(
                        f"### {index}. {product_name}"
                    )

                    # -------------------------------------------------
                    # Match score
                    # -------------------------------------------------

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "Match Score",
                            f"{score:.2f}%"
                        )

                    with col2:

                        st.write(
                            "**Brand**"
                        )

                        st.write(
                            brand
                            if brand.strip()
                            else "Not available"
                        )

                    with col3:

                        st.write(
                            "**Model**"
                        )

                        st.write(
                            model
                            if model.strip()
                            else "Not available"
                        )

                    st.write(
                        "**Category:**",
                        category
                        if category.strip()
                        else "Not available"
                    )

                    # -------------------------------------------------
                    # Product explanation
                    # -------------------------------------------------

                    with st.expander(
                        "💡 Why was this product recommended?"
                    ):

                        try:

                            explanation = (
                                explain_recommendation(
                                    requirement,
                                    product
                                )
                            )

                            st.write(
                                explanation
                            )

                        except Exception:

                            st.info(
                                "Recommendation explanation "
                                "is unavailable."
                            )

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

            else:

                st.warning(
                    "No matching products found."
                )


# =========================================================
# DATASHEET INTELLIGENCE
# =========================================================

elif page == "📄 Datasheet Intelligence":

    st.header(
        "📄 Datasheet Intelligence"
    )

    st.write(
        "Upload a product PDF/datasheet and extract "
        "structured product information."
    )

    uploaded_file = st.file_uploader(
        "Upload Product Datasheet",
        type=["pdf"]
    )

    if uploaded_file:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

        if st.button(
            "🤖 Analyze Datasheet",
            type="primary"
        ):

            with st.spinner(
                "Reading and analyzing datasheet..."
            ):

                try:

                    # -------------------------------------------------
                    # Extract PDF text
                    # -------------------------------------------------

                    pdf_text = extract_text_from_pdf(
                        uploaded_file
                    )

                    if not pdf_text.strip():

                        st.warning(
                            "No readable text was found "
                            "in this PDF."
                        )

                    else:

                        st.subheader(
                            "🧠 Extracted Product Intelligence"
                        )

                        # -------------------------------------------------
                        # AI extraction
                        # -------------------------------------------------

                        try:

                            extracted = (
                                extract_product_information(
                                    pdf_text
                                )
                            )

                            st.json(
                                extracted
                            )

                        except Exception as e:

                            st.warning(
                                "AI extraction unavailable."
                            )

                            st.code(
                                str(e)
                            )

                            st.text_area(
                                "Extracted Text",
                                pdf_text[:10000],
                                height=300
                            )

                        # -------------------------------------------------
                        # Raw text
                        # -------------------------------------------------

                        with st.expander(
                            "📄 View Extracted PDF Text"
                        ):

                            st.text(
                                pdf_text[:10000]
                            )

                except Exception as e:

                    st.error(
                        "PDF processing failed."
                    )

                    st.code(
                        str(e)
                    )


# =========================================================
# PRODUCT COMPARISON
# =========================================================

elif page == "📊 Product Comparison":

    st.header(
        "📊 Product Comparison"
    )

    st.write(
        "Search products and select up to 3 products."
    )

    comparison_query = st.text_input(
        "Search Products",
        placeholder="Example: industrial tool"
    )

    if comparison_query.strip():

        with st.spinner(
            "Finding products..."
        ):

            try:

                comparison_results = (
                    matcher.search(
                        comparison_query,
                        top_k=10
                    )
                )

            except Exception as e:

                st.error(
                    "Product search failed."
                )

                st.code(
                    str(e)
                )

                comparison_results = []

        if comparison_results:

            product_names = [
                product.get(
                    "product_name",
                    "Unknown Product"
                )
                for product in comparison_results
            ]

            selected_names = st.multiselect(
                "Select products to compare",
                product_names,
                max_selections=3
            )

            selected_products = [
                product
                for product in comparison_results
                if product.get(
                    "product_name"
                ) in selected_names
            ]

            if len(selected_products) >= 2:

                st.subheader(
                    "📊 Comparison"
                )

                # -------------------------------------------------
                # Create comparison table
                # -------------------------------------------------

                comparison_rows = []

                attributes = [
                    "brand",
                    "model",
                    "category",
                    "price",
                    "weight",
                    "dimensions",
                    "about",
                    "specification",
                    "technical_details"
                ]

                for attribute in attributes:

                    row = {
                        "Attribute":
                        attribute.replace(
                            "_",
                            " "
                        ).title()
                    }

                    for product in selected_products:

                        product_name = product.get(
                            "product_name",
                            "Product"
                        )

                        row[
                            product_name
                        ] = product.get(
                            attribute,
                            "Not available"
                        )

                    comparison_rows.append(
                        row
                    )

                comparison_table = pd.DataFrame(
                    comparison_rows
                )

                st.dataframe(
                    comparison_table,
                    use_container_width=True,
                    hide_index=True
                )

                # -------------------------------------------------
                # AI comparison
                # -------------------------------------------------

                st.subheader(
                    "🧠 AI Comparison"
                )

                try:

                    explanation = compare_products(
                        comparison_query,
                        selected_products
                    )

                    st.write(
                        explanation
                    )

                except Exception as e:

                    st.info(
                        "AI comparison explanation "
                        "is currently unavailable."
                    )

            elif len(selected_products) == 1:

                st.info(
                    "Select at least 2 products "
                    "to compare."
                )

        else:

            st.warning(
                "No products found."
            )


# =========================================================
# DATA QUALITY
# =========================================================

elif page == "🛡️ Data Quality":

    st.header(
        "🛡️ Product Data Quality"
    )

    st.write(
        "Check how complete a product's information is."
    )

    product_search = st.text_input(
        "Search Product",
        placeholder="Example: Dremel"
    )

    if product_search.strip():

        matches = products[
            products[
                "product_name"
            ]
            .fillna("")
            .astype(str)
            .str.contains(
                product_search,
                case=False,
                na=False
            )
        ].head(10)

        if matches.empty:

            st.warning(
                "No products found."
            )

        else:

            selected_product = st.selectbox(
                "Select Product",
                matches[
                    "product_name"
                ].tolist()
            )

            selected_row = matches[
                matches[
                    "product_name"
                ] == selected_product
            ].iloc[0]

            product = selected_row.to_dict()

            try:

                quality = analyze_data_quality(
                    product
                )

                # -------------------------------------------------
                # Metrics
                # -------------------------------------------------

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Completeness",
                        f"{quality['completeness']}%"
                    )

                with col2:

                    st.metric(
                        "Available Fields",
                        quality.get(
                            "available_fields",
                            0
                        )
                    )

                with col3:

                    st.metric(
                        "Missing Fields",
                        len(
                            quality.get(
                                "missing_fields",
                                []
                            )
                        )
                    )

                st.progress(
                    min(
                        float(
                            quality["completeness"]
                        ) / 100,
                        1.0
                    )
                )

                # -------------------------------------------------
                # Missing information
                # -------------------------------------------------

                st.subheader(
                    "⚠️ Missing Information"
                )

                missing_fields = quality.get(
                    "missing_fields",
                    []
                )

                if missing_fields:

                    for field in missing_fields:

                        st.warning(
                            field.replace(
                                "_",
                                " "
                            ).title()
                        )

                else:

                    st.success(
                        "No tracked information is missing."
                    )

                # -------------------------------------------------
                # Product data
                # -------------------------------------------------

                st.subheader(
                    "📦 Product Information"
                )

                st.json(
                    product
                )

            except Exception as e:

                st.error(
                    "Data quality analysis failed."
                )

                st.code(
                    str(e)
                )