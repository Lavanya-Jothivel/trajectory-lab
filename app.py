import streamlit as st

from src.multi_tool_agent import (
    run_multi_tool_reliability_agent,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Trajectory Lab",
    page_icon="🤖",
    layout="wide",
)


# =========================================================
# SESSION STATE
# =========================================================

if "auto_query" not in st.session_state:
    st.session_state.auto_query = ""


def set_example_query(example_query):
    st.session_state.auto_query = example_query


# =========================================================
# HEADER
# =========================================================

st.title("🤖 Trajectory Lab")

st.caption(
    "Reliable Multi-Tool Agent with automatic routing, "
    "recovery, verification, and silent-error correction."
)


# =========================================================
# TABS
# =========================================================

tab1, tab2 = st.tabs(
    [
        "🚀 Auto Agent",
        "🧪 Reliability Lab",
    ]
)


# =========================================================
# AUTO AGENT
# =========================================================

with tab1:

    st.subheader("Ask the Agent")

    st.write(
        "Type a math question or a general knowledge question. "
        "The agent automatically selects the appropriate tool."
    )

    st.markdown("**Try an example:**")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.button(
            "🔢 Math Example",
            use_container_width=True,
            on_click=set_example_query,
            args=("What is 25 * 18?",),
        )

    with col2:
        st.button(
            "🧠 AI Example",
            use_container_width=True,
            on_click=set_example_query,
            args=("What is artificial intelligence?",),
        )

    with col3:
        st.button(
            "💻 Programming",
            use_container_width=True,
            on_click=set_example_query,
            args=("What is Java programming language?",),
        )

    with col4:
        st.button(
            "📚 History",
            use_container_width=True,
            on_click=set_example_query,
            args=("Albert Einstein",),
        )

    st.text_input(
        "Your question",
        key="auto_query",
        placeholder=(
            "Example: What is 25 * 18? "
            "or What is deep learning?"
        ),
    )

    run_auto = st.button(
        "🚀 Run Agent",
        type="primary",
        use_container_width=True,
        key="run_auto",
    )

    if run_auto:

        current_query = st.session_state.auto_query.strip()

        if not current_query:

            st.warning(
                "Please enter a question first."
            )

        else:

            with st.spinner(
                "Running reliability-aware agent..."
            ):

                result = run_multi_tool_reliability_agent(
                    current_query,
                    primary_tool="auto",
                )

            st.divider()

            # =================================================
            # FINAL ANSWER
            # =================================================

            st.subheader("Final Answer")

            st.success(
                result["answer"]
            )

            # =================================================
            # AGENT DECISION
            # =================================================

            st.subheader("Agent Decision")

            metric1, metric2, metric3, metric4 = st.columns(4)

            with metric1:
                st.metric(
                    "Selected Tool",
                    result["selected_tool"],
                )

            with metric2:
                st.metric(
                    "Recovered",
                    "Yes"
                    if result["recovered"]
                    else "No",
                )

            with metric3:
                st.metric(
                    "Verified",
                    "Yes"
                    if result["verified"]
                    else "No",
                )

            with metric4:
                st.metric(
                    "Corrected",
                    "Yes"
                    if result["corrected"]
                    else "No",
                )

            # =================================================
            # TRAJECTORY
            # =================================================

            with st.expander(
                "🔍 View Execution Trajectory"
            ):

                for index, step in enumerate(
                    result["trajectory"],
                    start=1,
                ):

                    stage_name = (
                        step["stage"]
                        .replace("_", " ")
                        .title()
                    )

                    st.markdown(
                        f"### Step {index}: {stage_name}"
                    )

                    st.write(
                        f"**Tool:** `{step['tool']}`"
                    )

                    st.write(
                        f"**Input:** {step['input']}"
                    )

                    st.write(
                        "**Observation:**"
                    )

                    st.code(
                        str(step["observation"])
                    )

                    st.divider()


# =========================================================
# RELIABILITY LAB
# =========================================================

with tab2:

    st.subheader(
        "Reliability & Fault Injection"
    )

    st.write(
        "This section demonstrates how the agent handles "
        "explicit tool failures and silently incorrect outputs."
    )

    scenario = st.selectbox(
        "Choose a reliability scenario",
        [
            "Explicit Calculator Failure",
            "Silent Calculator Error",
            "Explicit Lookup Failure",
            "Silent Lookup Error",
        ],
        key="scenario",
    )

    # -----------------------------------------------------
    # SCENARIOS
    # -----------------------------------------------------

    if scenario == "Explicit Calculator Failure":

        demo_query = "(15 + 5) * 3"
        demo_tool = "unreliable_calculator"

        st.info(
            "The primary calculator intentionally fails "
            "for expressions containing 15."
        )

    elif scenario == "Silent Calculator Error":

        demo_query = "8 * 8"
        demo_tool = "faulty_calculator"

        st.info(
            "The faulty calculator intentionally returns 63. "
            "The trusted calculator should detect the mismatch "
            "and correct the result to 64."
        )

    elif scenario == "Explicit Lookup Failure":

        demo_query = "capital of japan"
        demo_tool = "unreliable_lookup"

        st.info(
            "The primary lookup intentionally fails for "
            "Japan-related queries. The trusted lookup tool "
            "should recover the answer."
        )

    else:

        demo_query = "capital of france"
        demo_tool = "faulty_lookup"

        st.info(
            "The faulty lookup intentionally returns Lyon. "
            "The trusted lookup should detect the mismatch "
            "and correct the answer to Paris."
        )

    st.write(
        f"**Query:** `{demo_query}`"
    )

    st.write(
        f"**Primary Tool:** `{demo_tool}`"
    )

    run_demo = st.button(
        "🧪 Run Reliability Demo",
        type="primary",
        use_container_width=True,
        key="run_demo",
    )

    if run_demo:

        with st.spinner(
            "Running reliability experiment..."
        ):

            result = run_multi_tool_reliability_agent(
                demo_query,
                primary_tool=demo_tool,
            )

        st.divider()

        # =================================================
        # RESULT
        # =================================================

        st.subheader("Final Answer")

        st.success(
            result["answer"]
        )

        metric1, metric2, metric3 = st.columns(3)

        with metric1:
            st.metric(
                "Recovered",
                "Yes"
                if result["recovered"]
                else "No",
            )

        with metric2:
            st.metric(
                "Verified",
                "Yes"
                if result["verified"]
                else "No",
            )

        with metric3:
            st.metric(
                "Corrected",
                "Yes"
                if result["corrected"]
                else "No",
            )

        # =================================================
        # TRAJECTORY
        # =================================================

        st.subheader(
            "Execution Trajectory"
        )

        for index, step in enumerate(
            result["trajectory"],
            start=1,
        ):

            stage_name = (
                step["stage"]
                .replace("_", " ")
                .title()
            )

            with st.expander(
                f"Step {index} — {stage_name}",
                expanded=True,
            ):

                st.write(
                    f"**Tool:** `{step['tool']}`"
                )

                st.write(
                    f"**Input:** {step['input']}"
                )

                st.write(
                    "**Observation:**"
                )

                st.code(
                    str(step["observation"])
                )


# =========================================================
# ABOUT
# =========================================================

st.divider()

with st.expander(
    "ℹ️ About Trajectory Lab"
):

    st.markdown(
        """
**Trajectory Lab** is a reliability-focused multi-tool
agent framework.

It demonstrates:

- Automatic tool routing
- Natural-language mathematical queries
- Safe mathematical execution
- Dynamic Wikipedia retrieval
- Explicit tool-failure recovery
- Trusted-tool rechecking
- Silent-error detection and correction
- Full execution trajectory inspection

The Reliability Lab uses controlled fault injection to
demonstrate how an agent responds when a tool either fails
or silently produces an incorrect result.
"""
    )