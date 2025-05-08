# Automated Code Repair and Quality Enhancement Using Large Language Models

## Overview

This project provides an end-to-end example for refining code:
- A **Flask** backend orchestrates LLM calls (Gemini, CodeT5).
- A **React** frontend for users to paste code, pick prompt style, and see refined outputs.
- A minimal pipeline for compile-and-test to gauge if the patch is plausible.
- Entropy-based ranking from LLM token log-probs.

## Prerequisites

- Python 3.8+
- Node 16+ (for React)
- (Optional) A working [google-generativeai](https://pypi.org/project/google-generativeai/) setup if you have a real Gemini key.
- For local CodeT5 usage, ensure GPU for performance or be patient on CPU.

## Setup

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
