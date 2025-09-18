from llmHelper import llm_model, model_switch

# Print all available models
print("Available models:")
for num, name in model_switch.items():
    print(f"{num}: {name}")

# Ask user to select a model number
model_number = int(input("Enter the model number you want to test: "))

try:
    print(f"\nUsing model number: {model_number} ({model_switch.get(model_number, 'Unknown')})")
    llm = llm_model(model_number)

    # Ask user for a query
    user_query = input("Enter your query for the model: ")
    response = llm.invoke(user_query).content.strip()

    print(f"\nResponse from model {model_number}:\n{response}")
except Exception as e:
    print(f"Error testing model {model_number}: {e}")
