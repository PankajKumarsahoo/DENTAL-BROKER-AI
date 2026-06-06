# import streamlit as st
# import json
# import pandas as pd
# import sys
# import os

# sys.path.append(os.path.abspath("."))

# from rag.chatbot import ask_question

# # ==========================================
# # PAGE CONFIG
# # ==========================================

# st.set_page_config(
#     page_title="Dental Broker Florida AI",
#     page_icon="🦷",
#     layout="wide"
# )

# # ==========================================
# # CUSTOM CSS
# # ==========================================

# st.markdown("""
# <style>

# @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

# html, body, [class*="css"]{
#     font-family: 'Poppins', sans-serif;
# }

# .stApp{
#     background-color:#0f1117;
# }

# .hero{
#     text-align:center;
#     padding:40px;
#     border-radius:20px;
#     background: linear-gradient(
#         135deg,
#         #111827,
#         #1f2937
#     );
#     border:1px solid #D4AF6A;
#     margin-bottom:20px;
# }

# .hero h1{
#     color:#D4AF6A;
#     font-size:48px;
# }

# .hero p{
#     color:white;
#     font-size:20px;
# }

# .property-card{
#     background:#1a1d25;
#     padding:20px;
#     border-radius:15px;
#     border:1px solid #D4AF6A;
#     margin-bottom:15px;
#     transition:0.3s;
# }

# .property-card:hover{
#     transform:scale(1.02);
# }

# .price{
#     color:#D4AF6A;
#     font-size:28px;
#     font-weight:bold;
# }

# .chat-box{
#     background:#111827;
#     border:1px solid #D4AF6A;
#     padding:20px;
#     border-radius:15px;
# }

# .source-box{
#     background:#1f2937;
#     padding:10px;
#     border-radius:10px;
# }

# </style>
# """, unsafe_allow_html=True)

# # ==========================================
# # HERO SECTION
# # ==========================================

# st.markdown("""
# <div class="hero">
# <h1>🦷 Dental Broker Florida AI</h1>
# <p>
# Find Dental Practices • Search Listings • Ask Questions
# </p>
# </div>
# """, unsafe_allow_html=True)

# # ==========================================
# # SIDEBAR
# # ==========================================

# st.sidebar.image(
#     "https://cdn-icons-png.flaticon.com/512/3004/3004458.png",
#     width=120
# )

# st.sidebar.title("Navigation")

# page = st.sidebar.radio(
#     "Select",
#     [
#         "AI Assistant",
#         "Property Search",
#         "Analytics"
#     ]
# )

# # ==========================================
# # LOAD PROPERTY DATA
# # ==========================================

# @st.cache_data
# def load_properties():

#     with open(
#         "data/property_metadata.json",
#         "r",
#         encoding="utf-8"
#     ) as f:

#         return json.load(f)

# properties = load_properties()

# # ==========================================
# # AI ASSISTANT
# # ==========================================

# if page == "AI Assistant":

#     st.subheader("💬 Ask Anything")

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     question = st.chat_input(
#         "Ask about dental offices..."
#     )

#     if question:

#         st.session_state.messages.append(
#             {"role":"user","content":question}
#         )

#         answer = ask_question(question)

#         st.session_state.messages.append(
#             {"role":"assistant","content":answer}
#         )

#     for msg in st.session_state.messages:

#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])

# # ==========================================
# # PROPERTY SEARCH
# # ==========================================

# elif page == "Property Search":

#     st.subheader("🏢 Property Listings")

#     city = st.selectbox(
#         "City",
#         ["All"] + sorted(
#             list(
#                 set(
#                     p["city"]
#                     for p in properties
#                     if p["city"]
#                 )
#             )
#         )
#     )

#     max_price = st.slider(
#         "Maximum Price",
#         0,
#         2000000,
#         500000
#     )

#     filtered = []

#     for p in properties:

#         price = p.get("price")

#         if price is None:
#             continue

#         if city != "All":

#             if p["city"] != city:
#                 continue

#         if price > max_price:
#             continue

#         filtered.append(p)

#     st.write(
#         f"Found {len(filtered)} properties"
#     )

#     for p in filtered:

#         st.markdown(f"""
#         <div class="property-card">

#         <h3>{p['title']}</h3>

#         <div class="price">
#         ${p['price']:,}
#         </div>

#         📍 {p['city']} <br>

#         🪑 Chairs: {p['chairs']} <br>

#         📊 Status: {p['status']}

#         </div>
#         """, unsafe_allow_html=True)

# # ==========================================
# # ANALYTICS
# # ==========================================

# elif page == "Analytics":

#     st.subheader("📈 Property Analytics")

#     df = pd.DataFrame(properties)

#     st.dataframe(df)

#     st.metric(
#         "Total Properties",
#         len(df)
#     )

#     prices = df["price"].dropna()

#     if len(prices):

#         st.metric(
#             "Average Price",
#             f"${int(prices.mean()):,}"
#         )

#         st.metric(
#             "Maximum Price",
#             f"${int(prices.max()):,}"
#         )

#         st.metric(
#             "Minimum Price",
#             f"${int(prices.min()):,}"
#         )

#####################################################################
import streamlit as st
import pandas as pd
import json
import time
import os
import sys

sys.path.append(os.path.abspath("."))

from rag.chatbot import ask_question

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Dental Broker Florida AI",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]{
    font-family:'Poppins',sans-serif;
}

.stApp{
    background:#0f1117;
}

section[data-testid="stSidebar"]{
    background:#151922;
}

.hero{
    padding:35px;
    border-radius:20px;
    background:linear-gradient(
    135deg,
    #111827,
    #1f2937);

    border:2px solid #D4AF6A;
    text-align:center;
    margin-bottom:20px;
}

.hero h1{
    color:#D4AF6A;
    font-size:50px;
}

.hero p{
    color:white;
    font-size:20px;
}

.smallcard{

    background:#1f2937;

    padding:15px;

    border-radius:15px;

    border:1px solid #D4AF6A;

    margin-bottom:10px;

}

.property-card{

    background:#1a1d25;

    padding:20px;

    border-radius:15px;

    border:1px solid #D4AF6A;

    margin-bottom:15px;

}

.price{

    color:#D4AF6A;

    font-size:30px;

    font-weight:bold;

}

.footer{

    text-align:center;

    color:gray;

    margin-top:50px;

}

</style>
""",unsafe_allow_html=True)

# =====================================================
# SESSION
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages=[]

if "questions" not in st.session_state:
    st.session_state.questions=0

if "responses" not in st.session_state:
    st.session_state.responses=0

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_properties():

    with open(
        "data/property_metadata.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

properties=load_properties()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.markdown("# 🦷 Dental Broker Florida AI")

st.sidebar.markdown("━━━━━━━━━━━━━━━━━━━")

page=st.sidebar.radio(

    "🏠 Navigation",

    [

        "AI Assistant",

        "Property Search",

        "Analytics"

    ]

)

st.sidebar.markdown("━━━━━━━━━━━━━━━━━━━")

st.sidebar.subheader("💬 Chat Controls")

if st.sidebar.button(
    "🗑️ Clear Chat",
    use_container_width=True
):

    st.session_state.messages=[]

    st.session_state.questions=0

    st.session_state.responses=0

    st.rerun()

if st.sidebar.button(
    "🔄 Reset Session",
    use_container_width=True
):

    st.cache_data.clear()

    st.session_state.messages=[]

    st.session_state.questions=0

    st.session_state.responses=0

    st.rerun()

st.sidebar.markdown("━━━━━━━━━━━━━━━━━━━")

st.sidebar.subheader("📊 Session")

st.sidebar.metric(

    "Questions Asked",

    st.session_state.questions

)

st.sidebar.metric(

    "Responses",

    st.session_state.responses

)

st.sidebar.markdown("━━━━━━━━━━━━━━━━━━━")

st.sidebar.subheader("💡 Suggested Questions")

st.sidebar.write("• Show active offices")

st.sidebar.write("• Offices under $500000")

st.sidebar.write("• Cheapest practice")

st.sidebar.write("• Find CBCT offices")

st.sidebar.write("• Buy a dental practice")

st.sidebar.write("• Sell my dental practice")

st.sidebar.write("• Transition practices")

st.sidebar.write("• Under LOI meaning")

st.sidebar.markdown("━━━━━━━━━━━━━━━━━━━")

st.sidebar.success(
"""
🦷 Powered By

• Groq

• LangChain

• ChromaDB

• Sentence Transformers
"""
)

# =====================================================
# HERO
# =====================================================

st.markdown("""

<div class="hero">

<h1>🦷 Dental Broker Florida AI</h1>

<p>

Florida's Intelligent Dental Practice Marketplace

</p>

<p>

✔ AI Assistant

✔ Property Search

✔ Analytics

✔ Practice Buying

✔ Practice Selling

</p>

</div>

""",unsafe_allow_html=True)

# =====================================================
# WELCOME
# =====================================================

if len(st.session_state.messages)==0:

    st.info("""

👋 Welcome!

You can ask me about:

🏢 Dental offices for sale

📍 Florida locations

💰 Property prices

🪑 Chair counts

📋 Transition practices

🦷 Buying a practice

🦷 Selling a practice

📞 Dental Broker Florida services

""")
# =====================================================
# AI ASSISTANT
# =====================================================

if page == "AI Assistant":

    st.header("💬 AI Dental Assistant")

    col1, col2 = st.columns([3,1])

    with col1:
        st.write(
            "Ask anything about Dental Broker Florida."
        )

    with col2:

        chat_text=""

        for m in st.session_state.messages:

            chat_text += (
                f"{m['role'].upper()}:\n"
                f"{m['content']}\n\n"
            )

        st.download_button(

            label="📄 Download Chat",

            data=chat_text,

            file_name="chat_history.txt",

            mime="text/plain"

        )

    st.markdown("---")

    st.subheader("⚡ Quick Questions")

    c1,c2,c3=st.columns(3)

    quick_question=None

    with c1:

        if st.button(
            "🏢 Active Offices",
            use_container_width=True
        ):
            quick_question="Show active dental offices."

        if st.button(
            "💰 Under $500k",
            use_container_width=True
        ):
            quick_question="Dental offices under $500000."

    with c2:

        if st.button(
            "🦷 CBCT Offices",
            use_container_width=True
        ):
            quick_question="Find offices with CBCT equipment."

        if st.button(
            "🏷 Cheapest Office",
            use_container_width=True
        ):
            quick_question="What is the cheapest dental office available?"

    with c3:

        if st.button(
            "📋 Sell Practice",
            use_container_width=True
        ):
            quick_question="How can I sell my dental practice?"

        if st.button(
            "🛒 Buy Practice",
            use_container_width=True
        ):
            quick_question="How do I buy a dental practice?"

    st.markdown("---")

    question = st.chat_input(
        "Ask about dental practices..."
    )

    if quick_question:
        question=quick_question

    if question:

        st.session_state.questions += 1

        st.session_state.messages.append({

            "role":"user",

            "content":question

        })

        with st.chat_message("user"):

            st.markdown(question)

        with st.chat_message("assistant"):

            progress=st.progress(0)

            status=st.empty()

            status.info(
                "🔍 Searching knowledge base..."
            )

            progress.progress(20)

            time.sleep(0.3)

            status.info(
                "📚 Reading property listings..."
            )

            progress.progress(50)

            time.sleep(0.3)

            status.info(
                "🦷 Understanding your question..."
            )

            progress.progress(75)

            time.sleep(0.3)

            status.info(
                "🤖 Generating response..."
            )

            progress.progress(95)

            start=time.time()

            try:

                answer=ask_question(question)

            except Exception as e:

                answer=(
                    "⚠ Sorry, an error occurred.\n\n"
                    f"{str(e)}"
                )

            end=time.time()

            progress.progress(100)

            time.sleep(0.2)

            progress.empty()

            status.success("✅ Done")

            st.markdown("### 🤖 Dental Broker AI")

            st.write(answer)

            st.caption(
                f"⏱ Response Time: "
                f"{end-start:.2f} sec"
            )

        st.session_state.responses += 1

        st.session_state.messages.append({

            "role":"assistant",

            "content":answer

        })

    st.markdown("---")

    st.subheader("💬 Conversation History")

    if len(st.session_state.messages)==0:

        st.info(
            "Start asking questions!"
        )

    else:

        for message in st.session_state.messages:

            with st.chat_message(
                message["role"]
            ):

                st.write(
                    message["content"]
                )

    st.markdown("---")

    with st.expander(
        "💡 Example Questions"
    ):

        st.write(
            """
• Show active dental offices.

• Dental offices under $500000.

• What is the cheapest office?

• Find offices with CBCT.

• Show transition practices.

• What does Under LOI mean?

• Show South Florida offices.

• Find offices with 5 chairs.

• How can I sell my practice?

• How do I buy a practice?

• What services does Dental Broker Florida offer?

• Show price reduction properties.

• Find Miami offices.

• Show active offices with CBCT.

• Compare transition and jump-start offices.
"""
        )
# =====================================================
# PROPERTY SEARCH
# =====================================================

elif page == "Property Search":

    st.header("🏢 Dental Property Explorer")

    st.write(
        "Search Florida dental offices and practices."
    )

    st.markdown("---")

    # ==========================
    # FILTERS
    # ==========================

    col1,col2=st.columns(2)

    with col1:

        cities=sorted(
            list(
                set(
                    p["city"]
                    for p in properties
                    if p["city"]
                )
            )
        )

        city=st.selectbox(

            "📍 City",

            ["All"]+cities

        )

    with col2:

        statuses=sorted(
            list(
                set(
                    p["status"]
                    for p in properties
                    if p["status"]
                )
            )
        )

        status=st.selectbox(

            "📊 Status",

            ["All"]+statuses

        )

    col1,col2=st.columns(2)

    with col1:

        max_price=st.slider(

            "💰 Maximum Price",

            0,

            2000000,

            500000,

            50000

        )

    with col2:

        min_chairs=st.slider(

            "🪑 Minimum Chairs",

            0,

            15,

            0

        )

    search_text=st.text_input(

        "🔎 Search Property",

        placeholder="Miami, CBCT, Transition..."

    )

    sort_option=st.selectbox(

        "📋 Sort By",

        [

            "Price Low to High",

            "Price High to Low",

            "Alphabetical"

        ]

    )

    st.markdown("---")

    # ==========================
    # FILTER DATA
    # ==========================

    filtered=[]

    for p in properties:

        price=p.get("price")

        chairs=p.get("chairs")

        title=p.get("title","")

        p_city=p.get("city")

        p_status=p.get("status")

        if city!="All":

            if p_city!=city:

                continue

        if status!="All":

            if p_status!=status:

                continue

        if price:

            if price>max_price:

                continue

        if chairs:

            if chairs<min_chairs:

                continue

        if search_text:

            if search_text.lower() not in title.lower():

                continue

        filtered.append(p)

    # ==========================
    # SORT
    # ==========================

    if sort_option=="Price Low to High":

        filtered=sorted(

            filtered,

            key=lambda x:

            x["price"]

            if x["price"]

            else 999999999

        )

    elif sort_option=="Price High to Low":

        filtered=sorted(

            filtered,

            key=lambda x:

            x["price"]

            if x["price"]

            else 0,

            reverse=True

        )

    else:

        filtered=sorted(

            filtered,

            key=lambda x:

            x["title"]

        )

    # ==========================
    # SUMMARY
    # ==========================

    c1,c2,c3=st.columns(3)

    c1.metric(

        "Properties Found",

        len(filtered)

    )

    prices=[

        p["price"]

        for p in filtered

        if p["price"]

    ]

    if prices:

        c2.metric(

            "Average Price",

            f"${int(sum(prices)/len(prices)):,}"

        )

        c3.metric(

            "Cheapest",

            f"${min(prices):,}"

        )

    st.markdown("---")

    # ==========================
    # PROPERTY CARDS
    # ==========================

    if len(filtered)==0:

        st.warning(

            "No matching properties found."

        )

    else:

        for p in filtered:

            price_text="N/A"

            if p["price"]:

                price_text=f"${p['price']:,}"

            chairs_text="N/A"

            if p["chairs"]:

                chairs_text=str(p["chairs"])

            status_text=p["status"]

            city_text=p["city"]

            st.markdown(f"""

<div class="property-card">

<h3>

🏢 {p['title']}

</h3>

<div class="price">

{price_text}

</div>

📍 <b>City:</b> {city_text}

<br>

🪑 <b>Chairs:</b> {chairs_text}

<br>

📊 <b>Status:</b> {status_text}

</div>

""",

unsafe_allow_html=True

)

            with st.expander(

                "📋 View Details"

            ):

                st.write(

                    "**Property Title:**",

                    p["title"]

                )

                st.write(

                    "**City:**",

                    city_text

                )

                st.write(

                    "**Price:**",

                    price_text

                )

                st.write(

                    "**Chairs:**",

                    chairs_text

                )

                st.write(

                    "**Status:**",

                    status_text

                )

                if p["url"]:

                    st.markdown(

                        f"[🌐 View Property]({p['url']})"

                    )

    st.markdown("---")

    st.success(

        f"Showing {len(filtered)} properties."

    )        
# =====================================================
# ANALYTICS
# =====================================================

elif page == "Analytics":

    st.header("📊 Dental Market Analytics")

    st.write(
        "Florida Dental Practice Market Insights"
    )

    st.markdown("---")

    df = pd.DataFrame(properties)

    # ==========================
    # CLEAN DATA
    # ==========================

    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    df["chairs"] = pd.to_numeric(
        df["chairs"],
        errors="coerce"
    )

    # ==========================
    # KPI
    # ==========================

    total_properties = len(df)

    active_count = len(
        df[
            df["status"]=="active"
        ]
    )

    loi_count = len(
        df[
            df["status"]=="under_loi"
        ]
    )

    avg_price = int(
        df["price"].dropna().mean()
    ) if len(df["price"].dropna()) else 0

    max_price = int(
        df["price"].dropna().max()
    ) if len(df["price"].dropna()) else 0

    min_price = int(
        df["price"].dropna().min()
    ) if len(df["price"].dropna()) else 0

    col1,col2,col3=st.columns(3)

    col1.metric(
        "🏢 Total",
        total_properties
    )

    col2.metric(
        "🟢 Active",
        active_count
    )

    col3.metric(
        "🟡 Under LOI",
        loi_count
    )

    col1,col2,col3=st.columns(3)

    col1.metric(
        "💰 Average",
        f"${avg_price:,}"
    )

    col2.metric(
        "📈 Highest",
        f"${max_price:,}"
    )

    col3.metric(
        "📉 Lowest",
        f"${min_price:,}"
    )

    st.markdown("---")

    # ==========================
    # PRICE DISTRIBUTION
    # ==========================

    st.subheader(
        "💰 Property Prices"
    )

    price_df=df[
        df["price"].notna()
    ]

    if len(price_df):

        st.bar_chart(
            price_df["price"]
        )

    # ==========================
    # STATUS
    # ==========================

    st.subheader(
        "📊 Listing Status"
    )

    status_counts=df[
        "status"
    ].value_counts()

    st.bar_chart(
        status_counts
    )

    # ==========================
    # CITIES
    # ==========================

    st.subheader(
        "🏙️ Listings by City"
    )

    city_counts=df[
        "city"
    ].value_counts()

    st.bar_chart(
        city_counts
    )

    # ==========================
    # CHAIRS
    # ==========================

    st.subheader(
        "🪑 Chair Distribution"
    )

    chair_df=df[
        df["chairs"].notna()
    ]

    if len(chair_df):

        st.bar_chart(
            chair_df["chairs"]
        )

    st.markdown("---")

    # ==========================
    # MARKET INSIGHTS
    # ==========================

    st.subheader(
        "📋 Market Summary"
    )

    if len(city_counts):

        top_city=city_counts.idxmax()

    else:

        top_city="Unknown"

    expensive=df.loc[
        df["price"].idxmax()
    ] if len(price_df) else None

    cheap=df.loc[
        df["price"].idxmin()
    ] if len(price_df) else None

    st.success(f"""

🏢 Total Listings : {total_properties}

📍 Top City : {top_city}

💰 Average Price : ${avg_price:,}

🟢 Active Listings : {active_count}

🟡 Under LOI : {loi_count}

""")

    if expensive is not None:

        st.info(f"""

🏆 Most Expensive Property

{expensive['title']}

Price : ${int(expensive['price']):,}

Location : {expensive['city']}

""")

    if cheap is not None:

        st.info(f"""

💵 Cheapest Property

{cheap['title']}

Price : ${int(cheap['price']):,}

Location : {cheap['city']}

""")

    st.markdown("---")

    # ==========================
    # TABLE
    # ==========================

    st.subheader(
        "📄 Property Dataset"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.download_button(

        label="📥 Download Dataset",

        data=df.to_csv(
            index=False
        ),

        file_name="property_data.csv",

        mime="text/csv"

    )