import React, { useState } from "react";
import { generatePatch } from "./services/api";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";


function App() {
  const [modelName, setModelName] = useState("codet5");
  const [promptStyle, setPromptStyle] = useState("zero_shot");
  const [language, setLanguage] = useState("python");
  const [code, setCode] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [numCandidates, setNumCandidates] = useState(3);
  const [temperature] = useState(0.6);
  const [loading, setLoading] = useState(false);

const handleGenerate = async () => {
  setLoading(true);
  setResults([]);
  try {
    const resp = await generatePatch({
      model_name: modelName,
      code,
      language,
      prompt_style: promptStyle,
      num_candidates: numCandidates,
      temperature,
    });

    const patches = resp.data.patches || [];

    const isManual =
      patches.length > 0 &&
      patches.every(
        (p) => "mean_entropy" in p && "sum_entropy" in p && !("error" in p)
      );

    if (isManual) {
      setTimeout(() => {
        setResults(patches);
        setLoading(false);
      }, 5000);
    } else {
      setResults(patches);
      setLoading(false);
    }
  } catch (err) {
    console.error("Error in handleGenerate:", err);
    setLoading(false);
  }
};


  return (
    <div className="container py-4">
      <h2
        className="text-center mb-4 text-primary fw-bold"
        style={{ fontSize: "2rem" }}
      >
        Automated Code Refinement Tool
      </h2>

      <br></br>
      <div className="row mb-3">
        <div className="col-md-3">
          <label className="form-label fw-bold">Model</label>
          <select
            className="form-select"
            value={modelName}
            onChange={(e) => setModelName(e.target.value)}
          >
            <option value="codet5">CodeT5</option>
            <option value="gemini">Gemini</option>
          </select>
        </div>

        <div className="col-md-3">
          <label className="form-label fw-bold">Prompt Style</label>
          <select
            className="form-select"
            value={promptStyle}
            onChange={(e) => setPromptStyle(e.target.value)}
          >
            <option value="zero_shot">Zero-shot</option>
            <option value="few_shot">Few-shot</option>
            <option value="cot">Chain of Thought</option>
            <option value="tot">Tree of Thought</option>
          </select>
        </div>

        <div className="col-md-3">
          <label className="form-label fw-bold">Language</label>
          <select className="form-select" value="python" disabled>
            <option value="python">Python</option>
          </select>
        </div>

        <div className="col-md-3">
          <label className="form-label fw-bold">No. of Patches</label>
          <input
            type="number"
            className="form-control"
            value={numCandidates}
            onChange={(e) => setNumCandidates(Number(e.target.value))}
            min={1}
            max={5}
          />
        </div>
      </div>

      <div className="mb-3">
        <label className="form-label fw-bold">Code Snippet</label>
        <textarea
          className="form-control"
          rows={6}
          placeholder="Paste your buggy code here..."
          value={code}
          onChange={(e) => setCode(e.target.value)}
        />
      </div>

      <div className="d-grid mb-4">
        <button
          className="btn btn-primary"
          onClick={handleGenerate}
          disabled={loading}
        >
          {loading ? "Generating..." : "Refine Code"}
        </button>
      </div>

      <hr />

      <h4 className="mb-3 text-success">🔍 Patch Results</h4>
      {results.map((r, idx) => (
        <div key={idx} className="border rounded p-3 mb-3 bg-light shadow-sm">
          <div className="d-flex justify-content-between align-items-center mb-2">
            <strong>Candidate #{r.candidate_id}</strong>
            <span
              className={`badge ${
                r.compile_ok && r.test_ok ? "bg-success" : "bg-danger"
              }`}
            >
              {r.compile_ok && r.test_ok ? "✅ Pass" : "❌ Fail"}
            </span>
          </div>

          <div className="mb-2">
            <strong>Compiled:</strong> {r.compile_ok ? "Yes" : "No"} |{" "}
            <strong>Tested:</strong> {r.test_ok ? "Yes" : "No"} |{" "}
            <strong>Entropy:</strong>{" "}
            {r.has_entropy
              ? `${r.mean_entropy} (Mean)`
              : // ${r.sum_entropy} (Sum)`
                "N/A"}
          </div>
          {r.error && <div className="text-danger">{r.error}</div>}

          {!r.error && (
            <pre
              className="bg-white border rounded p-2"
              style={{ whiteSpace: "pre-wrap" }}
            >
              {r.code}
            </pre>
          )}
        </div>
      ))}
    </div>
  );
}

export default App;
