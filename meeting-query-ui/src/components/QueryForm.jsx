import React, { useState } from "react";

export default function QueryForm({ setResponse }) {
  const [question, setQuestion] = useState("");
  const [company, setCompany] = useState("TRANSRAIL");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);

    try {
      const res = await fetch("https://your-api-id.execute-api.us-east-1.amazonaws.com/Prod/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, company }),
      });
      const data = await res.json();
      setResponse(data.answer || data.llm_response?.answer || "No answer found.");
    } catch (err) {
      setResponse("Error fetching answer.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl shadow max-w-2xl mx-auto">
      <div className="mb-4">
        <label className="block mb-1 font-medium">Company</label>
        <input
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          className="w-full border px-3 py-2 rounded"
          placeholder="e.g., TRANSRAIL"
        />
      </div>
      <div className="mb-4">
        <label className="block mb-1 font-medium">Your Question</label>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="w-full border px-3 py-2 rounded"
          placeholder="e.g., What were the key decisions made?"
          required
        />
      </div>
      <button
        type="submit"
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        {loading ? "Thinking..." : "Ask"}
      </button>
    </form>
  );
}
