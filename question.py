import streamlit as st
from docx import Document
import re
import random

def load_answers(file_path):
    with open(file_path, 'r') as f:
        answers = f.readlines()
    return [answer.strip() for answer in answers]

def extract_questions_from_word(file_path):
    doc = Document(file_path)
    questions = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text.startswith('Q'):
            question_text, *options_text = re.split('①|②|③|④|⑤', text)
            question = question_text.strip()
            options = [f'①{options_text[0]}', f'②{options_text[1]}', f'③{options_text[2]}', f'④{options_text[3]}', f'⑤{options_text[4]}'] if len(options_text) >= 5 else [f'①{options_text[i]}' for i in range(len(options_text))]
            questions.append({'question': question, 'options': options})
    return questions

def app():
    if 'questions' not in st.session_state or 'answers' not in st.session_state:
        questions = extract_questions_from_word(r"D:\python\blog\output\output.docx")
        answers = load_answers(r"D:\python\blog\2019_answer.txt")

        # Shuffle the questions and answers in unison
        combined = list(zip(questions, answers))
        random.shuffle(combined)
        st.session_state.questions, st.session_state.answers = zip(*combined)

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None

    question = st.session_state.questions[st.session_state.current_question]
    st.write(question['question'])
    st.session_state.selected_option = st.radio('Choose one:', question['options'], key=str(st.session_state.current_question))

    if st.button('정답 확인') and st.session_state.selected_option:
        correct_answer = st.session_state.answers[st.session_state.current_question]
        selected_option_index = question['options'].index(st.session_state.selected_option)
        if str(selected_option_index + 1) == correct_answer:  # Add 1 to selected_option_index because it is 0-indexed
            st.success("정답입니다.")
        else:
            st.error(f"오답입니다. 정답은 {correct_answer}번 입니다.")

    if st.button('다음 문제', disabled=st.session_state.current_question == len(st.session_state.questions) - 1):
        st.session_state.current_question += 1
        if st.session_state.current_question >= len(st.session_state.questions):
            st.session_state.current_question = 0
        st.session_state.selected_option = None  # Reset the selected option
        st.experimental_rerun()

    if st.button('이전 문제', disabled=st.session_state.current_question == 0):
        st.session_state.current_question -= 1
        if st.session_state.current_question < 0:
            st.session_state.current_question = len(st.session_state.questions) - 1
        st.session_state.selected_option = None  # Reset the selected option
        st.experimental_rerun()

if __name__ == "__main__":
    app()
