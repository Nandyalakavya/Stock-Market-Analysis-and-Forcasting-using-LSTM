import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
);

export default function ChartView({ data }) {
  const histLen = data.historical.length;

  const labels = [
    ...data.dates,
    ...Array(data.predicted.length).fill("")
  ];

  const chartData = {
    labels,
    datasets: [
      {
        label: "Historical",
        data: [
          ...data.historical,
          ...Array(data.predicted.length).fill(null)
        ],
        borderColor: "#a5b4fc",
        borderWidth: 2,
        tension: 0.25,

        // 🔥 IMPORTANT FIX
        pointRadius: 0,        // invisible
        pointHoverRadius: 6,   // visible on hover
        pointHitRadius: 10     // 👈 THIS ENABLES TOOLTIP
      },
      {
        label: "Predicted",
        data: [
          ...Array(histLen).fill(null),
          ...data.predicted
        ],
        borderColor: "#34d399",
        borderDash: [6, 6],
        borderWidth: 2,
        tension: 0.25,

        // 🔥 IMPORTANT FIX
        pointRadius: 0,
        pointHoverRadius: 6,
        pointHitRadius: 10
      }
    ]
  };

  const options = {
    responsive: true,
    interaction: {
      mode: "index",      // vertical guideline
      intersect: false
    },
    plugins: {
      legend: {
        position: "bottom",
        labels: {
          color: "#e5e7eb"
        }
      },
      tooltip: {
        enabled: true,
        callbacks: {
          title: (items) => items[0].label, // Date
          label: (ctx) =>
            `${ctx.dataset.label}: ${ctx.parsed.y.toFixed(2)}`
        }
      }
    },
    scales: {
      x: {
        ticks: { color: "#9ca3af" }
      },
      y: {
        ticks: { color: "#9ca3af" }
      }
    }
  };

  return <Line data={chartData} options={options} />;
}
