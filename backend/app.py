from flask import Flask, request, jsonify
from prompts.base_prompt import PromptEngine
from adapters.gemini import GeminiAdapter
from adapters.hf_local import TogetherAIAdapter 
from evaluation.test_runner import TestRunner
from evaluation.compile import Compiler
from jobs.generate_patch import generate_patches_job
import traceback

app = Flask(__name__)

model_adapters = {
    "gemini": None,
    "codet5": None  
}

prompt_engine = PromptEngine()
compiler = Compiler()
test_runner = TestRunner()

@app.route("/", methods=["GET"])
def index():
    return "Welcome to Code Repair API"

@app.route("/init_models", methods=["POST"])
def init_models():
    try:
        data = request.json or {}
        gemini_api_key = data.get("gemini_api_key", "")
        together_api_key = data.get("together_api_key", "")
        use_codet5 = data.get("use_codet5", True)

        if gemini_api_key:
            model_adapters["gemini"] = GeminiAdapter(api_key=gemini_api_key)
            print("[init_models] ✅ 1Initialized")

        if use_codet5 and together_api_key:
            model_adapters["codet5"] = TogetherAIAdapter(api_key=together_api_key)
            print("[init_models] ✅ 2Initialized")

        return jsonify({"status": "initialized"}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/generate_patch", methods=["POST"])
def generate_patch():
    try:
        data = request.json
        model_name = data.get("model_name", "codet5")  # frontend still sends "codet5"
        code_snippet = data.get("code", "")
        language = data.get("language", "python")
        prompt_style = data.get("prompt_style", "zero_shot")
        num_candidates = int(data.get("num_candidates", 3))
        temperature = float(data.get("temperature", 0.6))

        if model_name not in model_adapters or not model_adapters[model_name]:
            return jsonify({"error": f"Model '{model_name}' not initialized"}), 400

        results = generate_patches_job(
            code=code_snippet,
            language=language,
            prompt_style=prompt_style,
            model_adapter=model_adapters[model_name],
            prompt_engine=prompt_engine,
            compiler=compiler,
            test_runner=test_runner,
            num_candidates=num_candidates,
            temperature=temperature
        )

        return jsonify({"patches": results}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
