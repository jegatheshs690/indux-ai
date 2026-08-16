import fitz
import re


# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_text_from_pdf(pdf_file):
    """
    Extract text from an uploaded PDF.

    pdf_file can be:
    - a file path
    - a Streamlit UploadedFile
    """

    try:

        # Streamlit UploadedFile
        if hasattr(pdf_file, "read"):

            pdf_bytes = pdf_file.read()

            document = fitz.open(
                stream=pdf_bytes,
                filetype="pdf"
            )

        # Normal file path
        else:

            document = fitz.open(
                pdf_file
            )

        text = ""

        for page in document:

            page_text = page.get_text()

            if page_text:

                text += page_text
                text += "\n"

        document.close()

        return text.strip()

    except Exception as e:

        print(
            f"PDF extraction error: {e}"
        )

        return ""


# =========================================================
# CLEAN PDF TEXT
# =========================================================

def clean_text(text):

    if not text:
        return ""

    # Remove excessive spaces
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Remove excessive blank lines
    text = re.sub(
        r"\n\s*\n+",
        "\n\n",
        text
    )

    return text.strip()


# =========================================================
# EXTRACT COMMON PRODUCT ATTRIBUTES
# =========================================================

def extract_attributes(text):

    text_lower = text.lower()

    attributes = {
        "product_type": None,
        "material": None,
        "pressure": None,
        "flow_rate": None,
        "voltage": None,
        "power": None,
        "temperature": None,
        "weight": None,
        "dimensions": None
    }

    # -----------------------------------------------------
    # Product type
    # -----------------------------------------------------

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
        "tool"
    ]

    for product_type in product_types:

        if re.search(
            r"\b" +
            re.escape(product_type) +
            r"\b",
            text_lower
        ):

            attributes[
                "product_type"
            ] = product_type

            break

    # -----------------------------------------------------
    # Material
    # -----------------------------------------------------

    materials = [
        "stainless steel",
        "carbon steel",
        "aluminum",
        "aluminium",
        "copper",
        "brass",
        "iron",
        "plastic",
        "rubber"
    ]

    for material in materials:

        if material in text_lower:

            attributes[
                "material"
            ] = material.title()

            break

    # -----------------------------------------------------
    # Pressure
    # -----------------------------------------------------

    pressure = re.search(
        r"(\d+(?:\.\d+)?)\s*(bar|psi|mpa)",
        text_lower
    )

    if pressure:

        attributes[
            "pressure"
        ] = pressure.group(0)

    # -----------------------------------------------------
    # Flow rate
    # -----------------------------------------------------

    flow = re.search(
        r"(\d+(?:\.\d+)?)\s*"
        r"(l/min|lpm|gpm)",
        text_lower
    )

    if flow:

        attributes[
            "flow_rate"
        ] = flow.group(0)

    # -----------------------------------------------------
    # Voltage
    # -----------------------------------------------------

    voltage = re.search(
        r"(\d+(?:\.\d+)?)\s*(v|volt|volts)",
        text_lower
    )

    if voltage:

        attributes[
            "voltage"
        ] = voltage.group(0)

    # -----------------------------------------------------
    # Power
    # -----------------------------------------------------

    power = re.search(
        r"(\d+(?:\.\d+)?)\s*"
        r"(kw|w|hp|horsepower)",
        text_lower
    )

    if power:

        attributes[
            "power"
        ] = power.group(0)

    # -----------------------------------------------------
    # Temperature
    # -----------------------------------------------------

    temperature = re.search(
        r"(-?\d+(?:\.\d+)?)\s*"
        r"(°c|celsius|degrees c)",
        text_lower
    )

    if temperature:

        attributes[
            "temperature"
        ] = temperature.group(0)

    # -----------------------------------------------------
    # Weight
    # -----------------------------------------------------

    weight = re.search(
        r"(\d+(?:\.\d+)?)\s*"
        r"(kg|kilograms|g|grams|lb|lbs)",
        text_lower
    )

    if weight:

        attributes[
            "weight"
        ] = weight.group(0)

    # -----------------------------------------------------
    # Dimensions
    # -----------------------------------------------------

    dimensions = re.search(
        r"(\d+(?:\.\d+)?\s*[x×]\s*"
        r"\d+(?:\.\d+)?"
        r"(?:\s*[x×]\s*\d+(?:\.\d+)?)?)\s*"
        r"(mm|cm|in|inch|inches)?",
        text_lower
    )

    if dimensions:

        attributes[
            "dimensions"
        ] = dimensions.group(0)

    return attributes


# =========================================================
# COMPLETE PDF PROCESSING
# =========================================================

def process_pdf(pdf_file):

    raw_text = extract_text_from_pdf(
        pdf_file
    )

    if not raw_text:

        return {
            "success": False,
            "text": "",
            "attributes": {}
        }

    cleaned_text = clean_text(
        raw_text
    )

    attributes = extract_attributes(
        cleaned_text
    )

    return {
        "success": True,
        "text": cleaned_text,
        "attributes": attributes
    }


# =========================================================
# TERMINAL TEST
# =========================================================

if __name__ == "__main__":

    pdf_path = input(
        "Enter PDF file path: "
    )

    result = process_pdf(
        pdf_path
    )

    if not result["success"]:

        print(
            "\nCould not extract text from PDF."
        )

    else:

        print(
            "\nPDF processed successfully!"
        )

        print(
            "\nExtracted Attributes:"
        )

        for key, value in result[
            "attributes"
        ].items():

            print(
                f"{key}: {value}"
            )

        print(
            "\nExtracted Text Preview:"
        )

        print(
            result["text"][:3000]
        )