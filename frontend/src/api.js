const API_BASE = "http://localhost:8000";

export async function explainDecision(payload) {
  const res = await fetch(`${API_BASE}/explain`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (res.status === 429) {
    throw new Error("Rate limit exceeded. Please wait.");
  }

  if (!res.ok) {
    throw new Error("Failed to generate explanation");
  }

  return res.json(); // { explanation: string }
}
