import { useState, useCallback } from "react";

export function useApi(apiFunc) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  const request = useCallback(
    async (...args) => {
      setLoading(true);
      setError(null);

      try {
        const res = await apiFunc(...args);
        setData(res.data);
        return res.data;
      } catch (err) {
        setError(err);
        console.error("API Error:", err);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [apiFunc]
  );

  return {
    request,
    loading,
    error,
    data,
    setData,
  };
}