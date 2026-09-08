# 🤖 Trajectory Lab

### ReAct Replication and Reliability Analysis of Tool-Using Language Agents

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-32%20passed-brightgreen)](#testing)
[![Streamlit](https://img.shields.io/badge/Live%20Demo-Streamlit-red)](https://trajectory-lab-5agbx7aqfqtx92ljzeozla.streamlit.app/)

**Live Demo:**  
https://trajectory-lab-5agbx7aqfqtx92ljzeozla.streamlit.app/

Trajectory Lab is a research-oriented implementation exploring how tool-using language agents behave when tool execution is unreliable.

The project begins with the **ReAct** paradigm—interleaving reasoning, actions, and observations—and extends the basic agent with reliability mechanisms for:

- automatic multi-tool routing
- explicit tool-failure recovery
- silent-error verification
- automatic correction
- guarded tool execution
- unsupported-task abstention
- dynamic knowledge retrieval
- fallback retrieval
- trajectory-level evaluation
- controlled fault injection

The central question is:

> **Is producing the correct answer enough, or should a tool-using agent also be evaluated on how reliably it obtained that answer?**

Trajectory Lab explores both.

---

# 🚀 Live Interactive Demo

The project includes a deployed Streamlit application with two modes.

### 🚀 Auto Agent

Users can enter mathematical or factual questions.

Examples:

```text
What is 347 * 29?
What is artificial intelligence?
What is Java programming language?
Who is Alan Turing?
Apollo 11
```

The agent automatically determines whether to use:

```text
calculator
or
knowledge lookup
```

The interface displays:

```text
Final Answer
Selected Tool
Recovered
Verified
Corrected
Execution Trajectory
```

### 🧪 Reliability Lab

The Reliability Lab provides controlled fault-injection experiments demonstrating:

- explicit calculator failure
- silent calculator error
- explicit lookup failure
- silent lookup error

This makes the recovery and correction mechanisms directly observable.

**Live application:**

https://trajectory-lab-5agbx7aqfqtx92ljzeozla.streamlit.app/

---

# Research Foundation

This project is inspired by:

**ReAct: Synergizing Reasoning and Acting in Language Models**

Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao.

ICLR 2023.

ReAct combines reasoning traces with actions so that language models can interact with external environments and tools while solving tasks.

Trajectory Lab reproduces the core interaction pattern:

```text
Thought
   ↓
Action
   ↓
Action Input
   ↓
Observation
   ↓
Thought
   ↓
Final Answer
```

The project then extends this execution pattern to study what happens when tools fail, return incorrect results, or are bypassed by the model.

---

# Motivation

Final-answer accuracy does not necessarily imply reliable agent behavior.

A tool-using model may:

- answer directly instead of calling the required tool
- select the wrong tool
- generate malformed tool calls
- fabricate observations
- fail when a tool becomes unavailable
- trust plausible but incorrect tool outputs
- repeatedly call tools unnecessarily
- route unsupported requests to inappropriate tools

A particularly important distinction is between:

```text
Answer Correctness
```

and:

```text
Execution Reliability
```

For example, a model may know that:

```text
6 * 7 = 42
```

without actually calling the calculator it was instructed to use.

The final answer is correct, but the execution policy was violated.

Trajectory Lab therefore evaluates not only the final answer but also the trajectory used to obtain it.

---

# System Architecture

The current system combines automatic routing, guarded execution, recovery, verification, correction, and trajectory logging.

```text
                    User Query
                        │
                        ▼
                ┌───────────────┐
                │  Tool Router  │
                └───────────────┘
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
         Calculator        Knowledge Lookup
              │                   │
              └─────────┬─────────┘
                        │
                        ▼
                Primary Execution
                        │
               ┌────────┴────────┐
               │                 │
               ▼                 ▼
        Explicit Failure?   Successful Output
               │                 │
              Yes                ▼
               │            Verification
               ▼                 │
            Recovery        ┌────┴────┐
               │            │         │
               ▼          Match    Mismatch
         Trusted Tool        │         │
               │             ▼         ▼
               │          Accept    Correct
               └─────────────┬─────────┘
                             │
                             ▼
                        Final Answer
                             │
                             ▼
                     Trajectory Logging
```

The system also contains guarded-router experiments where unsupported tasks can be left unrouted rather than forcing an inappropriate tool call.

---

# Current Multi-Tool Agent

The current interactive agent supports two primary tool families.

## 1. Calculator

Arithmetic expressions are evaluated using a restricted Python AST evaluator rather than unrestricted `eval()`.

Example:

```text
Input:
What is (15 + 5) * 3?

Extracted Expression:
(15 + 5) * 3

Output:
60
```

Supported operations include basic arithmetic such as:

```text
+
-
*
/
%
**
()
```

The router can recognize natural-language mathematical prompts and extract the expression before execution.

---

## 2. Dynamic Knowledge Lookup

The original controlled implementation used a small local factual knowledge base.

The current version extends this into **dynamic external retrieval**.

The retrieval pipeline uses:

```text
Knowledge Query
      │
      ▼
Wikipedia
      │
      ├──── Success ────► Return Result
      │
      └──── Failure / Rate Limit
                    │
                    ▼
             Fallback Source
                    │
                    ▼
               Return Result
```

Wikipedia search results are ranked instead of blindly accepting the first result.

This improves ambiguous queries such as:

```text
What is Java programming language?
What is Python programming language?
What is C programming language?
What is Rust programming language?
```

and helps avoid unrelated results such as comparison or list pages.

Example dynamic queries:

```text
What is artificial intelligence?
What is reinforcement learning?
Who is Alan Turing?
Apollo 11
What is Kubernetes?
What is PostgreSQL?
```

A small deterministic answer set is retained for controlled benchmark cases so earlier experiments remain reproducible.

---

# Automatic Tool Routing

The current multi-tool agent automatically chooses between mathematical execution and factual retrieval.

Example:

```text
"What is 25 * 18?"
        │
        ▼
   Math Detection
        │
        ▼
    Calculator
        │
        ▼
       450
```

For a factual question:

```text
"What is deep learning?"
        │
        ▼
   Tool Router
        │
        ▼
      Lookup
        │
        ▼
Dynamic Knowledge Retrieval
```

This allows the Streamlit application to expose a simple **Auto Agent** interface without requiring users to manually choose a tool.

---

# Core ReAct Agent

The original implementation follows a ReAct-style execution loop.

A typical trajectory is:

```text
Question: What is 6 * 7?

Thought: I should calculate this.

Action: calculator

Action Input: 6 * 7

Observation: 42

Thought: I have the result.

Final Answer: 42
```

The implementation separates:

- prompt construction
- model generation
- output parsing
- tool execution
- trajectory recording

The parser recognizes either an agent action or a final answer.

---

# Real Language Model Integration

Trajectory Lab also integrates a real instruction-tuned language model:

```text
Qwen/Qwen2.5-0.5B-Instruct
```

through Hugging Face Transformers.

The model interface applies the tokenizer's chat template before generation so that the instruction-tuned model receives prompts in its expected conversational structure.

The experiments were designed to remain CPU-friendly.

The real-model experiments are separate from the deterministic reliability mechanisms used by the deployed Streamlit demo.

---

# Real-Model ReAct Observation

A small seven-task real-model evaluation produced:

| Metric | Result |
|---|---:|
| Answer Accuracy | 100.00% |
| Correct Tool Selection Rate | 57.14% |
| Average Steps | 1.57 |
| Average Tool Calls | 0.57 |
| Error Rate | 0.00% |

The important observation was the gap between:

```text
Answer Accuracy = 100%
```

and:

```text
Correct Tool Selection = 57.14%
```

The model could often answer simple questions correctly from internal knowledge or arithmetic ability while ignoring the intended tool-use policy.

Therefore:

> **Correct answers do not necessarily imply correct agent execution.**

This observation motivated the guarded-routing experiments.

---

# Guarded Routing

Trajectory Lab introduces a deterministic routing layer for supported tasks.

Arithmetic questions can be routed to:

```text
calculator
```

while supported factual questions can be routed to:

```text
lookup
```

The purpose of the guard is not to improve the language model's reasoning ability.

Instead, it enforces an execution policy when a deterministic tool is expected to be used.

---

# Raw Model vs Guarded Router

A controlled eight-task evaluation compared raw Qwen responses against guarded routing.

| Metric | Result |
|---|---:|
| Tasks | 8 |
| Raw Qwen Accuracy | 87.50% |
| Guarded Router Accuracy | 100.00% |
| Guard Trigger Rate | 100.00% |

One constructed arithmetic case exposed the difference.

Question:

```text
What is (15 + 5) * 3?
```

In the controlled run, the raw model returned an incorrect result.

The guarded router instead extracted:

```text
(15 + 5) * 3
```

and required execution through the calculator.

Result:

```text
60
```

The improvement should therefore be interpreted as **tool-policy enforcement**, not as improved language-model reasoning.

---

# Failure Injection

Trajectory Lab deliberately introduces controlled failures so reliability mechanisms can be tested reproducibly.

There are two major failure classes.

## 1. Explicit Tool Failure

An unreliable tool reports that execution failed.

Example:

```text
ERROR: calculator temporarily unavailable
```

Because the failure is visible, the reliability layer can detect it and execute a fallback strategy.

---

## 2. Silent Tool Failure

A faulty tool returns a plausible but incorrect result without reporting an error.

Example:

```text
8 * 8 → 63
```

This is more dangerous because simply checking for an error message is insufficient.

The result must instead be compared with a trusted reference execution.

---

# Recovery Agent

The recovery mechanism handles explicit tool failures.

Example:

```text
Question
   │
   ▼
Unreliable Calculator
   │
   ▼
ERROR
   │
   ▼
Failure Detected
   │
   ▼
Trusted Calculator
   │
   ▼
Correct Result
```

For:

```text
(15 + 5) * 3
```

the controlled unreliable calculator produces:

```text
ERROR: calculator temporarily unavailable
```

The trusted calculator then evaluates the original expression:

```text
60
```

The recovery event is recorded in the trajectory.

---

# Verification and Silent-Error Correction

Explicit failures are relatively easy to detect.

Silent failures are more difficult because the result appears valid.

For:

```text
8 * 8
```

the deliberately faulty calculator returns:

```text
63
```

The reliability layer rechecks the expression using the trusted calculator:

```text
64
```

Because the two results disagree, the system records a correction and returns:

```text
64
```

Trajectory:

```text
Faulty Calculator
       │
       ▼
      63
       │
       ▼
 Trusted Recheck
       │
       ▼
      64
       │
       ▼
Mismatch Detected
       │
       ▼
Corrected Answer
       │
       ▼
      64
```

For the current implementation, this is best understood as **trusted-tool rechecking** rather than universal independent factual verification.

---

# Reliability Lab

The deployed Streamlit application exposes four reproducible reliability scenarios.

| Scenario | Injected Problem | Expected Behavior |
|---|---|---|
| Explicit Calculator Failure | Calculator reports failure | Recover using trusted calculator |
| Silent Calculator Error | `8 * 8 → 63` | Detect mismatch and return `64` |
| Explicit Lookup Failure | Japan lookup reports failure | Recover using trusted lookup |
| Silent Lookup Error | France capital returns `Lyon` | Detect mismatch and return `Paris` |

These are intentionally injected failures used to evaluate the reliability pipeline.

They should not be interpreted as naturally occurring production failures.

---

# Reliable Guarded Agent

Guarded routing was combined with recovery and verification.

```text
Route
  │
  ▼
Execute Tool
  │
  ▼
Detect Failure
  │
  ├───────────────┐
  │               │
  ▼               ▼
Explicit       Silent
Failure        Fault
  │               │
  ▼               ▼
Recovery      Verification
  │               │
  ▼               ▼
Fallback      Correction
  │               │
  └───────┬───────┘
          │
          ▼
     Final Answer
```

---

# Reliable Guarded Benchmark

A five-task controlled reliability evaluation included:

- normal arithmetic
- explicit tool failure
- silent tool fault
- unsupported request

Results:

| Metric | Result |
|---|---:|
| Tasks | 5 |
| Accuracy | 100.00% |
| Guard Trigger Rate | 80.00% |
| Recovery Events | 1 |
| Verification Events | 1 |
| Correction Events | 1 |

The unsupported question was intentionally left unrouted.

This demonstrates that the guard does not simply trigger for every request.

---

# Unified Reliable Router

The unified reliability system combines:

- arithmetic routing
- factual lookup routing
- explicit failure detection
- fallback recovery
- silent-error verification
- correction
- abstention
- trajectory logging

Execution policy:

```text
Route
  ↓
Execute
  ↓
Detect
  ↓
Recover / Verify
  ↓
Correct
  ↓
Return
  ↓
Log
```

The newer multi-tool agent extends this concept with dynamic factual retrieval and a Streamlit interface.

---

# Unified Reliable Router Benchmark

The controlled benchmark contains seven scenarios covering:

- normal arithmetic
- explicit calculator failure
- silent calculator fault
- factual lookup
- unsupported-task abstention

Results:

| Metric | Result |
|---|---:|
| Tasks | 7 |
| Accuracy | 100.00% |
| Guard Trigger Rate | 85.71% |
| Abstention Rate | 14.29% |
| Recovery Events | 1 |
| Verification Events | 1 |
| Correction Events | 1 |
| Average Trajectory Events | 2.29 |

The abstention rate corresponds to the deliberately unsupported task.

Instead of forcing an arbitrary tool call, the guarded router returns no supported route.

---

# Trajectory-Level Evaluation

Trajectory Lab records execution trajectories rather than evaluating only final answers.

A trajectory can contain events such as:

```text
tool_selection
guard
primary
action
recovery
verification
correction
```

For an earlier five-run reliability evaluation:

| Metric | Result |
|---|---:|
| Runs | 5 |
| Average Trajectory Events | 2.40 |
| Guard Events | 5 |
| Tool Actions | 4 |
| Recovery Events | 1 |
| Verification Events | 1 |
| Correction Events | 1 |
| Recovery Rate | 20.00% |
| Verification Rate | 20.00% |
| Correction Rate | 20.00% |

This makes the internal execution behavior observable.

---

# Experimental Summary

The main controlled experiments produced:

| Experiment | Accuracy / Metric |
|---|---:|
| Direct Baseline | 60.00% |
| Mock ReAct | 100.00% |
| Qwen ReAct Answer Accuracy | 100.00% |
| Qwen ReAct Tool Selection | 57.14% |
| Raw Qwen Controlled Accuracy | 87.50% |
| Guarded Router | 100.00% |
| Reliable Guarded Benchmark | 100.00% |
| Unified Reliable Router | 100.00% |

**Important:** these results come from different small controlled task sets.

They should not be interpreted as scores from one common benchmark or as general real-world agent reliability claims.

---

# Key Result Visuals

## Raw Qwen vs Guarded Router

The guarded router improves controlled execution reliability by enforcing deterministic tool use for supported tasks rather than allowing the model to bypass required tools.

![Guarded Router Benchmark](results/guarded_router_benchmark.png)

## Unified Reliability Evaluation

The unified router combines guarded routing, explicit failure recovery, silent-error verification, correction, and abstention.

![Unified Router Benchmark](results/unified_router_benchmark.png)

## Reliability Mechanism Ablation

The ablation summary compares the major agent variants and reliability mechanisms evaluated in Trajectory Lab.

![Ablation Summary](results/ablation_summary.png)

---

# Key Finding

The central observation of Trajectory Lab is the distinction between:

```text
Answer Correctness
```

and:

```text
Execution Reliability
```

A language model may produce the correct answer while:

- ignoring the required tool
- selecting the wrong tool
- fabricating intermediate reasoning
- failing to recover from tool errors
- trusting incorrect tool outputs

Therefore, evaluation of tool-using agents should consider both:

```text
What answer did the agent produce?
```

and:

```text
How did the agent obtain that answer?
```

Trajectory Lab explores this second dimension through trajectory logging, tool-policy enforcement, recovery, trusted-tool rechecking, correction, and abstention.

---

# Project Structure

```text
trajectory-lab/
│
├── app.py
├── pytest.ini
├── requirements.txt
├── README.md
│
├── src/
│   ├── agent.py
│   ├── baseline.py
│   ├── environment.py
│   ├── guarded_agent.py
│   ├── guarded_router.py
│   ├── model_interface.py
│   ├── multi_tool_agent.py
│   ├── parser.py
│   ├── prompts.py
│   ├── react_recovery_agent.py
│   ├── recovery_agent.py
│   ├── reliability_agent.py
│   ├── reliable_guarded_agent.py
│   ├── reliable_guarded_router.py
│   ├── tools.py
│   └── verification_agent.py
│
├── experiments/
│   ├── baseline evaluation
│   ├── ReAct evaluation
│   ├── recovery experiments
│   ├── verification experiments
│   ├── trajectory analysis
│   ├── real-model evaluation
│   ├── guarded-router evaluation
│   └── unified reliability evaluation
│
├── tests/
│   ├── unit tests
│   └── integration tests
│
└── results/
    ├── CSV experiment results
    ├── JSON trajectory traces
    └── PNG plots
```

---

# Tech Stack

### Core

- Python 3.12
- PyTorch
- Hugging Face Transformers
- Qwen2.5-0.5B-Instruct

### Agent Reliability

- ReAct-style execution
- deterministic guarded routing
- automatic multi-tool routing
- AST-based calculator
- recovery mechanisms
- trusted-tool rechecking
- controlled fault injection

### Retrieval

- Wikipedia API
- fallback knowledge retrieval
- HTTP requests

### Interface

- Streamlit

### Evaluation

- Pytest
- Pandas
- NumPy
- scikit-learn
- Matplotlib

---

# Testing

The project contains unit and integration tests covering:

- calculator execution
- factual lookup
- tool registry
- parser behavior
- ReAct execution
- recovery behavior
- verification behavior
- silent-error correction
- guarded arithmetic routing
- guarded factual routing
- unsupported-task abstention
- unified reliability behavior

Current status:

```text
32 passed
```

Run:

```bash
pytest -q
```

or:

```bash
python -m pytest -v
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Lavanya-Jothivel/trajectory-lab.git
cd trajectory-lab
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Streamlit App

Start the interactive application with:

```bash
streamlit run app.py
```

Then use either:

```text
🚀 Auto Agent
```

or:

```text
🧪 Reliability Lab
```

---

# Running the Experiments

## Real-model agent evaluation

```bash
python -m experiments.real_agent_eval
```

## Tool-selection evaluation

```bash
python -m experiments.tool_selection_eval
```

## Guarded-router benchmark

```bash
python -m experiments.guarded_router_benchmark
```

## Reliable guarded benchmark

```bash
python -m experiments.reliable_guarded_benchmark
```

## Unified reliable-router benchmark

```bash
python -m experiments.unified_router_benchmark
```

## Reliable trajectory metrics

```bash
python -m experiments.reliable_trajectory_metrics
```

## Full test suite

```bash
python -m pytest -v
```

---

# Results

Generated experiment artifacts are stored under:

```text
results/
```

Important outputs include:

```text
results/real_agent_eval.csv
results/real_agent_accuracy.png

results/guarded_benchmark.csv
results/guarded_benchmark.png

results/guarded_router_benchmark.csv
results/guarded_router_benchmark.png

results/reliable_guarded_benchmark.csv
results/reliable_guarded_trajectories.json

results/reliable_trajectory_metrics.csv
results/reliable_trajectory_metrics.png

results/unified_router_benchmark.csv
results/unified_router_benchmark.png

results/final_results_summary.csv
results/final_results_summary.json
```

Additional baseline, recovery, verification, and trajectory experiment outputs are retained in the `results/` directory.

---

# Current Scope and Limitations

Trajectory Lab is a controlled research replication and reliability project rather than a general-purpose AI assistant.

Current limitations include:

- relatively small controlled evaluation sets
- rule-based routing for the deployed agent
- synthetic fault-injection scenarios
- one small instruction-tuned model in the real-model experiments
- external retrieval services can vary in availability and result quality
- trusted-tool rechecking is not equivalent to universal factual verification
- no general code-generation tool
- no large standardized agent benchmark
- no production-scale external tool ecosystem

The reported 100% results therefore validate specific mechanisms **within their controlled evaluation settings**.

They should not be interpreted as evidence of 100% reliability on arbitrary real-world agent tasks.

---

# Future Work

Potential extensions include:

- LLM-based semantic tool routing
- independent multi-source factual verification
- confidence-aware routing
- retrieval confidence scoring
- additional tool families
- code-generation tools
- web-search tools
- dynamic tool registries
- stochastic tool failures
- adversarial tool outputs
- multi-step recovery policies
- retry policies with exponential backoff
- tool-health monitoring
- latency and cost measurements
- trajectory anomaly detection
- automated policy-compliance scoring
- larger standardized agent benchmarks

---

# Reproducibility

The repository retains:

- experiment scripts
- unit tests
- integration tests
- CSV result tables
- JSON trajectories
- generated plots
- consolidated result summaries
- controlled fault-injection tools

This allows the reliability experiments to be rerun and inspected independently.

---

# Reference

Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023).

**ReAct: Synergizing Reasoning and Acting in Language Models.**

International Conference on Learning Representations (ICLR).

Paper: https://arxiv.org/abs/2210.03629

---

# Disclaimer

Trajectory Lab is an educational research replication and extension project.

The controlled evaluations are designed to study specific tool-use failure modes, routing policies, recovery mechanisms, and execution trajectories.

Results should be interpreted within the scope of those experiments and not as general claims about production-scale AI-agent reliability.

---

# Author

**Lavanya Jothivel**

B.Tech — Artificial Intelligence and Data Science  
Madras Institute of Technology, Anna University

GitHub: https://github.com/Lavanya-Jothivel

---

⭐ If you find the project useful, consider starring the repository.