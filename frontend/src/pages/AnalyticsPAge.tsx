import { useEffect, useState } from "react";
import { fetchAnalytics, AnalyticsResponse } from "../api/analytics";
import AnalyticsChart from "../components/AnalyticsChart";

export default function AnalyticsPage() {
  const [data, setData] = useState<AnalyticsResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics()
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading analytics...</div>;
  if (!data) return <div>No analytics available</div>;

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Analytics</h1>
      <AnalyticsChart data={data} />
    </div>
  );
}
