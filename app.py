
import streamlit as st
from ai_engine import evaluate_answer
from pathlib import Path
import re

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- LOAD CSS ----------------

css_file = Path(__file__).parent / "styles.css"

if css_file.exists():
    st.markdown(
        f"<style>{css_file.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True
    )

# ---------------- HEADER ----------------

st.markdown("""
<div class="main-header">
    <div class="brand">
        <span class="brand-icon">✦</span>
        <span>Interview<span class="brand-highlight">AI</span></span>
    </div>
    <div class="header-tag">AI-POWERED PRACTICE</div>
</div>

<div class="hero-section">
    <div class="hero-label">YOUR PERSONAL INTERVIEW ASSISTANT</div>
    <h1>Prepare smarter.<br>
    <span class="gradient-text">Interview better.</span></h1>
    <p>Practice your answers, discover your strengths, and improve
    your interview skills with personalized AI feedback.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- MAIN INPUT SECTION ----------------

st.markdown("""
<div class="section-heading">
    <h3>Practice your interview answer</h3>
    <p>Enter a question and write your answer below.</p>
</div>
""", unsafe_allow_html=True)

with st.form("interview_form"):

    question = st.text_area(
        "INTERVIEW QUESTION",
        placeholder="Example: Tell me about yourself...",
        height=110
    )

    answer = st.text_area(
        "YOUR ANSWER",
        placeholder="Write your interview answer here. Explain your thoughts clearly...",
        height=230
    )

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        submitted = st.form_submit_button(
            "✦ Evaluate My Answer",
            use_container_width=True,
            type="primary"
        )

    with col2:
        clear = st.form_submit_button(
            "Clear Form",
            use_container_width=True
        )

# ---------------- CLEAR / EVALUATE ----------------

if clear:
    st.rerun()

if submitted:

    if not question.strip() or not answer.strip():
        st.warning("Please enter both the interview question and your answer.")

    else:
        st.session_state["last_question"] = question
        st.session_state["last_answer"] = answer

        with st.spinner("Gemini AI is reviewing your answer..."):

            try:
                feedback = evaluate_answer(question, answer)

                st.session_state["feedback"] = feedback
                st.session_state["feedback_error"] = None

            except Exception as error:
                st.session_state["feedback_error"] = str(error)
                st.session_state.pop("feedback", None)

# ---------------- FEEDBACK SECTION ----------------


# ---------------- PROFESSIONAL FEEDBACK SECTION ----------------

if st.session_state.get("feedback_error"):
    st.error("Unable to generate feedback. Please try again.")

    with st.expander("Technical details"):
        st.code(st.session_state["feedback_error"])


if st.session_state.get("feedback"):

    feedback = st.session_state["feedback"]

    # Extract score from Gemini response
    score_match = re.search(
        r"OVERALL SCORE:\s*(\d+(?:\.\d+)?)\s*/\s*10",
        feedback,
        re.IGNORECASE
    )

    st.markdown("""
    <div class="feedback-heading">
        <div class="feedback-label">✦ AI ANALYSIS COMPLETE</div>
        <h2>Your Personal Interview Report</h2>
        <p>Detailed feedback to help you become interview-ready.</p>
    </div>
    """, unsafe_allow_html=True)

    if score_match:
        score = float(score_match.group(1))

        st.markdown(
            f"""
            <div class="score-card">
                <div class="score-label">YOUR OVERALL SCORE</div>
                <div class="score-number">{score}<span>/10</span></div>
                <div class="score-description">
                    Your performance based on this answer
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Remove duplicate score from the displayed feedback
        feedback = re.sub(
            r"OVERALL SCORE:\s*\d+(?:\.\d+)?\s*/\s*10",
            "",
            feedback,
            count=1,
            flags=re.IGNORECASE
        )

    st.markdown("""
    <div class="feedback-card">
        <div class="feedback-card-title">
            ✨ Your Personalized AI Feedback
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(feedback)

    st.markdown("""
    <div class="bottom-note">
        ✦ Every practice session brings you one step closer
        to interview success.
    </div>
    """, unsafe_allow_html=True)
