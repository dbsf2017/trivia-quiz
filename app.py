import streamlit as st
import requests

st.title("Trivia Quiz")

if "questions" not in st.session_state:
    st.session_state.questions = []
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.answered = False

if st.button("Start New Quiz"):
    response = requests.get("https://opentdb.com/api.php?amount=5&type=multiple")
    data = response.json()
    st.session_state.questions = data["results"]
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.answered = False

if st.session_state.questions:
    q = st.session_state.questions[st.session_state.current]
    total = len(st.session_state.questions)
    current = st.session_state.current

    st.write(f"**Question {current + 1} of {total}**")
    st.write(q["question"])

    options = q["incorrect_answers"] + [q["correct_answer"]]
    options = sorted(options)

    answer = st.radio("Choose your answer:", options, key=f"q{current}")

    if not st.session_state.answered:
        if st.button("Submit"):
            st.session_state.answered = True
            if answer == q["correct_answer"]:
                st.session_state.score += 1
                st.success("Correct!")
            else:
                st.error(f"Wrong! The answer was: {q['correct_answer']}")

    if st.session_state.answered:
        if current + 1 < total:
            if st.button("Next Question"):
                st.session_state.current += 1
                st.session_state.answered = False
                st.rerun()
        else:
            st.write(f"### Quiz Complete! Your score: {st.session_state.score} / {total}")
