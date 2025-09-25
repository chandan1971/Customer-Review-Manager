import axios from "axios"

const API_BASE = (import.meta.env.VITE_API_URL as string) || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
});

// Global error handler
api.interceptors.response.use(
  (res) => res,
  (err) => {
    console.error("API Error:", err.response?.data || err.message);
    return Promise.reject(err);
  }
);
