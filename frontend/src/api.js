import axios from "axios";

const api = axios.create({
  baseURL: "https://lstm-backend-3iht.onrender.com",
  timeout: 120000,
  headers: {
    "Content-Type": "application/json"
  }
});

// Fetch uploaded files
export const fetchFiles = () => api.get("/files");

// Upload CSV file
export const uploadCSV = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return api.post("/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });
};

// Run prediction
export const runPrediction = (file, horizon) =>
  api.get("/predict", {
    params: { file, horizon }
  });

export default api;