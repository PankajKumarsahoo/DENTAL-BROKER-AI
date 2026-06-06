# # import os
# # from dotenv import load_dotenv

# # from langchain_google_genai import ChatGoogleGenerativeAI

# # from retriever import retriever

# # load_dotenv()

# # print("KEY =", repr(os.getenv("GOOGLE_API_KEY")))

# # llm = ChatGoogleGenerativeAI(
# #     model="gemini-3.1-flash-lite",
# #     temperature=0.3,
# #     google_api_key=os.getenv("GOOGLE_API_KEY")
# # )

# # llm = ChatGoogleGenerativeAI(
# #     model="gemini-3.1-flash-lite",
# #     temperature=0.3,
# #     google_api_key=os.getenv("GOOGLE_API_KEY")
# # )


# # def ask_question(question):

# #     docs = retriever.invoke(question)

# #     context = "\n\n".join(
# #         [doc.page_content for doc in docs]
# #     )

# #     prompt = f"""
# # You are Dental Broker Florida AI Assistant.

# # Answer ONLY using the provided context.

# # If the answer is not found,
# # say:
# # "I could not find that information in the database."

# # Context:
# # {context}

# # Question:
# # {question}

# # Answer:
# # """

# #     response = llm.invoke(prompt)

# #     return response.content


# # if __name__ == "__main__":

# #     while True:

# #         question = input("\nAsk: ")

# #         if question.lower() == "exit":
# #             break

# #         answer = ask_question(question)

# #         print("\nAnswer:")
# #         print(answer)


# #################################################################################
# import os
# from dotenv import load_dotenv

# from langchain_google_genai import ChatGoogleGenerativeAI

# from retriever import retriever

# # ==========================================
# # LOAD ENV
# # ==========================================

# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# print("\n===================================")
# print("GOOGLE API KEY CHECK")
# print("===================================")

# if GOOGLE_API_KEY:
#     print("Key Loaded Successfully")
#     print("Key Starts With:", GOOGLE_API_KEY[:6])
#     print("Key Length:", len(GOOGLE_API_KEY))
# else:
#     print("ERROR: GOOGLE_API_KEY not found!")
#     exit()

# # ==========================================
# # GEMINI MODEL
# # ==========================================

# try:
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-3.1-flash-lite",
#         temperature=0.3,
#         google_api_key=GOOGLE_API_KEY
#     )

#     print("Gemini Model Loaded Successfully\n")

# except Exception as e:
#     print("Failed to initialize Gemini")
#     print(e)
#     exit()


# # ==========================================
# # QUESTION ANSWERING
# # ==========================================

# def ask_question(question):

#     try:

#         docs = retriever.invoke(question)

#         if not docs:
#             return "No relevant information found."

#         context = "\n\n".join(
#             [doc.page_content for doc in docs]
#         )

#         prompt = f"""
# You are Dental Broker Florida AI Assistant.

# Use ONLY the information provided in the context.

# Rules:
# 1. Do not make up information.
# 2. If answer is not present, say:
#    "I could not find that information in the database."
# 3. Give concise and professional answers.

# CONTEXT:
# {context}

# QUESTION:
# {question}

# ANSWER:
# """

#         response = llm.invoke(prompt)

#         return response.content

#     except Exception as e:

#         return f"""
# ERROR DURING GENERATION

# {str(e)}
# """


# # ==========================================
# # CHAT LOOP
# # ==========================================

# if __name__ == "__main__":

#     print("=" * 60)
#     print("Dental Broker Florida AI Assistant")
#     print("Type 'exit' to quit")
#     print("=" * 60)

#     while True:

#         question = input("\nAsk: ")

#         if question.lower() in ["exit", "quit"]:
#             break

#         answer = ask_question(question)

#         print("\nAnswer:")
#         print(answer)
#         print("-" * 60)
#------------------------------------------------------------------------------


import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from rag.retriever import retriever

# =====================================
# LOAD ENVIRONMENT VARIABLES
# =====================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in .env file."
    )

print("\n===================================")
print("Dental Broker Florida AI Assistant")
print("Using Groq + Chroma RAG")
print("===================================")

# =====================================
# LOAD LLM
# =====================================

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0.2,
)

# =====================================
# CHAT MEMORY
# =====================================

chat_history = []

MAX_HISTORY = 6

# =====================================
# ASK QUESTION
# =====================================

def ask_question(question):

    global chat_history

    try:

        # Retrieve documents

        docs = retriever.invoke(question)

        if not docs:
            return "I could not find that information in the database."

        # Build context

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        # Previous history

        history_text = "\n".join(
            chat_history[-MAX_HISTORY:]
        )

        # Prompt

        prompt = f"""
You are Dental Broker Florida AI Assistant.

Answer ONLY using the provided database context.

RULES:

1. Never make up information.

2. Use ONLY the provided context.

3. If the answer does not exist, say:

"I could not find that information in the database."

4. Property questions should include:
- Property Name
- Price
- Location

5. Be concise and professional.

CHAT HISTORY:
{history_text}

DATABASE CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

        # Generate response

        response = llm.invoke(prompt)

        answer = response.content.strip()

        # Save memory

        chat_history.append(
            f"User: {question}"
        )

        chat_history.append(
            f"Assistant: {answer}"
        )

        # Keep memory small

        if len(chat_history) > 20:
            chat_history = chat_history[-20:]

        # Return answer only

        return answer

    except Exception as e:

        return f"Error: {str(e)}"

# =====================================
# CLEAR MEMORY
# =====================================

def clear_memory():

    global chat_history

    chat_history = []

    print("Chat memory cleared.")

# =====================================
# TEST MODE
# =====================================

if __name__ == "__main__":

    print("=" * 60)
    print("Dental Broker Florida AI")
    print("=" * 60)

    print("Commands:")
    print("exit")
    print("clear")

    while True:

        question = input("\nAsk: ").strip()

        if not question:
            continue

        if question.lower() == "exit":
            break

        if question.lower() == "clear":
            clear_memory()
            continue

        answer = ask_question(question)

        print("\nAnswer:\n")
        print(answer)

        print("\n" + "=" * 60)
