# Chatbot functions here
def get_response(user_input: str, conn):
    user_input = user_input.lower()
    if "expiring" in user_input:
        import pandas as pd
        df = pd.read_sql_query("SELECT * FROM inventory", conn)
        expiring = df[df['spoilage_risk'] > 0.5]['item'].tolist()
        if expiring:
            return "Items expiring soon: " + ", ".join(expiring)
        else:
            return "No items expiring soon!"
    elif "recipe" in user_input:
        return "Go to Recipe Recommender tab to see suggestions."
    else:
        return "I can help with inventory, spoilage risk, and recipes."
