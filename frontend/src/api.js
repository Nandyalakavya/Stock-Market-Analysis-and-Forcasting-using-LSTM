import axios from "axios";

const api = axios.create({
  baseURL: "https://lstm-backend-y4zf.onrender.com",
  timeout: 180000, // 3 minutes for ML prediction
});

// Fetch uploaded files
export const fetchFiles = () => api.get("/files");

// Upload CSV file
export const uploadCSV = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return api.post("/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

// Run prediction
export const runPrediction = (file, horizon) =>
  api.get("/predict", {
    params: { file, horizon },
  });

export default api;