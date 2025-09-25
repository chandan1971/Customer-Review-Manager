import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Legend, Tooltip } from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, BarElement, Legend, Tooltip);

type Props = {
  data: Record<string, Record<string, number>>;
};

export default function AnalyticsChart({ data }: Props) {
  const labels = Object.keys(data);
  const sentiments = ["POSITIVE", "NEGATIVE", "NEUTRAL"];

  const datasets = sentiments.map((s, idx) => ({
  label: s, 
  data: labels.map((l) => data[l]?.[s] ?? 0),
  backgroundColor: ["#4caf50", "#900d03ff", "#ff9800"][idx],
  minBarLength: 5
}));
  return (
    <div className="bg-white p-4 rounded shadow">
      <Bar
        data={{ labels, datasets }}
        options={{
          responsive: true,
          plugins: { legend: { position: "top" } },
          scales: { x: { stacked: false }, y: { beginAtZero: true } }
        }}
      />
    </div>
  );
}
