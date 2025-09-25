import { Routes, Route, Navigate } from "react-router-dom";
import ReviewsPage from "../pages/ReviewsPage";
import AnalyticsPage from "../pages/AnalyticsPAge";
import SearchPage from "../pages/SearchPage";
import HealthPage from "../pages/HealthPage";

export default function AppRoutes() {
  return (
    <Routes>
      {/* Default route → redirect to reviews */}
      <Route path="/" element={<Navigate to="/reviews" replace />} />

      {/* Pages */}
      <Route path="/reviews" element={<ReviewsPage />} />
      <Route path="/analytics" element={<AnalyticsPage />} />
      <Route path="/search" element={<SearchPage />} />
      <Route path="/health" element={<HealthPage />} />

      {/* Catch-all → redirect to reviews */}
      <Route path="*" element={<Navigate to="/reviews" replace />} />
    </Routes>
  );
}
