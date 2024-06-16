import os
import time
import google.generativeai as genai

# Use environment variable for API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the GOOGLE_API_KEY environment variable.")

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 500,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
    "You are an enthusiastic and talkative chef from France, specializing in French cuisine. "
    "You love to share your deep knowledge of French dishes, techniques, and ingredients. "
    "You use common friendly expressions and enjoy discussing the elegance and traditions of French cooking. "
    "If the user inputs a non-French dish, you will provide its recipe but also make a comment about preferring French cuisine."
    "You always aim to be clear and provide the best possible recipes for the user's needs. You are familiar with various cuisines "
    "but French cuisine is your true passion."
    "If you get any dish which is not a recipe that you can provide ingredients for politely decline and end the conversation"
    "Decline any conversation that is not related to food recipes and cuisine. "
)

)
chat_history = [
    {
        "role": "user",
        "parts": ["hi\n"],
    }
]

chat_session = model.start_chat(
    history=chat_history
)

def send_message(chat_session, message, delay=1):
    response = chat_session.send_message(message)
    print(response.text)
    return response

# Function to handle user request
def handle_request(user_input):
    if user_input.startswith("Ingredients:"):
        ingredients = user_input[len("Ingredients:"):].strip()
        message = f"Suggest a dish with the following ingredients: {ingredients}"
    elif user_input.startswith("Dish:"):
        dish = user_input[len("Dish:"):].strip()
        message = f"Give me a detailed recipe for {dish}"
    elif user_input.startswith("Recipe:"):
        recipe = user_input[len("Recipe:"):].strip()
        message = f"Critique the following recipe: {recipe}"
    else:
        message = "Please provide ingredients, a dish name, or a recipe for critique."

    chat_history.append({
        "role": "user",
        "parts": [message]
    })

    chat_session = model.start_chat(
        history=chat_history
    )

    response = send_message(chat_session, message)
    chat_history.append({
        "role": "model",
        "parts": [response.text]
    })

# Main function for testing
def main():
    while True:
        user_input = input("\nEnter your request (Ingredients:/Dish:/Recipe:):\n")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending the chat. Goodbye!")
            break
        handle_request(user_input)

if __name__ == "__main__":
    main()
