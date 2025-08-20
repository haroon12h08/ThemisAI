import React, { useState } from "react";
import axios from "axios";

function App() {
  const [chequeFile, setChequeFile] = useState(null);
  const [signatureFile, setSignatureFile] = useState(null);
  const [chequeData, setChequeData] = useState(null);
  const [similarity, setSimilarity] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChequeUpload = (e) => setChequeFile(e.target.files[0]);
  const handleSignatureUpload = (e) => setSignatureFile(e.target.files[0]);

  // ✅ Proper submit handler
  const handleSubmit = async () => {
    if (!chequeFile || !signatureFile) {
      alert("Please upload both cheque and signature images.");
      return;
    }

    const formData = new FormData();
    formData.append("cheque", chequeFile);
    formData.append("signature", signatureFile);

    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/api/cheque/extract",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      if (response.data.status === "success") {
        setChequeData(response.data.details);
        setSimilarity(response.data.signature_match_score);
      } else {
        alert("Backend error: " + response.data.message);
      }
    } catch (err) {
      console.error("Request failed:", err.response ? err.response.data : err.message);
      alert("Network or server error.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-black text-gold-500 p-6">
      <h1 className="text-3xl font-bold mb-6 text-gold-400">Cheque Fraud Detection</h1>

      <div className="bg-gray-900 shadow-lg rounded-xl p-6 w-full max-w-md border border-gold-500">
        <label className="block mb-4">
          <span className="font-medium text-gold-300">Upload Cheque Image:</span>
          <input type="file" accept="image/*" onChange={handleChequeUpload} className="mt-2 text-white" />
        </label>

        <label className="block mb-4">
          <span className="font-medium text-gold-300">Upload Signature Image:</span>
          <input type="file" accept="image/*" onChange={handleSignatureUpload} className="mt-2 text-white" />
        </label>

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full bg-gold-500 text-black font-bold py-2 rounded-lg hover:bg-gold-400 transition disabled:bg-gray-600"
        >
          {loading ? "Processing..." : "Submit"}
        </button>

        {chequeData && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold mb-2 text-gold-400">Cheque Details</h2>
            <div className="space-y-2 text-gold-200">
              <p><b>Payee:</b> {chequeData.payee || "Not detected"}</p>
              <p><b>Amount (Words):</b> {chequeData.amount_words || "Not detected"}</p>
              <p><b>Amount (Digits):</b> {chequeData.amount_digits || "Not detected"}</p>
              <p><b>Date:</b> {chequeData.date || "Not detected"}</p>
              <p><b>IFSC:</b> {chequeData.ifsc || "Not detected"}</p>
              <p><b>MICR:</b> {chequeData.micr || "Not detected"}</p>
            </div>
          </div>
        )}

        {similarity !== null && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold mb-2 text-gold-400">Signature Match Score</h2>
            <p className="text-lg text-gold-300">{similarity.toFixed(2)}%</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
