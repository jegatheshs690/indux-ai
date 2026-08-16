import pandas as pd
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# DATA FILE
# =========================================================

from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "products.csv"


# =========================================================
# PRODUCT TYPES
# =========================================================

PRODUCT_TYPES = [
    "pump",
    "motor",
    "valve",
    "tool",
    "drill",
    "compressor",
    "bearing",
    "sensor",
    "switch",
    "cable",
    "machine",
    "machinery",
    "equipment",
    "welding",
    "generator",
    "filter",
    "hose",
    "clamp",
    "wrench",
    "hammer",
    "saw",
    "grinder",
]


# =========================================================
# MATERIALS
# =========================================================

MATERIALS = [
    "stainless steel",
    "carbon steel",
    "aluminum",
    "aluminium",
    "plastic",
    "rubber",
    "copper",
    "brass",
    "iron",
]


# =========================================================
# INDUSTRIAL KEYWORDS
# =========================================================

INDUSTRIAL_WORDS = [
    "industrial",
    "machinery",
    "machine",
    "equipment",
    "hardware",
    "electrical",
    "mechanical",
    "manufacturing",
    "engineering",
    "commercial",
    "professional",
]


# =========================================================
# IRRELEVANT CONSUMER CATEGORIES
# =========================================================

IRRELEVANT_CATEGORIES = [
    "toys & games",
    "clothing",
    "baby products",
    "costumes",
    "dolls",
    "stuffed animals",
    "puzzles",
    "party supplies",
    "games & accessories",
]


# =========================================================
# REQUIREMENT EXTRACTION
# =========================================================

def extract_requirements(query):

    query_lower = query.lower()

    requirements = {
        "product_type": None,
        "materials": [],
        "numbers": [],
        "industrial": False
    }

    # -----------------------------------------------------
    # Detect product type
    # -----------------------------------------------------

    sorted_product_types = sorted(
        PRODUCT_TYPES,
        key=len,
        reverse=True
    )

    for product_type in sorted_product_types:

        pattern = (
            r"\b" +
            re.escape(product_type) +
            r"\b"
        )

        if re.search(
            pattern,
            query_lower
        ):

            requirements["product_type"] = product_type

            break

    # -----------------------------------------------------
    # Detect materials
    # -----------------------------------------------------

    sorted_materials = sorted(
        MATERIALS,
        key=len,
        reverse=True
    )

    for material in sorted_materials:

        if material in query_lower:

            if (
                material == "carbon steel"
                and
                "stainless steel" in query_lower
            ):
                continue

            requirements["materials"].append(
                material
            )

    # -----------------------------------------------------
    # Detect industrial requirement
    # -----------------------------------------------------

    industrial_query_words = [
        "industrial",
        "commercial",
        "professional",
        "manufacturing",
        "factory",
        "machinery"
    ]

    for word in industrial_query_words:

        pattern = (
            r"\b" +
            re.escape(word) +
            r"\b"
        )

        if re.search(
            pattern,
            query_lower
        ):

            requirements["industrial"] = True

            break

    # -----------------------------------------------------
    # Detect technical numbers
    # -----------------------------------------------------

    numbers = re.findall(
        r"\d+(?:\.\d+)?\s*"
        r"(?:bar|psi|v|volt|volts|w|kw|kg|g|mm|cm|"
        r"l/min|rpm|°c|c)",
        query_lower
    )

    requirements["numbers"] = numbers

    return requirements


# =========================================================
# PRODUCT MATCHER
# =========================================================

class ProductMatcher:

    def __init__(self):

        print("Loading products...")

        self.df = pd.read_csv(
            DATA_FILE
        )

        # -------------------------------------------------
        # Make important columns safe
        # -------------------------------------------------

        columns_to_clean = [
            "product_id",
            "product_name",
            "category",
            "brand",
            "model",
            "about",
            "specification",
            "technical_details",
            "weight",
            "dimensions",
            "price",
            "source_url"
        ]

        for column in columns_to_clean:

            if column not in self.df.columns:

                self.df[column] = ""

            self.df[column] = (
                self.df[column]
                .fillna("")
                .astype(str)
            )

        # -------------------------------------------------
        # IMPORTANT DEPLOYMENT FIX
        #
        # products.csv does not contain search_text.
        # Create it automatically from the available
        # product information.
        # -------------------------------------------------

        search_columns = [
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

        self.df["search_text"] = (
            self.df[search_columns]
            .fillna("")
            .astype(str)
            .agg(
                " ".join,
                axis=1
            )
            .str.lower()
            .str.replace(
                r"\s+",
                " ",
                regex=True
            )
            .str.strip()
        )

        print(
            f"Products available for matching: "
            f"{len(self.df)}"
        )

        # -------------------------------------------------
        # Build TF-IDF search index
        # -------------------------------------------------

        print(
            "Building search index..."
        )

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=15000,
            ngram_range=(1, 2)
        )

        self.product_vectors = (
            self.vectorizer.fit_transform(
                self.df["search_text"]
            )
        )

        print(
            "Search index ready!"
        )

    # =====================================================
    # CALCULATE PRODUCT SCORE
    # =====================================================

    def calculate_score(
        self,
        product,
        similarity,
        requirements,
        query
    ):

        # -------------------------------------------------
        # Base semantic similarity
        # -------------------------------------------------

        score = similarity * 45

        # -------------------------------------------------
        # Combine product information
        # -------------------------------------------------

        product_name = str(
            product.get(
                "product_name",
                ""
            )
        ).lower()

        category = str(
            product.get(
                "category",
                ""
            )
        ).lower()

        about = str(
            product.get(
                "about",
                ""
            )
        ).lower()

        specification = str(
            product.get(
                "specification",
                ""
            )
        ).lower()

        technical_details = str(
            product.get(
                "technical_details",
                ""
            )
        ).lower()

        text = (
            product_name + " " +
            category + " " +
            about + " " +
            specification + " " +
            technical_details
        )

        query_lower = query.lower()

        # =================================================
        # 1. PRODUCT TYPE
        # =================================================

        product_type = requirements[
            "product_type"
        ]

        if product_type:

            pattern = (
                r"\b" +
                re.escape(product_type) +
                r"\b"
            )

            if re.search(
                pattern,
                product_name
            ):

                score += 30

            elif re.search(
                pattern,
                category
            ):

                score += 25

            elif re.search(
                pattern,
                text
            ):

                score += 12

            else:

                score -= 15

        # =================================================
        # 2. MATERIAL
        # =================================================

        materials = requirements[
            "materials"
        ]

        if materials:

            matched_materials = 0

            for material in materials:

                if material in text:

                    matched_materials += 1

            material_score = (
                18 *
                matched_materials /
                len(materials)
            )

            score += material_score

            if matched_materials == 0:

                score -= 8

        # =================================================
        # 3. INDUSTRIAL RELEVANCE
        # =================================================

        if requirements[
            "industrial"
        ]:

            industrial_match = False

            for word in INDUSTRIAL_WORDS:

                if word in category:

                    industrial_match = True

                    break

            if not industrial_match:

                for word in INDUSTRIAL_WORDS:

                    if word in text:

                        industrial_match = True

                        break

            if industrial_match:

                score += 15

            else:

                score -= 12

        # =================================================
        # 4. PENALIZE CONSUMER PRODUCTS
        # =================================================

        for word in IRRELEVANT_CATEGORIES:

            if word in category:

                score -= 30

                break

        # =================================================
        # 5. TECHNICAL INFORMATION BONUS
        # =================================================

        technical_fields = 0

        if about.strip():

            technical_fields += 1

        if specification.strip():

            technical_fields += 1

        if technical_details.strip():

            technical_fields += 1

        score += (
            technical_fields * 2
        )

        # =================================================
        # 6. NUMERIC REQUIREMENT
        # =================================================

        numbers = requirements[
            "numbers"
        ]

        if numbers:

            matched_numbers = 0

            for number in numbers:

                numeric_part = re.findall(
                    r"\d+(?:\.\d+)?",
                    number
                )

                if numeric_part:

                    value = numeric_part[0]

                    if value in text:

                        matched_numbers += 1

            numeric_score = (
                5 *
                matched_numbers /
                len(numbers)
            )

            score += numeric_score

        # =================================================
        # 7. EXACT QUERY WORD BONUS
        # =================================================

        query_words = [
            word
            for word in re.findall(
                r"\b[a-zA-Z]+\b",
                query_lower
            )
            if len(word) >= 4
        ]

        matched_query_words = 0

        for word in query_words:

            if word in text:

                matched_query_words += 1

        if query_words:

            keyword_score = (
                5 *
                matched_query_words /
                len(query_words)
            )

            score += keyword_score

        # =================================================
        # FINAL SCORE
        # =================================================

        return max(
            0,
            min(
                100,
                score
            )
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def search(
        self,
        query,
        top_k=5
    ):

        if (
            not query or
            not query.strip()
        ):

            return []

        # -------------------------------------------------
        # Extract requirements
        # -------------------------------------------------

        requirements = extract_requirements(
            query
        )

        # -------------------------------------------------
        # Query TF-IDF vector
        # -------------------------------------------------

        query_vector = (
            self.vectorizer.transform(
                [query]
            )
        )

        # -------------------------------------------------
        # Calculate similarity
        # -------------------------------------------------

        similarities = cosine_similarity(
            query_vector,
            self.product_vectors
        ).flatten()

        # -------------------------------------------------
        # Candidate pool
        # -------------------------------------------------

        candidate_count = min(
            300,
            len(self.df)
        )

        candidate_indices = (
            similarities
            .argsort()
            [-candidate_count:]
            [::-1]
        )

        results = []

        # -------------------------------------------------
        # Score candidates
        # -------------------------------------------------

        for index in candidate_indices:

            product = self.df.iloc[
                index
            ]

            score = self.calculate_score(
                product,
                similarities[index],
                requirements,
                query
            )

            results.append({

                "product_id":
                    product.get(
                        "product_id",
                        ""
                    ),

                "product_name":
                    product.get(
                        "product_name",
                        ""
                    ),

                "category":
                    product.get(
                        "category",
                        ""
                    ),

                "brand":
                    product.get(
                        "brand",
                        ""
                    ),

                "model":
                    product.get(
                        "model",
                        ""
                    ),

                "about":
                    product.get(
                        "about",
                        ""
                    ),

                "specification":
                    product.get(
                        "specification",
                        ""
                    ),

                "technical_details":
                    product.get(
                        "technical_details",
                        ""
                    ),

                "weight":
                    product.get(
                        "weight",
                        ""
                    ),

                "dimensions":
                    product.get(
                        "dimensions",
                        ""
                    ),

                "price":
                    product.get(
                        "price",
                        ""
                    ),

                "source_url":
                    product.get(
                        "source_url",
                        ""
                    ),

                "match_score":
                    round(
                        score,
                        2
                    )
            })

        # -------------------------------------------------
        # Sort by final score
        # -------------------------------------------------

        results.sort(
            key=lambda x:
                x["match_score"],
            reverse=True
        )

        return results[
            :top_k
        ]


# =========================================================
# COMMAND-LINE TEST
# =========================================================

if __name__ == "__main__":

    matcher = ProductMatcher()

    query = input(
        "\nEnter product requirement: "
    )

    requirements = extract_requirements(
        query
    )

    print(
        "\nDetected requirements:"
    )

    print(
        requirements
    )

    results = matcher.search(
        query,
        top_k=5
    )

    print(
        "\nTop Matching Products:\n"
    )

    if not results:

        print(
            "No matching products found."
        )

    else:

        for i, product in enumerate(
            results,
            1
        ):

            print(
                f"{i}. "
                f"{product['product_name']}"
            )

            print(
                f"   Match: "
                f"{product['match_score']}%"
            )

            print(
                f"   Category: "
                f"{product['category']}"
            )

            if str(
                product["brand"]
            ).strip():

                print(
                    f"   Brand: "
                    f"{product['brand']}"
                )

            if str(
                product["model"]
            ).strip():

                print(
                    f"   Model: "
                    f"{product['model']}"
                )

            print()
