import axios from "axios";

const API_BASE = "http://127.0.0.1:8000/api";

export const createPlan = (data) => {
  return axios.post(`${API_BASE}/plan`, data);
};

export const getTrips = () => {
  return axios.get(`${API_BASE}/trips`);
};