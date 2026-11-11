
import os
import time

from dotenv import load_dotenv
from google import genai
from langfuse import get_client

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.5-flash-lite"

# Initialize Gemini and Langfuse
client = genai.Client(api_key=API_KEY) if API_KEY else None
langfuse = get_client()


def evaluate_answer(question, answer):
    if not API_KEY or client is None:
        raise ValueError("Gemini API key not found. Check your .env file.")

    start_time = time.time()

    try:
        with langfuse.start_as_current_observation(
            as_type="generation",
            name="Gemini Interview Answer Evaluation",
            model=MODEL_NAME,
            input={
                "question_length": len(question),
                "answer_length": len(answer)
            }
        ) as generation:

            prompt = f"""
You are an experienced interview coach.

Evaluate the candidate's answer in a simple and helpful way.

Interview Question:
{question}

Candidate Answer:
{answer}

Provide feedback using this structure:

1. Score: Give a score out of 10.
2. Strengths: Mention what the candidate did well.
3. Improvements: Explain what can be improved.
4. Better Answer: Provide a clear and professional sample answer.
5. Communication Feedback: Comment on clarity and confidence.

Use simple English and be encouraging.
"""

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            feedback = response.text or "No feedback was generated."
            latency = round(time.time() - start_time, 2)

            usage = getattr(response, "usage_metadata", None)

            usage_details = {}
            if usage:
                usage_details = {
                    "input_tokens": getattr(
                        usage, "prompt_token_count", None
                    ),
                    "output_tokens": getattr(
                        usage, "candidates_token_count", None
                    ),
                    "total_tokens": getattr(
                        usage, "total_token_count", None
                    )
                }

            generation.update(
                output={
                    "feedback_length": len(feedback)
                },
                usage_details=usage_details,
                metadata={
                    "latency_seconds": latency,
                    "status": "success"
                }
            )

            return feedback

    except Exception as error:
        latency = round(time.time() - start_time, 2)

        # Record the error without storing the user's answer
        with langfuse.start_as_current_observation(
            as_type="span",
            name="Interview Evaluation Error",
            input={"status": "failed"}
        ) as observation:
            observation.update(
                level="ERROR",
                status_message=str(error),
                metadata={"latency_seconds": latency}
            )

        raise
