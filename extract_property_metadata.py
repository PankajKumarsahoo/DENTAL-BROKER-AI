# import json
# import re
# import os

# # ==========================================
# # CONFIG
# # ==========================================

# INPUT_FILE = "categorized_data/property_listing.json"
# OUTPUT_FILE = "data/property_metadata.json"

# os.makedirs("data", exist_ok=True)

# # ==========================================
# # HELPERS
# # ==========================================

# def extract_price(text):
#     """
#     Extract price like:
#     $450,000
#     $1,400,000
#     """

#     match = re.search(r"\$([\d,]+)", text)

#     if match:
#         return int(match.group(1).replace(",", ""))

#     return None


# def extract_chairs(text):
#     """
#     Extract:
#     5 Chairs
#     7-Chair
#     12 Chairs
#     """

#     patterns = [
#         r"(\d+)\s*chairs?",
#         r"(\d+)-chair",
#         r"(\d+)\s*chair"
#     ]

#     text = text.lower()

#     for pattern in patterns:
#         match = re.search(pattern, text)

#         if match:
#             return int(match.group(1))

#     return None


# def extract_operatories(text):
#     """
#     Extract:
#     12 Operatory
#     12-Operatory
#     5 Operatories
#     """

#     patterns = [
#         r"(\d+)\s*operatory",
#         r"(\d+)-operatory",
#         r"(\d+)\s*operatories"
#     ]

#     text = text.lower()

#     for pattern in patterns:
#         match = re.search(pattern, text)

#         if match:
#             return int(match.group(1))

#     return None


# def extract_status(text):

#     text = text.lower()

#     if "under loi" in text:
#         return "under_loi"

#     if "sold" in text:
#         return "sold"

#     if "active" in text:
#         return "active"

#     if "price reduction" in text:
#         return "active"

#     return "unknown"


# def extract_city(title, content):

#     florida_cities = [
#         "Miami",
#         "Kendall",
#         "Coral Springs",
#         "Rockledge",
#         "Haines City",
#         "Hallandale Beach",
#         "Pompano Beach",
#         "Orlando",
#         "West Palm Beach",
#         "Boynton Beach",
#         "North Miami Beach",
#         "Merritt Island"
#     ]

#     combined = f"{title} {content}"

#     for city in florida_cities:

#         if city.lower() in combined.lower():
#             return city

#     return None


# # ==========================================
# # LOAD PROPERTY DATA
# # ==========================================

# print("\nLoading Property Listings...")

# with open(INPUT_FILE, "r", encoding="utf-8") as f:
#     properties = json.load(f)

# print(f"Found {len(properties)} property listings")

# # ==========================================
# # EXTRACT METADATA
# # ==========================================

# metadata = []

# for item in properties:

#     title = item.get("title", "")
#     content = item.get("content", "")
#     url = item.get("url", "")

#     full_text = f"{title}\n{content}"

#     property_data = {
#         "title": title,
#         "url": url,
#         "city": extract_city(title, content),
#         "price": extract_price(full_text),
#         "chairs": extract_chairs(full_text),
#         "operatories": extract_operatories(full_text),
#         "status": extract_status(full_text)
#     }

#     metadata.append(property_data)

# # ==========================================
# # SAVE
# # ==========================================

# with open(
#     OUTPUT_FILE,
#     "w",
#     encoding="utf-8"
# ) as f:

#     json.dump(
#         metadata,
#         f,
#         indent=2,
#         ensure_ascii=False
#     )

# # ==========================================
# # REPORT
# # ==========================================

# print("\n" + "=" * 60)
# print("PROPERTY METADATA EXTRACTION COMPLETE")
# print("=" * 60)

# print(f"Properties Processed : {len(metadata)}")
# print(f"Saved To            : {OUTPUT_FILE}")

# print("\nSample Records:\n")

# for item in metadata[:5]:

#     print("-" * 50)
#     print("Title       :", item["title"])
#     print("City        :", item["city"])
#     print("Price       :", item["price"])
#     print("Chairs      :", item["chairs"])
#     print("Operatories :", item["operatories"])
#     print("Status      :", item["status"])

# print("\nDone!")




#######################333
import json
import re
import os

# ==========================================
# CONFIG
# ==========================================

INPUT_FILE = "categorized_data/property_listing.json"
OUTPUT_FILE = "data/property_metadata.json"

os.makedirs("data", exist_ok=True)


# ==========================================
# HELPERS
# ==========================================
def extract_price(text):

    text = text.lower()

    price_patterns = [

        r"price\s*\$([\d,]+)",
        r"asking price\s*\$([\d,]+)",
        r"\$([\d,]+)\s*featured",
        r"\$([\d,]+)\s*active",
        r"\$([\d,]+)\s*under loi",
        r"\$([\d,]+)\s*sold",
    ]

    for pattern in price_patterns:

        match = re.search(pattern, text)

        if match:

            try:
                return int(
                    match.group(1).replace(",", "")
                )
            except:
                pass

    prices = re.findall(r"\$([\d,]+)", text)

    valid = []

    for p in prices:

        try:

            value = int(
                p.replace(",", "")
            )

            if 50000 <= value <= 3000000:
                valid.append(value)

        except:
            pass

    if valid:
        return min(valid)

    return None


def extract_chairs(text):

    text = text.lower()

    patterns = [

        r"(\d+)-chair",
        r"(\d+)\s*chair",
        r"(\d+)\s*chairs",
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            return int(match.group(1))

    return None


def extract_operatories(text):
    patterns = [
        r"(\d+)\s*operatory",
        r"(\d+)-operatory",
        r"(\d+)\s*operatories",
        r"(\d+)-operatories",
        r"(\d+)\s*ops",
    ]

    text = text.lower()

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return int(match.group(1))

    return None


def extract_status(title, content):

    text = f"{title}\n{content}".lower()

    # Highest priority

    if re.search(r"\bunder loi\b", text):
        return "under_loi"

    if re.search(r"\bprice reduction\b", text):
        return "price_reduction"

    if re.search(r"\bactive\b", text):
        return "active"

    if re.search(r"\bsold\b", text):
        return "sold"

    return "unknown"


def extract_city(title, content):
    florida_cities = [
        "Miami",
        "North Miami Beach",
        "Kendall",
        "Coral Springs",
        "Rockledge",
        "Haines City",
        "Hallandale Beach",
        "Pompano Beach",
        "Orlando",
        "West Palm Beach",
        "Boynton Beach",
        "Merritt Island",
        "Fort Lauderdale",
        "Boca Raton",
        "Tampa",
        "Naples",
        "Jacksonville",
        "Melbourne",
        "Palm Bay"
    ]

    combined = f"{title} {content}"

    for city in florida_cities:
        if city.lower() in combined.lower():
            return city

    return None


# ==========================================
# LOAD PROPERTY DATA
# ==========================================

print("\nLoading Property Listings...")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    properties = json.load(f)

print(f"Found {len(properties)} property listings")


# ==========================================
# EXTRACT METADATA
# ==========================================

metadata = []

bad_titles = [
    "active archives",
    "sold listings",
    "under loi archives",
    "favorite properties",
    "dental office for sale | dental office 4 sale",
]

for item in properties:
    title = item.get("title", "")
    content = item.get("content", "")
    url = item.get("url", "")

    title_lower = title.lower()

    # ======================================
    # SKIP BAD PAGES
    # ======================================
    if any(bad_title in title_lower for bad_title in bad_titles):
        continue

    full_text = f"{title}\n{content}"

    property_data = {
        "title": title,
        "url": url,
        "city": extract_city(title, content),
        "price": extract_price(full_text),
        "chairs": extract_chairs(full_text),
        "operatories": extract_operatories(full_text),
        "status": extract_status(title, content)
    }

    metadata.append(property_data)


# ==========================================
# SAVE
# ==========================================

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)


# ==========================================
# REPORT
# ==========================================

print("\n" + "=" * 60)
print("PROPERTY METADATA EXTRACTION COMPLETE")
print("=" * 60)

print(f"Properties Processed : {len(metadata)}")
print(f"Saved To             : {OUTPUT_FILE}")

print("\nSample Records:\n")

for item in metadata[:10]:
    print("-" * 50)
    print("Title       :", item["title"])
    print("City        :", item["city"])
    print("Price       :", item["price"])
    print("Chairs      :", item["chairs"])
    print("Operatories :", item["operatories"])
    print("Status      :", item["status"])

print("\nDone!")