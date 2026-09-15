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

export const register = (credentials) => {
  return axios.post(`${API_BASE}/auth/register`, credentials);
};

export const getCurrentUser = () => {
  return axios.get(`${API_BASE}/auth/me`);
};

export const logout = () => {
  return axios.post(`${API_BASE}/auth/logout`);
};

export const createPlan = (data) => {
  return axios.post(`${API_BASE}/planner/plan`, data);
};

export const getTrips = () => {
  return axios.get(`${API_BASE}/planner/trips`);
};

export const getTripById = (tripId) => {
  return axios.get(`${API_BASE}/planner/trips/${tripId}`);
};

export const deleteTrip = (tripId) => {
  return axios.delete(`${API_BASE}/planner/trips/${tripId}`);
};

export async function sendChatMessage(payload) {
  const response = await axios.post(
    `${API_BASE}/planner/plan/chat`,
    payload
  );

  return response.data;
}