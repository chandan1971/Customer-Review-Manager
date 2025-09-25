import { api } from "./client";

export type Review = {
  id: number;
  location: string;
  rating: number;
  review_text: string;
  review_date: string;
  sentiment?: string;
  topics?: string; 
};

export type ReviewFilter = {
  location?: string;
  sentiment?: string;
  q?: string;
  page?: number;
  page_size?: number;
};

 export type newReviews= {
    id: number | null;
    location: string;
    rating: number;
    text: string;
    date: string;
};

export async function fetchReviews(filters?: ReviewFilter): Promise<Review[]> {
  const params: Record<string, any> = {};
  if (filters) {
    for (const key in filters) {
      const value = filters[key as keyof ReviewFilter];
      if (value !== undefined && value !== null && value !== "") {
        params[key] = value;
      }
    }
  }

  const res = await api.get("/reviews", { params });
  return Array.isArray(res.data.reviews) ? res.data.reviews : [];
}


export async function fetchReviewById(id: number): Promise<Review> {
  const res = await api.get(`/reviews/${id}`);
  return res.data.review;
}

export async function ingestReviews(reviews: newReviews[]): Promise<{ rows_inserted: number }> {
  reviews.forEach((r) => {
    if (!Number.isInteger(r.id)) {
      throw new Error(`Invalid review id: ${r.id}. ID must be an integer.`);
    }
  });

  const res = await api.post("/reviews/ingest", reviews);
  return res.data;
}

export async function suggestReply(id: number): Promise<{ reply: string }> {
  const res = await api.get(`/reviews/${id}/suggest-reply`);
  return res.data;
}
