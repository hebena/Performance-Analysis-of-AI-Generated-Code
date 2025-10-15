# Replication package for: Performance Analysis of AI-Generated Code: A Case Study of Copilot, Copilot Chat, CodeLlaMa, and DeepSeek-Coder Models

## Structure of the Project

This replication package contains four main folders:

### 1. **data/**
Contains the datasets and static analysis rules used in the study.

- **datasets/**
  - `humaneval-v2-20210705.jsonl` - HumanEval dataset
  - `mbpp.jsonl` - MBPP (Mostly Basic Python Problems) dataset
  - `evalperf_dataset.jsonl` - EvalPerf dataset
  - `aixbench_dataset_autotest_nl.jsonl` - AIxBench dataset

- **rules/**
  - `pmd_rules.xml` - PMD static analysis rules

### 2. **result/**
Contains the experimental results for the four models (Copilot, Copilot Chat, CodeLlaMa, and DeepSeek-Coder).

- **critical_path/**

  Critical path analysis results for scripts showing performance regression across four models.
  - `humaneval/` - Critical path results for HumanEval dataset
  - `mbpp/` - Critical path results for MBPP dataset
  - `evalperf/` - Critical path results for EvalPerf dataset

- **dynamic_output/**

  Dynamic execution results for the four models.
  - `original/` - Results from original prompts
  - `cot_prompt/` - Results from Chain-of-Thought prompt engineering
  - `few_shot_prompt/` - Results from few-shot prompt engineering

### 3. **root causes/**
Root cause analysis performed by two independent authors.
- `author1.xlsx` - Root cause analysis by author 1
- `author2.xlsx` - Root cause analysis by author 2

### 4. **scripts/**
Scripts for calculating performance metrics.
- `runtime.py` - Script to measure execution time using cProfile
- `memory.py` - Script to measure memory usage using tracemalloc
- `cpu.py` - Script to measure CPU utilization using cProfile and Psutil