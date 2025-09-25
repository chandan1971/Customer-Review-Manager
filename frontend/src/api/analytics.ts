import { api } from "./client";

export type AnalyticsResponse = Record<
  string,
  { Positive: number; Negative: number; Neutral: number }
>;

export async function fetchAnalytics(): Promise<AnalyticsResponse> {
  const res = await api.get("/analytics/");
  // backend returns { analytics: {...} }
  return res.data.analytics ?? res.data;
}
