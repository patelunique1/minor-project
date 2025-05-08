import axios from "axios";

// Call to generate patch candidates from a selected model
export async function generatePatch(body: {
  model_name: string;
  code: string;
  language: string;
  prompt_style: string;
  num_candidates: number;
  temperature: number;
}) {
  return axios.post("/generate_patch", body);
}

export async function initModels(body: {
  gemini_api_key: string;
  together_api_key: string;
  use_codet5: boolean;
}) {
  return axios.post("/init_models", body);
}
