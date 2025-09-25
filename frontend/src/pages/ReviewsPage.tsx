import { useState } from "react";
import {
  fetchReviews,
  ingestReviews,
  suggestReply,
  Review,
  ReviewFilter,
} from "../api/reviews";

export default function ReviewsPage() {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [reply, setReply] = useState<string | null>(null);

  // Filters
  const [filters, setFilters] = useState<ReviewFilter>({
    location: "",
    sentiment: "",
    q: "",
    page: 1,
    page_size: 5,
  });

  // Form state for adding multiple reviews
  const [newReviews, setNewReviews] = useState<
    { id: number | null; location: string; rating: number; text: string; date: string }[]
  >([{ id: null, location: "", rating: 0, text: "", date: "" }]);

  const loadReviews = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchReviews(filters);
      setReviews(data);
    } catch {
      setError("Failed to load reviews");
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestReply = async (id: number) => {
    if (!Number.isInteger(id)) return setError("ID must be an integer");
    setError(null);
    try {
      const res = await suggestReply(id);
      setReply(res.reply);
    } catch {
      setError("Failed to suggest reply");
    }
  };

  const handleAddReviews = async () => {
    setError(null);

    // Validate each review
    for (const r of newReviews) {
      if (r.id === null || !Number.isInteger(r.id)) return setError("Each review must have an integer ID");
      if (!r.location.trim()) return setError("All reviews must have a location");
      if (r.rating < 1 || r.rating > 5) return setError("All reviews must have rating 1-5");
      if (!r.text.trim()) return setError("All reviews must have review text");
      if (!r.date.trim()) return setError("All reviews must have a review date");
    }

    try {
      const res = await ingestReviews(newReviews);
      alert(`Inserted ${res.rows_inserted} review(s)`);
      setNewReviews([{ id: null, location: "", rating: 0, text: "", date: "" }]);
      await loadReviews();
    } catch {
      setError("Failed to add reviews");
    }
  };

  const totalPages = 10; // Replace with real total pages from API if available

  return (
    <div className="p-4 max-w-6xl mx-auto">
      <h1 className="text-2xl font-semibold mb-4">Customer Reviews</h1>

      {error && <div className="mb-4 p-2 bg-red-100 text-red-700 rounded">{error}</div>}

      {/* Filters */}
      <div className="mb-4 p-4 bg-gray-50 rounded shadow flex flex-wrap gap-2 items-end">
        <input
          type="text"
          placeholder="Location"
          className="border p-1 rounded"
          value={filters.location}
          onChange={(e) => setFilters({ ...filters, location: e.target.value })}
        />
        <select
          className="border p-1 rounded"
          value={filters.sentiment}
          onChange={(e) => setFilters({ ...filters, sentiment: e.target.value })}
        >
          <option value="">All Sentiments</option>
          <option value="POSITIVE">Positive</option>
          <option value="NEGATIVE">Negative</option>
          <option value="NEUTRAL">Neutral</option>
        </select>
        <input
          type="text"
          placeholder="Search text"
          className="border p-1 rounded"
          value={filters.q}
          onChange={(e) => setFilters({ ...filters, q: e.target.value })}
        />
        <input
          type="number"
          placeholder="Page size"
          className="border p-1 rounded"
          value={filters.page_size}
          onChange={(e) => setFilters({ ...filters, page_size: Number(e.target.value) || 5 })}
        />
        <button
          className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
          onClick={loadReviews}
        >
          {loading ? "Loading..." : "Apply Filters"}
        </button>
      </div>

      {/* Add Multiple Reviews Form */}
      <div className="mb-6 p-4 bg-gray-50 rounded shadow">
        <h2 className="text-xl font-semibold mb-2">Add Reviews</h2>
        {newReviews.map((review, idx) => (
          <div key={idx} className="flex flex-col gap-2 mb-2 p-2 border rounded">
            <input
              type="number"
              placeholder="ID (integer)"
              className="border p-1 rounded"
              value={review.id ?? ""}
              onChange={(e) =>
                setNewReviews((prev) =>
                  prev.map((r, i) => (i === idx ? { ...r, id: Number(e.target.value) } : r))
                )
              }
            />
            <input
              type="text"
              placeholder="Location"
              className="border p-1 rounded"
              value={review.location}
              onChange={(e) =>
                setNewReviews((prev) =>
                  prev.map((r, i) => (i === idx ? { ...r, location: e.target.value } : r))
                )
              }
            />
            <input
              type="number"
              placeholder="Rating (1-5)"
              className="border p-1 rounded"
              value={review.rating || ""}
              onChange={(e) =>
                setNewReviews((prev) =>
                  prev.map((r, i) => (i === idx ? { ...r, rating: Number(e.target.value) } : r))
                )
              }
              min={1}
              max={5}
            />
            <textarea
              placeholder="Review Text"
              className="border p-1 rounded"
              value={review.text}
              onChange={(e) =>
                setNewReviews((prev) =>
                  prev.map((r, i) => (i === idx ? { ...r, text: e.target.value } : r))
                )
              }
            />
            <input
              type="date"
              className="border p-1 rounded"
              value={review.date}
              onChange={(e) =>
                setNewReviews((prev) =>
                  prev.map((r, i) => (i === idx ? { ...r, date: e.target.value } : r))
                )
              }
            />
          </div>
        ))}
        <div className="flex gap-2">
          <button
            className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
            onClick={handleAddReviews}
          >
            Add Reviews
          </button>
          <button
            className="px-3 py-1 bg-gray-400 text-white rounded hover:bg-gray-500"
            onClick={() =>
              setNewReviews([
                ...newReviews,
                { id: null, location: "", rating: 0, text: "", date: "" },
              ])
            }
          >
            Add Another Review
          </button>
        </div>
      </div>

      {/* Reviews List */}
      <div className="grid gap-3">
        {reviews.map((r) => (
          <div key={r.id} className="p-3 bg-white rounded shadow cursor-pointer hover:bg-slate-50">
            <div className="flex justify-between items-center">
              <div className="text-xs text-slate-500">ID: {r.id}</div>
              <button
                className="px-2 py-0.5 bg-purple-600 text-white rounded text-xs hover:bg-purple-700"
                onClick={() => handleSuggestReply(r.id)}
              >
                Suggest Reply
              </button>
            </div>
            <div className="text-sm text-slate-500">{r.location} • Rating: {r.rating}</div>
            <div className="mt-1">{r.review_text}</div>
            <div className="mt-2 text-xs text-slate-400">Sentiment: {r.sentiment ?? "N/A"}</div>
            {r.topics && (
              <div className="text-xs text-slate-400">
                Topics: {JSON.parse(r.topics).join(", ")}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Pagination */}
      <div className="mt-4 flex gap-2">
        <button
          className="px-3 py-1 bg-gray-300 rounded hover:bg-gray-400"
          disabled={(filters?.page ?? 1) <= 1}
          onClick={() => setFilters((prev) => ({ ...prev, page: prev.page! - 1 }))}
        >
          Prev
        </button>
        <span className="px-3 py-1">{filters.page}</span>
        <button
          className="px-3 py-1 bg-gray-300 rounded hover:bg-gray-400"
          disabled={(filters?.page ?? 1) >= totalPages}
          onClick={() => setFilters((prev) => ({ ...prev, page: prev.page! + 1 }))}
        >
          Next
        </button>
        <button
          className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
          onClick={loadReviews}
        >
          Go
        </button>
      </div>

      {/* Suggested Reply */}
      {reply && (
        <div className="mt-4 p-2 bg-white border rounded shadow max-w-lg">
          <strong>Suggested Reply:</strong> {reply}
        </div>
      )}
    </div>
  );
}
