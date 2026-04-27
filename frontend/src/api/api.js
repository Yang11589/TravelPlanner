import axios from "axios";

const API_BASE = "http://127.0.0.1:8000/api";

// Add request interceptor to include auth token
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    // Only add Authorization header if token exists and is not 'undefined'
    if (token && token !== "undefined") {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const login = (credentials) => {
  return axios.post(`${API_BASE}/auth/login`, credentials);
};

export const createPlan = (data) => {
  return axios.post(`${API_BASE}/plan`, data);
};

export const getTrips = () => {
  return axios.get(`${API_BASE}/trips`);
};