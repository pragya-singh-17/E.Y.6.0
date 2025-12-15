import { useState } from "react";
import { explainDecision } from "./api";

export default function ExplainButton({ payload }) {
  const [loading, setLoading] = useState(false);
  const [explanation, setExplanation] = useState(null);
  const [error, setError] = useState(null);

  const handleClick = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await explainDecision(payload);
      setExplanation(res.explanation);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "8px" }}>
      <button onClick={handleClick} disabled={loading}>
        {loading ? "Explaining…" : "Explain"}
      </button>

      {error && (
        <div style={{ color: "red", marginTop: "4px" }}>
          {error}
        </div>
      )}

      {explanation && (
        <div
          style={{
            marginTop: "8px",
            padding: "8px",
            border: "1px solid #ccc",
            background: "#f9f9f9",
          }}
        >
          {explanation}
        </div>
      )}
    </div>
  );
}
