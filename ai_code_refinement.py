from flask import Flask, request, jsonify
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import google.generativeai as genai
import torch

app = Flask(__name__)

# -----------------------------
# Model & API Configurations
# -----------------------------
# Load a pre-trained model (e.g., CodeT5)
MODEL_NAME = "Salesforce/codet5-small"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# Configure Gemini API (ensure to keep API keys secure)
GEMINI_API_KEY = "AIzaSyAYpU979RYjHYexIJJ_RmpOsRro38IHFyg"
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

# -----------------------------
# Helper Functions for Refinement
# -----------------------------

def generate_with_model(prompt):
    """
    Uses CodeT5 to generate a refined code snippet given a prompt.
    """
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(**inputs, max_length=512)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def refine_zero_shot(code_input):
    """
    Zero-Shot prompting: Directly ask the model to refine the code.
    """
    prompt = f"Refine and improve the following code for readability, efficiency, and error-free performance:\n\n{code_input}\n"
    return generate_with_model(prompt)

def refine_few_shot(code_input):
    """
    Few-Shot prompting: Provide examples before asking the model to improve the code.
    """
    few_shot_examples = (
        "Example 1:\n"
        "Input Code: def add(a, b): return a+b\n"
        "Refined Code:\n"
        "def add(a, b):\n"
        "    # Adds two numbers\n"
        "    return a + b\n\n"
        "Example 2:\n"
        "Input Code: for i in range(10): print(i)\n"
        "Refined Code:\n"
        "for i in range(10):\n"
        "    print(i)  # Printing numbers from 0 to 9\n\n"
    )
    prompt = f"{few_shot_examples}Now, refine and improve the following code:\n\n{code_input}\n"
    return generate_with_model(prompt)

def refine_chain_of_thought(code_input):
    """
    Chain-of-Thought prompting: Instruct the model to think step-by-step.
    """
    prompt = (
        "Analyze the following code step-by-step, then provide a refined version that improves readability, "
        "efficiency, and correctness.\n"
        "Step 1: Identify any potential issues.\n"
        "Step 2: Propose improvements for clarity and performance.\n"
        "Step 3: Present the refined code.\n\n"
        f"Code:\n{code_input}\n"
    )
    return generate_with_model(prompt)

def refine_tree_of_thought(code_input):
    """
    Tree-of-Thought prompting: Ask the model to consider multiple improvement paths and select the best one.
    """
    prompt = (
        "Consider multiple improvement paths for the following code and provide the best refined version. "
        "Evaluate alternative strategies and choose the most optimal solution.\n\n"
        f"Code:\n{code_input}\n"
    )
    return generate_with_model(prompt)

def refine_rag(code_input):
    """
    Retrieval-Augmented Generation (RAG): Simulate a retrieval process to include relevant examples or hints.
    In a full implementation, this would query a code database or documentation.
    """
    # Simulate retrieval of similar code improvement examples.
    retrieved_info = (
        "Retrieved hints:\n"
        "1. Use proper indentation and comments for clarity.\n"
        "2. Optimize loops with list comprehensions if applicable.\n"
        "3. Add error handling where necessary.\n"
    )
    prompt = (
        f"Using the following retrieved information:\n{retrieved_info}\n"
        "Refine and improve the following code:\n\n"
        f"{code_input}\n"
    )
    return generate_with_model(prompt)

def refine_with_gemini(prompt):
    """
    Uses Gemini API as an alternative for code refinement.
    """
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating code with Gemini: {str(e)}"

# -----------------------------
# Flask Endpoints
# -----------------------------

@app.route('/')
def home():
    return "Welcome to the Multi-Strategy Code Refinement API!"

@app.route('/generate_zero_shot', methods=['POST'])
def generate_zero_shot():
    data = request.json
    code_input = data.get("code", "")
    refined_code = refine_zero_shot(code_input)
    return jsonify({"strategy": "zero_shot", "refined_code": refined_code})

@app.route('/generate_few_shot', methods=['POST'])
def generate_few_shot():
    data = request.json
    code_input = data.get("code", "")
    refined_code = refine_few_shot(code_input)
    return jsonify({"strategy": "few_shot", "refined_code": refined_code})

@app.route('/generate_cot', methods=['POST'])
def generate_cot():
    data = request.json
    code_input = data.get("code", "")
    refined_code = refine_chain_of_thought(code_input)
    return jsonify({"strategy": "chain_of_thought", "refined_code": refined_code})

@app.route('/generate_tot', methods=['POST'])
def generate_tot():
    data = request.json
    code_input = data.get("code", "")
    refined_code = refine_tree_of_thought(code_input)
    return jsonify({"strategy": "tree_of_thought", "refined_code": refined_code})

@app.route('/generate_rag', methods=['POST'])
def generate_rag():
    data = request.json
    code_input = data.get("code", "")
    refined_code = refine_rag(code_input)
    return jsonify({"strategy": "rag", "refined_code": refined_code})

@app.route('/generate_gemini', methods=['POST'])
def generate_gemini():
    data = request.json
    code_input = data.get("code", "")
    # A Gemini prompt can be customized with any of the strategies; here we use a simple one.
    prompt = f"Refine and improve the following code:\n\n{code_input}\n"
    refined_code = refine_with_gemini(prompt)
    return jsonify({"strategy": "gemini", "refined_code": refined_code})

# Combined endpoint to showcase all techniques together
@app.route('/generate_all', methods=['POST'])
def generate_all():
    data = request.json
    code_input = data.get("code", "")
    results = {
        "zero_shot": refine_zero_shot(code_input),
        "few_shot": refine_few_shot(code_input),
        "chain_of_thought": refine_chain_of_thought(code_input),
        "tree_of_thought": refine_tree_of_thought(code_input),
        "rag": refine_rag(code_input),
        "gemini": refine_with_gemini(f"Refine and improve the following code:\n\n{code_input}\n")
    }
    return jsonify({"results": results, "feedback": "The code has been refined using multiple strategies."})

# -----------------------------
# Main Execution
# -----------------------------
if __name__ == '__main__':
    # Use debug=True for development; remove in production
    app.run(debug=True)
