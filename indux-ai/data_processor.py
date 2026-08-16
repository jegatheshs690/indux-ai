import pandas as pd
import re


INPUT_FILE = "data/product.csv"
OUTPUT_FILE = "data/processed_products.csv"


def clean_text(value):
    """Clean a text value safely."""
    if pd.isna(value):
        return ""

    value = str(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def load_data():
    print("Loading dataset...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Total products loaded: {len(df)}")

    return df


def prepare_products(df):

    # Keep only fields useful for our prototype
    columns = [
        "Uniq Id",
        "Product Name",
        "Brand Name",
        "Category",
        "Model Number",
        "About Product",
        "Product Specification",
        "Technical Details",
        "Shipping Weight",
        "Product Dimensions",
        "Selling Price",
        "Product Url"
    ]

    # Only keep columns that actually exist
    columns = [column for column in columns if column in df.columns]

    products = df[columns].copy()

    # Rename columns to simple names
    products = products.rename(columns={
        "Uniq Id": "product_id",
        "Product Name": "product_name",
        "Brand Name": "brand",
        "Category": "category",
        "Model Number": "model",
        "About Product": "about",
        "Product Specification": "specification",
        "Technical Details": "technical_details",
        "Shipping Weight": "weight",
        "Product Dimensions": "dimensions",
        "Selling Price": "price",
        "Product Url": "source_url"
    })

    # Clean text fields
    text_columns = [
        "product_name",
        "brand",
        "category",
        "model",
        "about",
        "specification",
        "technical_details",
        "weight",
        "dimensions"
    ]

    for column in text_columns:
        if column in products.columns:
            products[column] = products[column].apply(clean_text)

    # Combine useful information for search/matching
    products["search_text"] = (
        products["product_name"] + " " +
        products["category"] + " " +
        products["about"] + " " +
        products["specification"] + " " +
        products["technical_details"]
    )

    # Remove products without a name
    products = products[
        products["product_name"].str.len() > 0
    ]

    # Remove duplicate product names
    products = products.drop_duplicates(
        subset=["product_name"]
    )

    return products


def main():

    df = load_data()

    products = prepare_products(df)

    print(f"Products after cleaning: {len(products)}")

    products.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"Saved cleaned dataset to: {OUTPUT_FILE}")

    print("\nColumns:")
    print(products.columns.tolist())

    print("\nSample products:")

    print(
        products[
            [
                "product_name",
                "category"
            ]
        ].head(10).to_string(index=False)
    )


if __name__ == "__main__":
    main()