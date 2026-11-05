import os
from google import genai

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def get_ai_response(question):
    try:
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=question
        )

        return interaction.output_text

    except Exception as e:
        print("Gemini API Error:", e)

        return None