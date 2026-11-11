
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


def evaluate_answer(question, answer):

    if not API_KEY:
        raise ValueError("Gemini API key not found in .env file.")

    prompt = f"""
    You are a professional AI Interview Coach.

    Evaluate the candidate's answer fairly.
    Use simple, natural and professional English.

    INTERVIEW QUESTION:
    {question}

    CANDIDATE'S ANSWER:
    {answer}

    Follow this exact output structure:

    OVERALL SCORE: X/10

    ### 🎯 Overall Assessment
    Give a short assessment of the answer.

    ### 💪 Strengths
    Give 3 specific strengths.

    ### 🚀 Areas to Improve
    Give 3 practical improvements.

    ### 📌 Important Points Missing
    Mention important missing points.

    ### ✨ Interview-Ready Answer
    Rewrite the answer in natural, confident English.
    Do not invent experience or achievements.

    ### 🎤 Interview Coach's Tip
    Give one practical interview tip.

    ### ⭐ Final Recommendation
    Give one encouraging sentence.

    Rules:
    - Score fairly based on relevance, clarity,
      structure, examples and accuracy.
    - Be specific to the candidate's answer.
    - Use simple English.
    - Never invent candidate information.
    """

    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text or "No feedback was generated."
