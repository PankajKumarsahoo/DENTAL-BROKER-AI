
# import json
# import os
# import re
# from collections import defaultdict

# # ==========================================
# # CONFIG
# # ==========================================

# INPUT_FILE = "data/website_pages.json"
# OUTPUT_DIR = "categorized_data"

# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # ==========================================
# # CATEGORY RULES
# # ==========================================

# def categorize_page(url, title, content):

#     url = url.lower()
#     title = title.lower()

#     if "/author/" in url:
#         return "author_profile"

#     if "/label/" in url:
#         return "tag_page"

#     if "/category/" in url:
#         return "category_page"

#     if any(keyword in title for keyword in [
#         "for sale",
#         "jump-start dental office",
#         "dental office building",
#         "under loi",
#         "active",
#         "sold",
#         "practice for sale",
#         "dental office for sale"
#     ]):
#         return "property_listing"

#     if any(keyword in title for keyword in [
#         "buy a dental practice",
#         "buy dental office",
#         "dental practice buyer",
#         "ownership"
#     ]):
#         return "buying_guide"

#     if any(keyword in title for keyword in [
#         "sell your dental practice",
#         "selling dental practice",
#         "sell dental practice"
#     ]):
#         return "selling_guide"

#     if any(keyword in title for keyword in [
#         "transition",
#         "ownership changes",
#         "succession planning"
#     ]):
#         return "transition_guide"

#     if any(keyword in title for keyword in [
#         "broker",
#         "dental office brokers",
#         "sales brokers"
#     ]):
#         return "broker_service"

#     if "pediatric" in title:
#         return "pediatric_dentistry"

#     if "orlando" in title:
#         return "location_guide"

#     if "florida dental office" in title:
#         return "florida_market"

#     if "frequently asked questions" in content.lower():
#         return "faq_article"

#     return "general_blog"


# # ==========================================
# # CONTENT CLEANING
# # ==========================================

# def clean_content(text):

#     junk_patterns = [
#         r"Create a Listing",
#         r"Login Register",
#         r"Favorites 0",
#         r"Compare listings",
#         r"Lost your password",
#         r"Reset Password",
#         r"Notifications",
#         r"Privacy Policy",
#         r"Accessibility Statement",
#         r"Powered by",
#         r"Total Visitor",
#         r"Facebook Linkedin Youtube Instagram"
#     ]

#     for pattern in junk_patterns:
#         text = re.sub(
#             pattern,
#             "",
#             text,
#             flags=re.IGNORECASE
#         )

#     text = re.sub(r"\s+", " ", text)

#     return text.strip()


# # ==========================================
# # METADATA EXTRACTION
# # ==========================================

# def extract_price(text):

#     matches = re.findall(
#         r"\$[\d,]+",
#         text
#     )

#     if matches:
#         return matches[0]

#     return "Unknown"


# def extract_location(title, content):

#     text = title + " " + content

#     locations = [
#         "Miami",
#         "North Miami Beach",
#         "Kendall",
#         "Coral Springs",
#         "Pompano Beach",
#         "Haines City",
#         "Rockledge",
#         "Hallandale Beach",
#         "Orlando",
#         "Florida"
#     ]

#     for location in locations:

#         if location.lower() in text.lower():
#             return location

#     return "Unknown"


# def extract_status(title, content):

#     text = f"{title} {content}".lower()

#     if "under loi" in text:
#         return "Under LOI"

#     if "sold" in text:
#         return "Sold"

#     if "active" in text:
#         return "Active"

#     if "price reduction" in text:
#         return "Price Reduction"

#     return "Unknown"


# def extract_chairs(text):

#     match = re.search(
#         r"(\d+)[-\s]?(chair|chairs|operatory|operatories)",
#         text.lower()
#     )

#     if match:
#         return int(match.group(1))

#     return None


# def extract_collections(text):

#     match = re.search(
#         r"\$([\d,.]+)\s*collections",
#         text.lower()
#     )

#     if match:
#         return "$" + match.group(1)

#     return None


# def extract_property_id(url):

#     match = re.search(
#         r"/property/([^/]+)/",
#         url
#     )

#     if match:
#         return match.group(1)

#     return None


# # ==========================================
# # LOAD DATA
# # ==========================================

# with open(
#     INPUT_FILE,
#     "r",
#     encoding="utf-8"
# ) as f:

#     pages = json.load(f)

# print(f"\nLoaded {len(pages)} pages")


# # ==========================================
# # REMOVE DUPLICATES
# # ==========================================

# seen_urls = set()
# unique_pages = []

# for page in pages:

#     url = page.get("url", "")

#     if url not in seen_urls:

#         unique_pages.append(page)
#         seen_urls.add(url)

# print(
#     f"After duplicate removal: {len(unique_pages)} pages"
# )

# # ==========================================
# # CATEGORIZE
# # ==========================================

# categorized = defaultdict(list)

# for page in unique_pages:

#     url = page.get("url", "")
#     title = page.get("title", "")
#     content = page.get("content", "")

#     cleaned_content = clean_content(content)

#     category = categorize_page(
#         url,
#         title,
#         cleaned_content
#     )

#     price = extract_price(cleaned_content)

#     location = extract_location(
#         title,
#         cleaned_content
#     )

#     status = extract_status(
#         title,
#         cleaned_content
#     )

#     chairs = extract_chairs(
#         title + " " + cleaned_content
#     )

#     collections = extract_collections(
#         cleaned_content
#     )

#     property_id = extract_property_id(url)

#     categorized[category].append({

#         "url": url,

#         "title": title,

#         "content": cleaned_content,

#         "price": price,

#         "location": location,

#         "status": status,

#         "chairs": chairs,

#         "collections": collections,

#         "property_id": property_id
#     })


# # ==========================================
# # SAVE CATEGORY FILES
# # ==========================================

# for category, items in categorized.items():

#     output_file = os.path.join(
#         OUTPUT_DIR,
#         f"{category}.json"
#     )

#     with open(
#         output_file,
#         "w",
#         encoding="utf-8"
#     ) as f:

#         json.dump(
#             items,
#             f,
#             indent=2,
#             ensure_ascii=False
#         )

# # ==========================================
# # SAVE RAG DOCUMENTS
# # ==========================================

# useful_categories = {

#     "property_listing",
#     "buying_guide",
#     "selling_guide",
#     "transition_guide",
#     "broker_service",
#     "location_guide",
#     "pediatric_dentistry",
#     "florida_market",
#     "faq_article",
#     "general_blog"
# }

# useful_docs = []

# for category in useful_categories:

#     useful_docs.extend(
#         categorized.get(category, [])
#     )

# with open(
#     os.path.join(
#         OUTPUT_DIR,
#         "rag_ready_documents.json"
#     ),
#     "w",
#     encoding="utf-8"
# ) as f:

#     json.dump(
#         useful_docs,
#         f,
#         indent=2,
#         ensure_ascii=False
#     )

# # ==========================================
# # SAVE PROPERTY DATASET
# # ==========================================

# properties = []

# for item in categorized.get(
#     "property_listing",
#     []
# ):

#     properties.append({

#         "title": item["title"],

#         "price": item["price"],

#         "location": item["location"],

#         "status": item["status"],

#         "chairs": item["chairs"],

#         "collections": item["collections"],

#         "url": item["url"]
#     })

# with open(
#     os.path.join(
#         OUTPUT_DIR,
#         "properties.json"
#     ),
#     "w",
#     encoding="utf-8"
# ) as f:

#     json.dump(
#         properties,
#         f,
#         indent=2,
#         ensure_ascii=False
#     )

# # ==========================================
# # REPORT
# # ==========================================

# print("\n" + "=" * 60)
# print("CATEGORY REPORT")
# print("=" * 60)

# total_docs = 0

# for category, docs in sorted(
#     categorized.items()
# ):

#     count = len(docs)

#     total_docs += count

#     print(
#         f"{category:25} : {count}"
#     )

# print("=" * 60)
# print(
#     f"TOTAL DOCUMENTS : {total_docs}"
# )

# print("\nFiles saved in:")
# print(OUTPUT_DIR)

# print("\nCreated:")

# for file in os.listdir(
#     OUTPUT_DIR
# ):
#     print(" -", file)

# print("\nRAG Ready File:")
# print(
#     "categorized_data/rag_ready_documents.json"
# )

# print("\nProperty Dataset:")
# print(
#     "categorized_data/properties.json"
# )


def categorize_page(url, title, content):

    url = url.lower()
    title = title.lower()
    content = content.lower()

    # =====================================
    # ARCHIVE PAGES
    # =====================================

    archive_patterns = [
        "/author/",
        "/label/",
        "/tag/",
        "/category/",
        "/status/",
        "/agent/",
    ]

    if any(pattern in url for pattern in archive_patterns):
        return "archive_page"

    # =====================================
    # NAVIGATION / UTILITY PAGES
    # =====================================

    utility_pages = [
        "/favorite-properties/",
        "/submit-property/",
        "/find-a-lawyer/",
        "/find-a-lender/",
        "/practice-assessment-calculator/",
        "/sign-nda/",
        "/sms-privacy-policy/",
        "/sms-terms-of-service/",
        "/privacy-policy/",
        "/contact/",
    ]

    if any(page in url for page in utility_pages):
        return "navigation_page"

    # =====================================
    # PROPERTY LISTINGS
    # =====================================

    if "/property/" in url:
        return "property_listing"

    # =====================================
    # BUYING GUIDES
    # =====================================

    buying_keywords = [
        "buy a dental practice",
        "buy dental office",
        "dental practice buyer",
        "buyers guide",
        "ownership",
        "purchase a dental practice",
        "find a dental practice",
    ]

    if any(keyword in title for keyword in buying_keywords):
        return "buying_guide"

    # =====================================
    # SELLING GUIDES
    # =====================================

    selling_keywords = [
        "sell your dental practice",
        "selling dental practice",
        "sell dental practice",
        "practice sale",
        "sell dental office",
        "maximize value",
    ]

    if any(keyword in title for keyword in selling_keywords):
        return "selling_guide"

    # =====================================
    # TRANSITION GUIDES
    # =====================================

    transition_keywords = [
        "transition",
        "ownership changes",
        "succession planning",
        "practice transition",
        "transition dental practice",
    ]

    if any(keyword in title for keyword in transition_keywords):
        return "transition_guide"

    # =====================================
    # BROKER SERVICES
    # =====================================

    broker_keywords = [
        "broker",
        "dental office brokers",
        "sales brokers",
        "broker price opinion",
        "broker services",
    ]

    if any(keyword in title for keyword in broker_keywords):
        return "broker_service"

    # =====================================
    # LOCATION GUIDES
    # =====================================

    location_keywords = [
        "orlando",
        "miami",
        "south florida",
        "florida dental office",
        "boynton beach",
        "coral springs",
        "pompano beach",
        "hallandale",
        "kendall",
    ]

    if any(keyword in title for keyword in location_keywords):
        return "location_guide"

    # =====================================
    # FAQ ARTICLES
    # =====================================

    faq_keywords = [
        "frequently asked questions",
        "faq",
        "questions and answers",
    ]

    if any(keyword in content for keyword in faq_keywords):
        return "faq_article"

    # =====================================
    # BLOG ARTICLES
    # =====================================

    return "general_blog"