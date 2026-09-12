import axios from "axios";

// Set VITE_API_BASE_URL in a .env file when deploying; defaults to local FastAPI dev server.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
});

/**
 * Sends subject/body to the FastAPI /predict endpoint.
 * Throws an Error with a human-readable message on failure.
 */
export async function predictEmail(subject, body) {
  try {
    const response = await client.post("/predict", { subject, body });
    return response.data;
  } catch (err) {
    if (err.response) {
      // FastAPI validation errors come back as an array under `detail`
      const detail = err.response.data?.detail;
      if (Array.isArray(detail)) {
        const message = detail.map((d) => d.msg).join(", ");
        throw new Error(message || "Invalid input.");
      }
      throw new Error(detail || `Request failed (${err.response.status}).`);
    }
    if (err.request) {
      throw new Error(
        "Could not reach the backend. Is the FastAPI server running on " +
          API_BASE_URL +
          "?"
      );
    }
    throw new Error(err.message || "Something went wrong.");
  }
}
