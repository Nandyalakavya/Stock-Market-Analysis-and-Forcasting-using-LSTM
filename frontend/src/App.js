import { useEffect, useState } from "react";
import { fetchFiles, uploadCSV, runPrediction } from "./api";
import UploadPanel from "./components/UploadPanel";
import ChartView from "./components/ChartView";

export default function App() {
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState("");
  const [horizon, setHorizon] = useState("6m");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  
  const loadFiles = () => {
    fetchFiles()
      .then(res => setFiles(res.data))
      .catch(err => {
        console.error("Error loading files:", err);
        alert("Backend not reachable");
      });
  };

  useEffect(() => {
    loadFiles();
  }, []);

 
  const handleUpload = (file) => {
    if (!file) return;

    uploadCSV(file)
      .then(() => {
        alert("CSV uploaded successfully");
        loadFiles(); 
      })
      .catch(err => {
        console.error("Upload error:", err);
        alert("CSV upload failed");
      });
  };

 
  const handleRunPrediction = () => {
    if (!selectedFile) {
      alert("Please select a CSV file first");
      return;
    }

    setLoading(true);
    setData(null);

    runPrediction(selectedFile, horizon)
      .then(res => {
        setData(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Prediction error:", err);
        alert(err.response?.data?.error || "Prediction failed");
        setLoading(false);
      });
  };

  
  return (
    <div className="container">
      <h1>Market Insights AI</h1>
      <div className="subtitle">
        Upload stock CSV, choose horizon, and view LSTM predictions
      </div>

      <div className="main-grid">
        
        <div className="panel">
          <UploadPanel
            files={files}
            onUpload={handleUpload}
            onSelect={setSelectedFile}
          />

          <h3>Prediction Horizon</h3>
          <select value={horizon} onChange={e => setHorizon(e.target.value)}>
            <option value="6m">6 months</option>
            <option value="1y">1 year</option>
            <option value="2y">2 years</option>
            <option value="3y">3 years</option>
            <option value="5y">5 years</option>
          </select>

          <button
            onClick={handleRunPrediction}
            disabled={!selectedFile || loading}
          >
            {loading ? "Predicting..." : "Run Prediction"}
          </button>

          {data && (
            <div className="metrics">
              <p>RMSE: {data.metrics.rmse}</p>
              <p>MAE: {data.metrics.mae}</p>
              <p>R²: {data.metrics.r2}</p>
              <p>Profit/Loss (%): {data.metrics.profit_loss}</p>
            </div>
          )}
        </div>

        <div className="chart-panel">
          {loading && <p>Running LSTM prediction...</p>}
          {data && <ChartView data={data} />}
        </div>
      </div>
    </div>
  );
}
