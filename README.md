# Automated Code Repair and Quality Enhancement Using Large Language Models

## Overview

This project introduces a hybrid automated program repair pipeline that leverages the complementary strengths of:
- **Gemini**: A powerful cloud-hosted large language model for logic-intensive and semantically rich fixes.
- **CodeT5**: A local, low-latency transformer model ideal for syntactic repairs and privacy-sensitive use cases.

The system combines structured **prompting strategies** and **entropy-based ranking** to produce high-quality code patches with minimal developer input. It is built with:
- A **Flask** backend that handles prompting, inference, entropy scoring, validation and logging.
- A **React** frontend for code input, prompt selection and output display.
- Support for Zero-Shot, Few-Shot, Chain-of-Thought (CoT) and Tree-of-Thought (ToT) prompts.

The pipeline supports automated repair of Python functions and is designed to be modular, reproducible and suitable for integration into CI/CD workflows.

## Features

- **Multi-model Support**: Switch between Gemini and CodeT5 for flexibility in logic depth, privacy and performance.
- **Prompt Engineering**: Choose from Zero-Shot, Few-Shot, CoT and ToT prompt templates.
- **Entropy-Based Ranking**: Prioritize candidate patches based on model confidence using entropy scores.
- **Two-Stage Evaluation**:
  - *Syntax Check*: Validate code structure using Python's AST.
  - *Test Suite Execution*: Ensure correctness via functional tests.

## System Architecture

```
Frontend (React) --> Backend (Flask)
                           |
             +-------------+--------------+
             |                            |
         Prompt Engine         Candidate Patch Generator
             |                            |
    Entropy Scorer                Evaluation Hub (Syntax + Test)
             \___________________________/
                          |
                    Refined Code
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- Google Gemini API key

## Setup Instructions

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

- Configure your `.env` file with:
  ```bash
  GEMINI_API_KEY=your-key-here
  ```

### 2. Frontend

```bash
cd frontend
npm install
npm start
```

## Prompting Strategies

- **Zero-Shot**: Simple instruction without examples.
- **Few-Shot**: Shows example bug-fix pairs.
- **Chain-of-Thought**: Encourages reasoning steps.
- **Tree-of-Thought**: Generates structured candidate branches.

## Entropy Scoring

- **CodeT5**: Uses token-level log-probabilities for *exact* entropy.
- **Gemini**: Uses unigram/bigram token histograms for *approximate* entropy.

Lower-entropy patches are favored, as they are more likely to be valid and correct.

## Known Limitations

- Gemini API lacks token-level probabilities (approximate entropy only).
- Not tested on large-scale or multi-file projects.
- Semantic misalignments and hallucinations still occur.
- Prompt clarity significantly affects outcome.

## Future Work

- Add support for Java, C++ and multi-file Python programs.
- Add feedback-driven prompt adaptation and reinforcement.

## Example Patch

Bug:
```python
def cube(x):
    x * x * x
```

Fix (CodeT5):
```python
def cube(x):
    return x * x * x
```

Bug:
```python
def is_even(n):
    if n % 2 == 1:
        return True
    return False
```

Fix (Gemini CoT):
```python
def is_even(n):
    if n % 2 == 0:
        return True
    return False
```
