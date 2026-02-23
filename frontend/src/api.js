import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000",   
});

export const fetchFiles = () =>
  api.get("/files");

export const uploadCSV = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/upload", formData);
};

export const runPrediction = (file, horizon) =>
  api.get("/predict", {
    params: { file, horizon }
  });
