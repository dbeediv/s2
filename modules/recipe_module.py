# Recipe recommender functions here
import pandas as pd

# Load recipes CSV
recipes_df = pd.read_csv("recipes.csv")  # format: item,ingredients

def suggest_recipes(df_inventory):
    available_items = set(df_inventory['item'].tolist())
    suggestions = []
    for _, row in recipes_df.iterrows():
        ingredients = set(str(row['ingredients']).split(","))
        if ingredients.issubset(available_items):
            suggestions.append(row['item'])
    if not suggestions:
        suggestions.append("No exact recipe match. Try combining items creatively!")
    return suggestions
