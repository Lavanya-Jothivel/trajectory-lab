import streamlit as st

from src.reliability_agent import run_reliability_agent


st.set_page_config(
    page_title="Trajectory Lab",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Trajectory Lab")
st.subheader("Reliable ReAct Agent with Recovery & Verification")

st.write(
    "Explore how an AI agent handles normal tool execution, "
    "explicit tool failures, and silent incorrect outputs using "
    "recovery and verification."
)

# -----------------------------
# User Input
# -----------------------------

expression = st.text_input(
    "Enter a mathematical expression",
    placeholder="Example: (15 + 5) * 3",
)

primary_tool = st.selectbox(
    "Choose Primary Tool",
    [
        "calculator",
        "unreliable_calculator",
        "faulty_calculator",
    ],
)

# -----------------------------
# Run Agent
# -----------------------------

if st.button("🚀 Run Agent", type="primary"):

    if not expression.strip():
        st.warning("Please enter a mathematical expression.")

    else:
        try:
            result = run_reliability_agent(
                expression=expression,
                primary_tool=primary_tool,
            )

            st.divider()

            # -----------------------------
            # Final Answer
            # -----------------------------

            st.subheader("🎯 Final Answer")

            st.success(result["answer"])

            # -----------------------------
            # Reliability Metrics
            # -----------------------------

            st.subheader("📊 Reliability Status")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Recovered",
                    "Yes" if result["recovered"] else "No",
                )

            with col2:
                st.metric(
                    "Verified",
                    "Yes" if result["verified"] else "No",
                )

            with col3:
                st.metric(
                    "Corrected",
                    "Yes" if result["corrected"] else "No",
                )

            # -----------------------------
            # Agent Trajectory
            # -----------------------------

            st.subheader("🧠 Agent Trajectory")

            for step_number, step in enumerate(
                result["trajectory"],
                start=1,
            ):

                stage = step["stage"].upper()

                with st.container(border=True):

                    st.markdown(
                        f"### Step {step_number} — {stage}"
                    )

                    st.write(
                        f"**Tool:** `{step['tool']}`"
                    )

                    st.write(
                        f"**Input:** `{step['input']}`"
                    )

                    observation = step["observation"]

                    if observation.startswith("ERROR:"):
                        st.error(
                            f"Observation: {observation}"
                        )

                    else:
                        st.info(
                            f"Observation: {observation}"
                        )

            # -----------------------------
            # Explanation
            # -----------------------------

            st.subheader("🔍 Reliability Analysis")

            if result["recovered"]:
                st.warning(
                    "⚠️ The primary tool failed. "
                    "Trajectory Lab detected the failure "
                    "and recovered using the reliable calculator."
                )

            elif result["corrected"]:
                st.warning(
                    "⚠️ The primary tool returned an incorrect result. "
                    "Verification detected the mismatch and corrected it."
                )

            else:
                st.success(
                    "✅ The primary result was independently verified "
                    "and no correction was required."
                )

        except Exception as e:
            st.error(f"Agent execution failed: {e}")


st.divider()

st.caption(
    "Trajectory Lab • ReAct Agent Reliability • "
    "Failure Recovery • Verification • Self-Correction"
)