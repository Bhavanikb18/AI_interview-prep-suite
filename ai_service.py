from groq import Groq

client = Groq(api_key="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");

MODEL = "llama-3.1-8b-instant"

def generate_ai_response(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def evaluate_answer(prompt):
    return generate_ai_response(prompt)