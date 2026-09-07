# TrajectoryLab Results

This file summarizes the experimental results from TrajectoryLab.

TrajectoryLab studies the reliability of tool-using language agents using controlled experiments involving ReAct-style tool use, deterministic routing, explicit failure recovery, silent-error verification, correction, abstention, and trajectory-level analysis.

The experiments are intentionally small and controlled.

Results from different task sets should not be treated as directly comparable benchmark scores.

---

# Experimental Setup

The project evaluates several agent variants:

- Direct baseline
- Mock ReAct agent
- Real-model ReAct agent
- Guarded arithmetic agent
- Guarded router
- Recovery agent
- Verification agent
- Reliable guarded agent
- Unified reliable guarded router

The real-model experiments use:

```text
Qwen/Qwen2.5-0.5B-Instruct
```

Inference is performed using Hugging Face Transformers.

The experiments were designed to run on CPU.

---

# 1. Direct Baseline vs ReAct

A small synthetic evaluation compared a limited direct-answer baseline with a ReAct-style agent.

Results:

| Method | Accuracy |
|---|---:|
| Direct Baseline | 60.00% |
| ReAct Mock Agent | 100.00% |

The ReAct agent used tool execution for supported arithmetic and factual tasks.

This experiment is a small sanity check rather than a general benchmark.

---

# 2. Real-Model ReAct Evaluation

A real-model evaluation was performed using:

```text
Qwen/Qwen2.5-0.5B-Instruct
```

The seven-task evaluation included:

- arithmetic questions
- factual lookup questions

Results:

| Metric | Result |
|---|---:|
| Tasks | 7 |
| Answer Accuracy | 100.00% |
| Correct Tool Selection Rate | 57.14% |
| Average Steps | 1.57 |
| Average Tool Calls | 0.57 |
| Error Rate | 0.00% |

The most important observation was the difference between:

```text
Answer Accuracy: 100.00%
```

and:

```text
Correct Tool Selection Rate: 57.14%
```

The language model frequently produced the correct answer directly without following the intended tool-use policy.

This shows that final-answer accuracy alone may hide execution-policy violations.

---

# 3. Tool Selection Evaluation

The real-model tool-selection evaluation measured whether the model used the expected tool.

Expected tool categories included:

```text
calculator
lookup
```

Results:

| Metric | Result |
|---|---:|
| Tasks | 7 |
| Tool Usage Rate | 57.14% |
| Correct Tool Selection Rate | 57.14% |

The model answered some questions directly instead of invoking the expected tool.

This motivated the introduction of deterministic guarded routing.

---

# 4. Raw Qwen vs Guarded Router

A controlled eight-task evaluation compared raw language-model answers with deterministic guarded routing.

The task set contained:

- arithmetic questions
- factual lookup questions

Results:

| Metric | Result |
|---|---:|
| Tasks | 8 |
| Raw Qwen Accuracy | 87.50% |
| Guarded Router Accuracy | 100.00% |
| Guard Trigger Rate | 100.00% |

One controlled arithmetic example was:

```text
What is (15 + 5) * 3?
```

In the recorded run, the raw model produced an incorrect answer.

The guarded router instead extracted the arithmetic expression and forced calculator execution.

Correct result:

```text
60
```

The result should be interpreted as an improvement in execution reliability through deterministic tool enforcement, not an improvement in the language model's underlying reasoning capability.

---

# 5. Explicit Failure Recovery

TrajectoryLab includes an unreliable calculator that deliberately produces an explicit failure.

Example:

```text
ERROR: calculator temporarily unavailable
```

For:

```text
What is (15 + 5) * 3?
```

the primary tool failed.

The recovery trajectory was:

```text
Guard
  |
  v
Unreliable Calculator
  |
  v
ERROR
  |
  v
Recovery
  |
  v
Trusted Calculator
  |
  v
60
```

The recovery mechanism successfully returned:

```text
60
```

Controlled recovery evaluation:

| Metric | Result |
|---|---:|
| Standard Agent Success | 66.67% |
| Recovery Agent Success | 100.00% |
| Recovery Events | 1 |

The injected failure is synthetic and should be interpreted as a controlled stress test.

---

# 6. Silent-Error Verification

Explicit failures are visible.

Silent errors are harder because the tool can return a plausible but incorrect result.

TrajectoryLab simulates this using a faulty calculator.

For:

```text
8 * 8
```

the faulty tool returns:

```text
63
```

The trusted calculator returns:

```text
64
```

The verification layer compares the two results.

Trajectory:

```text
Guard
  |
  v
Faulty Calculator
  |
  v
63
  |
  v
Verification
  |
  v
Trusted Result: 64
  |
  v
Correction
  |
  v
64
```

Controlled verification evaluation:

| Metric | Result |
|---|---:|
| Faulty Tool Accuracy | 66.67% |
| Verification Agent Accuracy | 100.00% |
| Correction Events | 1 |

Again, the failure is deliberately injected for controlled reliability analysis.

---

# 7. Guarded Reliability Evaluation

The guarded agent combines deterministic routing with reliability mechanisms.

It supports:

- mandatory calculator routing
- explicit failure recovery
- silent-error verification
- automatic correction
- unsupported-task abstention

A five-task controlled evaluation produced:

| Metric | Result |
|---|---:|
| Tasks | 5 |
| Accuracy | 100.00% |
| Guard Trigger Rate | 80.00% |
| Recovery Events | 1 |
| Verification Events | 1 |
| Correction Events | 1 |

The 80% guard-trigger rate occurred because one unsupported task was intentionally left unrouted.

This demonstrates that the guard is selective rather than triggering on every input.

---

# 8. Reliable Trajectory Metrics

TrajectoryLab records execution events for reliability analysis.

Possible trajectory event types include:

```text
guard
action
recovery
verification
correction
```

Results from the five-run reliability evaluation:

| Metric | Result |
|---|---:|
| Runs | 5 |
| Average Trajectory Events | 2.40 |
| Total Guard Events | 5 |
| Total Tool Actions | 4 |
| Total Recovery Events | 1 |
| Total Verification Events | 1 |
| Total Correction Events | 1 |
| Recovery Rate | 20.00% |
| Verification Rate | 20.00% |
| Correction Rate | 20.00% |

This makes execution reliability observable beyond the final answer.

---

# 9. Unified Reliable Router

The final router combines arithmetic and factual routing with all reliability mechanisms.

Supported behavior includes:

```text
deterministic routing
calculator execution
factual lookup
explicit failure detection
fallback recovery
silent-error verification
correction
abstention
trajectory logging
```

Its execution flow is:

```text
Route
  |
  v
Execute
  |
  v
Detect
  |
  +-----------------------+
  |                       |
  v                       v
Explicit Failure       Silent Fault
  |                       |
  v                       v
Recover                Verify
  |                       |
  v                       v
Fallback               Correct
  |                       |
  +-----------+-----------+
              |
              v
         Final Answer
              |
              v
       Trajectory Log
```

---

# 10. Unified Reliable Router Benchmark

The final controlled benchmark contains seven scenarios.

They cover:

- normal arithmetic
- explicit calculator failure
- silent calculator failure
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

The unsupported question was intentionally left unrouted.

The 14.29% abstention rate therefore corresponds to one of the seven test cases.

This demonstrates that the final router can choose not to invoke a tool when no supported route exists.

---

# 11. Consolidated Results

| Experiment | Result |
|---|---:|
| Direct Baseline Accuracy | 60.00% |
| Mock ReAct Accuracy | 100.00% |
| Qwen ReAct Answer Accuracy | 100.00% |
| Qwen ReAct Tool Selection Accuracy | 57.14% |
| Raw Qwen Controlled Accuracy | 87.50% |
| Guarded Router Accuracy | 100.00% |
| Reliable Guarded Benchmark Accuracy | 100.00% |
| Unified Reliable Router Accuracy | 100.00% |
| Unified Router Guard Trigger Rate | 85.71% |
| Unified Router Abstention Rate | 14.29% |
| Unified Average Trajectory Events | 2.29 |

These values come from different experimental settings.

They should not be interpreted as a single leaderboard or direct model-to-model benchmark comparison.

---

# 12. Main Research Observation

TrajectoryLab highlights the difference between:

```text
Answer Correctness
```

and:

```text
Execution Reliability
```

A model can answer correctly while failing to follow the expected tool-use policy.

The real-model experiment demonstrates this clearly:

```text
Answer Accuracy: 100.00%
Tool Selection Accuracy: 57.14%
```

This suggests that evaluating only the final answer can hide important reliability failures.

For tool-using agents, evaluation should consider both:

```text
What answer did the agent produce?
```

and:

```text
How did the agent obtain that answer?
```

---

# 13. Reliability Pipeline

The final reliability architecture can be summarized as:

```text
Route
  ->
Execute
  ->
Detect
  ->
Recover / Verify
  ->
Correct
  ->
Return
  ->
Log
```

Each stage addresses a different failure mode.

### Route

Ensures supported tasks use the expected tool.

### Execute

Runs the selected external tool.

### Detect

Identifies explicit execution failures.

### Recover

Falls back to a trusted alternative when the primary tool fails.

### Verify

Checks potentially unreliable outputs using an independent trusted computation.

### Correct

Replaces incorrect outputs when verification detects a mismatch.

### Log

Records the full execution path for trajectory-level analysis.

---

# 14. Automated Testing

The project includes unit and integration tests for:

- calculator behavior
- lookup behavior
- tool registry
- parser behavior
- ReAct execution
- recovery
- verification
- correction
- guarded routing
- reliable guarded routing
- unsupported-task abstention
- integration-level reliability behavior

Current test status:

```text
32 passed
```

Run:

```bash
python -m pytest -v
```

---

# 15. Result Artifacts

Generated result files are stored in:

```text
results/
```

Important artifacts include:

```text
baseline_results.csv
baseline_accuracy.png
baseline_comparison.csv
direct_vs_react.png

recovery_comparison.csv
recovery_success.png

verification_comparison.csv
verification_accuracy.png

reliability_summary.csv
reliability_summary.png

unified_benchmark.csv

trajectories.json
trajectory_metrics.csv
trajectory_metrics.png

real_model_eval.csv
real_model_eval.png

real_model_trajectories.json
real_trajectory_metrics.csv

tool_selection_eval.csv

real_agent_eval.csv
real_agent_accuracy.png

guarded_benchmark.csv
guarded_benchmark.png

guarded_router_benchmark.csv
guarded_router_benchmark.png

reliable_guarded_benchmark.csv
reliable_guarded_trajectories.json

reliable_trajectory_metrics.csv
reliable_trajectory_metrics.png

unified_router_benchmark.csv
unified_router_benchmark.png

ablation_summary.csv
ablation_summary.png

project_summary.csv
project_summary.json

final_results_summary.csv
final_results_summary.json
```

---

# 16. Interpretation

The strongest conclusion from the current controlled experiments is not that the system achieves universal 100% reliability.

Instead, the experiments demonstrate that explicitly designed reliability mechanisms can handle specific failure classes that unconstrained language-model execution may not handle consistently.

The project demonstrates working mechanisms for:

- tool-policy enforcement
- explicit failure recovery
- silent-error detection
- automatic correction
- selective abstention
- execution-trace analysis

---

# 17. Limitations

The current experiments have several important limitations.

They include:

- small controlled task sets
- synthetic failure injection
- small factual knowledge base
- deterministic rule-based routing
- a single small language model
- limited factual domains
- arithmetic-focused verification
- limited multi-step reasoning
- no large standardized agent benchmark
- no production external tools

Therefore, all reported percentages should be interpreted within the scope of the corresponding controlled experiment.

They should not be presented as general reliability scores for arbitrary real-world language agents.

---

# 18. Future Evaluation

Future work can strengthen the experimental evidence by adding:

- larger tool-use datasets
- standardized agent benchmarks
- multiple language models
- semantic tool routing
- dynamic tool registries
- larger retrieval systems
- random tool outages
- stochastic incorrect tool responses
- adversarial tool outputs
- multi-step task trajectories
- latency measurements
- token-cost measurements
- confidence-aware verification
- automated trajectory anomaly detection

---

# 19. Reproducibility

The repository stores:

- source code
- experiment scripts
- tests
- CSV outputs
- JSON trajectories
- plots
- consolidated summaries

This allows the individual controlled experiments to be reproduced independently.

---

# Reference

Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023).

**ReAct: Synergizing Reasoning and Acting in Language Models.**

International Conference on Learning Representations (ICLR).

Paper:

https://arxiv.org/abs/2210.03629

---

# Result Disclaimer

TrajectoryLab is a research and educational replication project.

The reported results validate the implemented mechanisms on the corresponding controlled experiments.

They are not intended to claim state-of-the-art performance or general 100% reliability across real-world agent systems.