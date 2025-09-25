import { useState } from "react";
import { searchReviews, SearchResult } from "../api/search";

export default function SearchPage() {
  const [q, setQ] = useState("");
  const [results, setResults] = useState<SearchResult | null>(null);
  const [loading, setLoading] = useState(false);

  async function doSearch() {
    if (!q.trim()) return;
    setLoading(true);
    try {
      const res = await searchReviews(q, 5);
      setResults(res);
    } catch (err) {
      console.error(err);
      setResults([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Search Reviews</h1>
      <div className="flex gap-2 mb-4">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          className="border p-2 flex-1"
          placeholder="Enter query"
        />
        <button
          onClick={doSearch}
          className="bg-blue-600 text-white px-4 rounded"
        >
          Search
        </button>
      </div>

      {loading && <div>Searching...</div>}
      {!loading && results && (
        <div className="space-y-2">
          {results.map((r) => (
            <div key={r.id} className="p-3 bg-white rounded shadow">
              <div className="text-sm text-slate-500">
                Score: {r.similarity.toFixed(3)}
              </div>
              <div>{r.review_text}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
