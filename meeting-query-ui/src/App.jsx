import React, { useState } from "react";
import QueryForm from "./components/QueryForm";

export default function App() {
  const [response, setResponse] = useState(null);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-6 text-center">Meeting Intelligence Assistant</h1>
      <QueryForm setResponse={setResponse} />
      {response && (
        <div className="mt-8 bg-white p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-2">Answer</h2>
          <p className="text-gray-800 whitespace-pre-wrap">{response}</p>
        </div>
      )}
    </div>
  );
}
