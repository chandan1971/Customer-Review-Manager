import { api } from "./client";

export type SearchResult = {
  id: number;
  review_text: string;
  similarity: number;
}[];

export async function searchReviews(q: string, k = 5): Promise<SearchResult> {
  const res = await api.get("/search", { params: { q, k } });
  return res.data;
}
