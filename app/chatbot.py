KNOWLEDGE_BASE = {
    "shipping_time": "Standard shipping takes 5-7 business days.",

    "returns": (
        "Items can be returned within 30 days of delivery "
        "as long as they are unused and in their original packaging."
    ),

    "refund": (
        "Refunds are processed within 5 business days "
        "after the returned item is received."
    ),

    "password": (
        "Click 'Forgot Password' on the login page "
        "and follow the instructions sent to your email."
    ),

    "cancel": (
        "Orders can be cancelled before they are shipped. "
        "Contact customer support as soon as possible."
    ),

    "international": (
        "ShopEasy currently ships only within the United States."
    )
}


def chatbot(question):
    question = question.lower()

    if "shipping" in question and "long" in question:
        return KNOWLEDGE_BASE["shipping_time"]

    if "return" in question:
        return KNOWLEDGE_BASE["returns"]

    if "refund" in question:
        return KNOWLEDGE_BASE["refund"]

    if "password" in question:
        return KNOWLEDGE_BASE["password"]

    if "cancel" in question:
        return KNOWLEDGE_BASE["cancel"]

    if "international" in question:
        return KNOWLEDGE_BASE["international"]

    return "I'm sorry, I don't have enough information to answer that question."


if __name__ == "__main__":
    question = input("Customer: ")
    answer = chatbot(question)

    print("ShopEasy Bot:", answer)