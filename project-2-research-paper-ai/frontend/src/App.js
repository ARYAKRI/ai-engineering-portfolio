import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const uploadFile = async () => {
    if (!file) return alert("Please select a PDF first!");
    
    const formData = new FormData();
    formData.append("file", file);

    await fetch("http://127.0.0.1:8000/upload-paper", {
      method: "POST",
      body: formData,
    });

    alert("PDF uploaded and indexed successfully!");
  };

  const askQuestion = async () => {
    setAnswer("Thinking..."); // Show a loading state
    const response = await fetch(
      `http://127.0.0.1:8000/ask?question=${encodeURIComponent(question)}`
    );
    const data = await response.json();
    setAnswer(data.answer);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif", maxWidth: "600px", margin: "auto" }}>
      <h1>📄 AI Research Assistant</h1>
      
      <div style={{ border: "1px solid #ccc", padding: "20px", borderRadius: "10px" }}>
        <h3>Step 1: Upload Paper</h3>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={uploadFile} style={{ marginLeft: "10px" }}>Upload</button>
      </div>

      <br />

      <div style={{ border: "1px solid #ccc", padding: "20px", borderRadius: "10px" }}>
        <h3>Step 2: Ask Anything</h3>
        <input
          type="text"
          placeholder="e.g. Who produced this journal?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          style={{ width: "70%", padding: "10px" }}
        />
        <button onClick={askQuestion} style={{ padding: "10px", marginLeft: "10px" }}>Ask AI</button>
      </div>

      {answer && (
        <div style={{ marginTop: "20px", background: "#f9f9f9", padding: "15px", borderRadius: "10px" }}>
          <strong>AI Answer:</strong>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default App; 
