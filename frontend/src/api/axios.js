import axios from "axios";

export const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || "http://localhost:8000",
  withCredentials: true,
  timeout: 10000,
});
