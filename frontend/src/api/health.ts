import { api } from "./client";

export async function checkHealth(): Promise<"OK" | "DOWN"> {
  try {
    const res = await api.get("/health/");
    return res.status === 200 ? "OK" : "DOWN";
  } catch {
    return "DOWN";
  }
}
