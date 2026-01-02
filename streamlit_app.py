import json
import streamlit as st
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.title("AI Learning Assistant")

tab1, tab2 = st.tabs(["Create Study Pack", "Insights"])

# ---------------- Tab 1: User text → study pack ----------------
with tab1:
    st.markdown(
        "Paste any learning material (notes, chapter, article) below. "
        "The app uses Snowflake Cortex to generate a concise summary, "
        "interactive flashcards, and a multiple‑choice quiz."
    )

    user_text = st.text_area(
        "Input content",
        height=250,
        placeholder=(
            "Example: Binary search is an efficient algorithm for finding an item "
            "in a sorted array ..."
        ),
    )

    user_id = "demo_user"

    if st.button("Generate study pack", disabled=not user_text.strip()):
        # 1) Summary
        summary_df = session.sql(
            "SELECT SNOWFLAKE.CORTEX.SUMMARIZE(?) AS SUMMARY",
            params=[user_text],
        ).to_pandas()
        summary = summary_df["SUMMARY"].iloc[0]

        # Build prompts in Python, pass whole prompt as parameter
        flash_prompt = (
            'Create 5 flashcards as a JSON array of objects with fields '
            '"question" and "answer" for this text: ' + user_text
        )
        quiz_prompt = (
            'Create 5 multiple-choice quiz questions as a JSON array of objects '
            'with fields "question", "options" (4 options), and "correct_index" '
            '(0-3) for this text: ' + user_text
        )

        # 2) Flashcards JSON
        flash_df = session.sql(
            """
            SELECT SNOWFLAKE.CORTEX.COMPLETE(
              'snowflake-arctic', ?
            ) AS FLASHCARDS
            """,
            params=[flash_prompt],
        ).to_pandas()
        flashcards_json = flash_df["FLASHCARDS"].iloc[0]

        # 3) Quiz JSON
        quiz_df = session.sql(
            """
            SELECT SNOWFLAKE.CORTEX.COMPLETE(
              'snowflake-arctic', ?
            ) AS QUIZ
            """,
            params=[quiz_prompt],
        ).to_pandas()
        quiz_json = quiz_df["QUIZ"].iloc[0]

        st.session_state.summary = summary
        st.session_state.flashcards_json = flashcards_json
        st.session_state.quiz_json = quiz_json

        st.success("Study pack generated successfully.")

    # ----- Summary -----
    if "summary" in st.session_state:
        st.subheader("Auto‑generated summary")
        st.write(st.session_state.summary)

    # ----- Interactive flashcards -----
       # ----- Interactive flashcards -----
    if "flashcards_json" in st.session_state:
        st.subheader("Interactive flashcards")

        try:
            flashcards = json.loads(st.session_state.flashcards_json)
        except Exception:
            st.warning("Unable to parse flashcards JSON. Showing raw content.")
            st.json(st.session_state.flashcards_json)
            flashcards = []

        total_fc = len(flashcards)
        total_score = 0

        for i, fc in enumerate(flashcards):
            question = fc.get("question", "")
            correct_answer = fc.get("answer", "")

            st.markdown(f"**Card {i+1}: {question}**")
            user_answer = st.text_input("Your answer", key=f"fc_{i}")

            if user_answer:
                # Prompt for grading and feedback
                eval_prompt = (
                    "You are grading a short student answer.\n\n"
                    f"Question: {question}\n"
                    f"Expected answer: {correct_answer}\n"
                    f"Student answer: {user_answer}\n\n"
                    "1. Give a score from 0 to 1 (decimals allowed).\n"
                    "2. Briefly explain what was correct.\n"
                    "3. Briefly explain what was missing or incorrect.\n"
                    "Respond strictly as JSON with fields "
                    '"score", "correct_points", "missing_points".'
                )

                eval_df = session.sql(
                    """
                    SELECT SNOWFLAKE.CORTEX.COMPLETE(
                      'snowflake-arctic', ?
                    ) AS EVAL
                    """,
                    params=[eval_prompt],
                ).to_pandas()

                raw_eval = eval_df["EVAL"].iloc[0]

                try:
                    eval_json = json.loads(raw_eval)
                    score = float(eval_json.get("score", 0))
                    correct_points = eval_json.get("correct_points", "")
                    missing_points = eval_json.get("missing_points", "")
                except Exception:
                    # Fallback if model response is not perfect JSON
                    score = 0.0
                    correct_points = "Could not parse detailed feedback."
                    missing_points = raw_eval

                total_score += score

                st.success(f"Score for this card: {score:.2f} / 1.00")
                st.write("What you did well:")
                st.write(f"- {correct_points}")
                st.write("What you missed / got wrong:")
                st.write(f"- {missing_points}")

            st.markdown("---")

        if total_fc > 0:
            st.info(
                f"Flashcard score (sum over cards): {total_score:.2f} out of {total_fc:.0f}. "
                f"Each card is graded on a 0–1 scale, then summed."
            )

    # ----- Interactive quiz -----
    if "quiz_json" in st.session_state:
        st.subheader("Multiple‑choice quiz")

        try:
            quiz = json.loads(st.session_state.quiz_json)
        except Exception:
            st.warning("Unable to parse quiz JSON. Showing raw content.")
            st.json(st.session_state.quiz_json)
            quiz = []

        user_choices = []

        for i, q in enumerate(quiz):
            question = q.get("question", "")
            options = q.get("options", [])

            if not options:
                continue

            st.markdown(f"**Q{i+1}. {question}**")
            choice = st.radio(
                "Select an option",
                options=list(range(len(options))),
                format_func=lambda idx, opts=options: opts[idx],
                key=f"q_mc_{i}",
            )
            user_choices.append(choice)
            st.markdown("---")

        if quiz and st.button("Submit quiz"):
            correct = 0
            explanations = []

            for i, q in enumerate(quiz):
                options = q.get("options", [])
                correct_idx = q.get("correct_index", 0)
                chosen_idx = user_choices[i]

                if chosen_idx == correct_idx:
                    correct += 1
                    explanations.append(
                        f"Q{i+1}: correct option selected → 1 mark awarded."
                    )
                else:
                    correct_option = options[correct_idx] if options else ""
                    explanations.append(
                        f"Q{i+1}: incorrect option selected. "
                        f"Correct answer: '{correct_option}' → 0 marks."
                    )

            total_q = len(quiz)
            score = round((correct / total_q) * 100, 2)
            st.success(f"Quiz score: {score} ({correct} out of {total_q} correct).")

            st.write("Scoring breakdown:")
            for e in explanations:
                st.write("-", e)

# ---------------- Tab 2: Insights (placeholder) ----------------
with tab2:
    st.subheader("Insights")
    st.write(
        "This prototype focuses on generating study material from pasted text. "
        "Quiz scores can be stored in Snowflake to build instructor dashboards "
        "for weak‑topic analysis and learner progress."
    )
