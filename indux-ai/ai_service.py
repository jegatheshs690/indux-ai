import re


# =========================================================
# INDUX AI - LOCAL AI SERVICE
# API KEY NOT REQUIRED
# =========================================================
#
# This module provides lightweight local AI/NLP functionality
# for the InduX AI hackathon prototype.
#
# Features:
#   1. Product information extraction
#   2. Recommendation explanation
#   3. Product comparison
#   4. Data quality analysis
#
# No external AI API is required.
# =========================================================


# =========================================================
# UTILITY
# =========================================================

def clean_value(value):
    """
    Convert a value into a clean string.

    Empty/invalid values such as NaN, None and null
    are converted into an empty string.
    """

    if value is None:
        return ""

    value = str(value).strip()

    if value.lower() in [
        "nan",
        "none",
        "null",
        ""
    ]:
        return ""

    return value


# =========================================================
# PRODUCT INFORMATION EXTRACTION
# =========================================================

def extract_product_information(
    pdf_text,
    existing_attributes=None
):
    """
    Extract structured product information from PDF text
    using lightweight local NLP and regular expressions.

    No API key is required.
    """

    if existing_attributes is None:
        existing_attributes = {}

    text = clean_value(pdf_text)

    # -----------------------------------------------------
    # Empty PDF
    # -----------------------------------------------------

    if not text:

        return {
            "product_name": None,
            "product_type": None,
            "manufacturer": None,
            "model": None,
            "material": None,
            "application": None,
            "pressure": None,
            "flow_rate": None,
            "voltage": None,
            "power": None,
            "temperature": None,
            "weight": None,
            "dimensions": None,
            "certification": None,
            "important_specifications": []
        }

    text_lower = text.lower()

    # -----------------------------------------------------
    # Initial result structure
    # -----------------------------------------------------

    result = {

        "product_name":
            existing_attributes.get(
                "product_name"
            ),

        "product_type":
            existing_attributes.get(
                "product_type"
            ),

        "manufacturer":
            existing_attributes.get(
                "manufacturer"
            ),

        "model":
            existing_attributes.get(
                "model"
            ),

        "material":
            existing_attributes.get(
                "material"
            ),

        "application":
            existing_attributes.get(
                "application"
            ),

        "pressure":
            existing_attributes.get(
                "pressure"
            ),

        "flow_rate":
            existing_attributes.get(
                "flow_rate"
            ),

        "voltage":
            existing_attributes.get(
                "voltage"
            ),

        "power":
            existing_attributes.get(
                "power"
            ),

        "temperature":
            existing_attributes.get(
                "temperature"
            ),

        "weight":
            existing_attributes.get(
                "weight"
            ),

        "dimensions":
            existing_attributes.get(
                "dimensions"
            ),

        "certification":
            existing_attributes.get(
                "certification"
            ),

        "important_specifications":
            []
    }

    # =====================================================
    # PRODUCT NAME
    # =====================================================

    if not result["product_name"]:

        product_name_patterns = [

            r"product\s*name\s*[:\-]\s*([^\n]+)",

            r"product\s*[:\-]\s*([^\n]+)",

            r"model\s*name\s*[:\-]\s*([^\n]+)"
        ]

        for pattern in product_name_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                result["product_name"] = (
                    match.group(1).strip()
                )

                break

    # =====================================================
    # PRODUCT TYPE
    # =====================================================

    product_types = [

        "pump",
        "motor",
        "valve",
        "compressor",
        "generator",
        "drill",
        "grinder",
        "saw",
        "sensor",
        "switch",
        "filter",
        "hose",
        "bearing",
        "clamp",
        "cable",
        "controller",
        "transformer",
        "fan",
        "blower",
        "machine",
        "machinery",
        "tool",
        "equipment"
    ]

    if not result["product_type"]:

        for product_type in product_types:

            if re.search(
                r"\b"
                + re.escape(product_type)
                + r"\b",
                text_lower
            ):

                result["product_type"] = (
                    product_type.title()
                )

                break

    # =====================================================
    # MANUFACTURER
    # =====================================================

    manufacturer_patterns = [

        r"manufacturer\s*[:\-]\s*([^\n]+)",

        r"manufactured\s*by\s*[:\-]?\s*([^\n]+)",

        r"brand\s*[:\-]\s*([^\n]+)",

        r"maker\s*[:\-]\s*([^\n]+)"
    ]

    if not result["manufacturer"]:

        for pattern in manufacturer_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                result["manufacturer"] = (
                    match.group(1).strip()
                )

                break

    # =====================================================
    # MODEL
    # =====================================================

    model_patterns = [

        r"model\s*(?:number|no\.|#)?"
        r"\s*[:\-]\s*([A-Za-z0-9\-_./]+)",

        r"part\s*(?:number|no\.|#)?"
        r"\s*[:\-]\s*([A-Za-z0-9\-_./]+)",

        r"model\s*[:\-]\s*([A-Za-z0-9\-_./]+)"
    ]

    if not result["model"]:

        for pattern in model_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                result["model"] = (
                    match.group(1).strip()
                )

                break

    # =====================================================
    # MATERIAL
    # =====================================================

    material_patterns = [

        r"material\s*[:\-]\s*([^\n]+)",

        r"construction\s*[:\-]\s*([^\n]+)",

        r"body\s*material\s*[:\-]\s*([^\n]+)"
    ]

    if not result["material"]:

        for pattern in material_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                result["material"] = (
                    match.group(1).strip()
                )

                break

    # =====================================================
    # APPLICATION
    # =====================================================

    application_patterns = [

        r"application\s*[:\-]\s*([^\n]+)",

        r"applications\s*[:\-]\s*([^\n]+)",

        r"intended\s*use\s*[:\-]\s*([^\n]+)",

        r"use\s*case\s*[:\-]\s*([^\n]+)"
    ]

    if not result["application"]:

        for pattern in application_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                result["application"] = (
                    match.group(1).strip()
                )

                break

    # =====================================================
    # PRESSURE
    # =====================================================

    pressure_patterns = [

        r"maximum\s*pressure\s*[:\-]?\s*([^\n]+)",

        r"max\s*pressure\s*[:\-]?\s*([^\n]+)",

        r"operating\s*pressure\s*[:\-]?\s*([^\n]+)",

        r"pressure\s*[:\-]\s*([^\n]+)"
    ]

    if not result["pressure"]:

        for pattern in pressure_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                result["pressure"] = (
                    match.group(1).strip()
                )

                break

    # =====================================================
    # FLOW RATE
    # =====================================================

    flow_patterns = [

        r"flow\s*rate\s*[:\-]?\s*([^\n]+)",

        r"maximum\s*flow\s*[:\-]?\s*([^\n]+)",

        r"max\s*flow\s*[:\-]?\s*([^\n]+)"
    ]

    if not result["flow_rate"]:

        for pattern in flow_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                result["flow_rate"] = (
                    match.group(1).strip()
                )

                break

    # =====================================================
    # VOLTAGE
    # =====================================================

    voltage_patterns = [

        r"input\s*voltage\s*[:\-]?\s*([^\n]+)",

        r"operating\s*voltage\s*[:\-]?\s*([^\n]+)",

        r"voltage\s*[:\-]\s*([^\n]+)"
    ]

    if not result["voltage"]:

        for pattern in voltage_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                result["voltage"] = (
                    match.group(1).strip()
                )

                break

    # =====================================================
    # POWER
    # =====================================================

    power_patterns = [

        r"power\s*[:\-]\s*([^\n]+)",

        r"rated\s*power\s*[:\-]\s*([^\n]+)",

        r"power\s*rating\s*[:\-]\s*([^\n]+)"
    ]

    if not result["power"]:

        for pattern in power_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                result["power"] = (
                    match.group(1).strip()
                )

                break

    # =====================================================
    # TEMPERATURE
    # =====================================================

    temperature_patterns = [

        r"operating\s*temperature\s*[:\-]?\s*([^\n]+)",

        r"maximum\s*temperature\s*[:\-]?\s*([^\n]+)",

        r"max\s*temperature\s*[:\-]?\s*([^\n]+)",

        r"temperature\s*[:\-]\s*([^\n]+)"
    ]

    if not result["temperature"]:

        for pattern in temperature_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                result["temperature"] = (
                    match.group(1).strip()
                )

                break

    # =====================================================
    # WEIGHT
    # =====================================================

    weight_patterns = [

        r"shipping\s*weight\s*[:\-]?\s*([^\n]+)",

        r"net\s*weight\s*[:\-]?\s*([^\n]+)",

        r"weight\s*[:\-]\s*([^\n]+)"
    ]

    if not result["weight"]:

        for pattern in weight_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                result["weight"] = (
                    match.group(1).strip()
                )

                break

    # =====================================================
    # DIMENSIONS
    # =====================================================

    dimension_patterns = [

        r"product\s*dimensions\s*[:\-]?\s*([^\n]+)",

        r"dimensions\s*[:\-]\s*([^\n]+)",

        r"size\s*[:\-]\s*([^\n]+)"
    ]

    if not result["dimensions"]:

        for pattern in dimension_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                result["dimensions"] = (
                    match.group(1).strip()
                )

                break

    # =====================================================
    # CERTIFICATIONS
    # =====================================================

    certifications = [

        "ISO 9001",
        "ISO 14001",
        "ISO 45001",
        "CE",
        "UL",
        "RoHS",
        "ANSI",
        "ASME",
        "IEC",
        "ATEX",
        "FDA"
    ]

    found_certifications = []

    for certification in certifications:

        if certification.lower() in text_lower:

            found_certifications.append(
                certification
            )

    if found_certifications:

        result["certification"] = (
            ", ".join(found_certifications)
        )

    # =====================================================
    # IMPORTANT SPECIFICATIONS
    # =====================================================

    specification_patterns = [

        r"maximum\s*pressure\s*[:\-]?\s*([^\n]+)",

        r"max\s*pressure\s*[:\-]?\s*([^\n]+)",

        r"operating\s*pressure\s*[:\-]?\s*([^\n]+)",

        r"flow\s*rate\s*[:\-]?\s*([^\n]+)",

        r"input\s*voltage\s*[:\-]?\s*([^\n]+)",

        r"operating\s*voltage\s*[:\-]?\s*([^\n]+)",

        r"power\s*[:\-]?\s*([^\n]+)",

        r"operating\s*temperature\s*[:\-]?\s*([^\n]+)",

        r"maximum\s*temperature\s*[:\-]?\s*([^\n]+)",

        r"material\s*[:\-]?\s*([^\n]+)"
    ]

    for pattern in specification_patterns:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        for match in matches[:2]:

            value = clean_value(match)

            if value and value not in result[
                "important_specifications"
            ]:

                result[
                    "important_specifications"
                ].append(value)

    # =====================================================
    # FALLBACK PRODUCT NAME
    # =====================================================

    if not result["product_name"]:

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if lines:

            first_line = lines[0]

            if len(first_line) <= 150:

                result["product_name"] = (
                    first_line
                )

    return result


# =========================================================
# EXPLAIN RECOMMENDATION
# =========================================================

def explain_recommendation(
    requirement,
    product
):
    """
    Generate an explainable recommendation using
    actual product information.
    """

    requirement = clean_value(
        requirement
    )

    product_name = clean_value(
        product.get(
            "product_name"
        )
    )

    category = clean_value(
        product.get(
            "category"
        )
    )

    brand = clean_value(
        product.get(
            "brand"
        )
    )

    model = clean_value(
        product.get(
            "model"
        )
    )

    about = clean_value(
        product.get(
            "about"
        )
    )

    specification = clean_value(
        product.get(
            "specification"
        )
    )

    technical_details = clean_value(
        product.get(
            "technical_details"
        )
    )

    score = product.get(
        "match_score",
        0
    )

    # =====================================================
    # PRODUCT TEXT
    # =====================================================

    product_text = " ".join([

        product_name,

        category,

        brand,

        model,

        about,

        specification,

        technical_details
    ]).lower()

    # =====================================================
    # REQUIREMENT WORD MATCHING
    # =====================================================

    requirement_words = set(
        re.findall(
            r"\b[a-zA-Z0-9]+\b",
            requirement.lower()
        )
    )

    matched_words = []

    for word in requirement_words:

        if len(word) < 3:
            continue

        if word in product_text:

            matched_words.append(
                word
            )

    # =====================================================
    # BUILD EXPLANATION
    # =====================================================

    explanation = []

    explanation.append(
        f"### Why this product was recommended"
    )

    explanation.append(
        f"**{product_name}** achieved a "
        f"**{score}% match** based on the available "
        f"product information."
    )

    if matched_words:

        explanation.append(
            "✓ Matching evidence found for: "
            + ", ".join(
                sorted(
                    matched_words
                )[:10]
            )
            + "."
        )

    if category:

        explanation.append(
            f"✓ Product category: **{category}**."
        )

    if brand:

        explanation.append(
            f"✓ Brand information available: "
            f"**{brand}**."
        )

    if model:

        explanation.append(
            f"✓ Model information available: "
            f"**{model}**."
        )

    if specification:

        explanation.append(
            "✓ Technical specification information "
            "is available."
        )

    else:

        explanation.append(
            "⚠ Technical specification information "
            "is limited."
        )

    if about:

        explanation.append(
            "✓ Product description is available "
            "and was considered during matching."
        )

    # =====================================================
    # LIMITATION
    # =====================================================

    explanation.append(
        "⚠ Recommendation is based only on the "
        "information available in the product dataset. "
        "It should not be treated as a certified "
        "engineering recommendation."
    )

    return "\n\n".join(
        explanation
    )


# =========================================================
# PRODUCT COMPARISON
# =========================================================

def compare_products(
    requirement,
    products
):
    """
    Generate a transparent comparison based only
    on supplied product information.
    """

    if not products:

        return (
            "No products selected for comparison."
        )

    lines = []

    lines.append(
        "### Product Comparison"
    )

    if requirement:

        lines.append(
            f"Requested requirement: "
            f"**{clean_value(requirement)}**"
        )

    lines.append("")

    # =====================================================
    # FIND BEST MATCH
    # =====================================================

    def get_score(product):

        try:

            return float(
                product.get(
                    "match_score",
                    0
                )
            )

        except Exception:

            return 0

    best_product = max(
        products,
        key=get_score
    )

    best_name = clean_value(
        best_product.get(
            "product_name"
        )
    )

    best_score = get_score(
        best_product
    )

    lines.append(
        f"🏆 **Strongest available match:** "
        f"{best_name} "
        f"({best_score:.2f}% match)"
    )

    lines.append("")

    # =====================================================
    # EACH PRODUCT
    # =====================================================

    for product in products:

        name = clean_value(
            product.get(
                "product_name"
            )
        )

        score = get_score(
            product
        )

        category = clean_value(
            product.get(
                "category"
            )
        )

        brand = clean_value(
            product.get(
                "brand"
            )
        )

        model = clean_value(
            product.get(
                "model"
            )
        )

        specification = clean_value(
            product.get(
                "specification"
            )
        )

        technical_details = clean_value(
            product.get(
                "technical_details"
            )
        )

        lines.append(
            f"**{name}** — "
            f"**{score:.2f}% match**"
        )

        if brand:

            lines.append(
                f"- Brand: {brand}"
            )

        if model:

            lines.append(
                f"- Model: {model}"
            )

        if category:

            lines.append(
                f"- Category: {category}"
            )

        if specification:

            lines.append(
                "- ✓ Specification information available"
            )

        else:

            lines.append(
                "- ⚠ Limited specification information"
            )

        if technical_details:

            lines.append(
                "- ✓ Technical details available"
            )

        else:

            lines.append(
                "- ⚠ Technical details unavailable"
            )

        lines.append("")

    # =====================================================
    # SIMPLE COMPARISON CONCLUSION
    # =====================================================

    if len(products) >= 2:

        scores = [
            get_score(product)
            for product in products
        ]

        highest = max(scores)
        lowest = min(scores)

        difference = highest - lowest

        if difference >= 15:

            lines.append(
                "### Recommendation Insight"
            )

            lines.append(
                "The highest-ranked product has a "
                "significantly stronger matching score "
                "than the lowest-ranked option."
            )

        elif difference >= 5:

            lines.append(
                "### Recommendation Insight"
            )

            lines.append(
                "The products have moderately different "
                "matching scores. Review their technical "
                "specifications before selecting one."
            )

        else:

            lines.append(
                "### Recommendation Insight"
            )

            lines.append(
                "The products have relatively similar "
                "matching scores. The final choice should "
                "consider the available technical details."
            )

    # =====================================================
    # SAFETY NOTE
    # =====================================================

    lines.append("")

    lines.append(
        "⚠ This comparison uses only the available "
        "dataset information. It is not a real-world "
        "engineering compatibility guarantee."
    )

    return "\n".join(
        lines
    )


# =========================================================
# DATA QUALITY ANALYSIS
# =========================================================

def analyze_data_quality(product):
    """
    Calculate a transparent product-data completeness
    score using actual available fields.
    """

    fields = [

        "product_name",

        "category",

        "brand",

        "model",

        "about",

        "specification",

        "technical_details",

        "weight",

        "dimensions",

        "price"
    ]

    available = 0

    missing = []

    # =====================================================
    # CHECK FIELDS
    # =====================================================

    for field in fields:

        value = clean_value(
            product.get(
                field,
                ""
            )
        )

        if value:

            available += 1

        else:

            missing.append(
                field
            )

    # =====================================================
    # COMPLETENESS
    # =====================================================

    if fields:

        completeness = round(
            (
                available /
                len(fields)
            ) * 100,
            2
        )

    else:

        completeness = 0

    # =====================================================
    # SIMPLE CONFIDENCE
    # =====================================================

    confidence = completeness

    # =====================================================
    # RETURN RESULT
    # =====================================================

    return {

        "completeness":
            completeness,

        "confidence":
            confidence,

        "available_fields":
            available,

        "total_fields":
            len(fields),

        "missing_fields":
            missing
    }


# =========================================================
# LOCAL AI SERVICE TEST
# =========================================================

if __name__ == "__main__":

    print(
        "========================================"
    )

    print(
        "          INDUX AI SERVICE"
    )

    print(
        "========================================"
    )

    print(
        "Local AI service loaded successfully!"
    )

    print(
        "No API key is required."
    )

    print()

    # -----------------------------------------------------
    # Sample PDF-like text
    # -----------------------------------------------------

    sample_text = """

    Industrial Stainless Steel Pump

    Manufacturer: ABC Industries

    Model: P250

    Material: Stainless Steel

    Application: Chemical Processing

    Maximum Pressure: 250 bar

    Flow Rate: 18 L/min

    Input Voltage: 230 V

    Power: 2.5 kW

    Operating Temperature: 120 C

    Weight: 18 kg

    Product Dimensions: 300 x 200 x 180 mm

    Certification: ISO 9001, CE

    """

    # -----------------------------------------------------
    # Test extraction
    # -----------------------------------------------------

    result = extract_product_information(
        sample_text
    )

    print(
        "Sample Product Extraction:"
    )

    print()

    for key, value in result.items():

        print(
            f"{key}: {value}"
        )

    print()

    # -----------------------------------------------------
    # Test quality analysis
    # -----------------------------------------------------

    quality = analyze_data_quality(
        result
    )

    print(
        "Sample Data Quality:"
    )

    print(
        quality
    )

    print()

    print(
        "========================================"
    )

    print(
        "AI service test completed successfully!"
    )

    print(
        "========================================"
    )