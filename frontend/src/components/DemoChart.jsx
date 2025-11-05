import { Doughnut } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";
import { spendMock } from "../data/mockSpend";
import { useEffect, useMemo, useState } from "react";

ChartJS.register(ArcElement, Tooltip, Legend);


export default function DemoChart() {

  const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

  const [items, setItems] = useState([]);     // [{ category, amount }]
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_URL}/api/expenses`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        // Expecting: [{ category: "Food", amount: 124.5 }, ...]
        if (!cancelled) setItems(Array.isArray(data) ? data : []);
      } catch (e) {
        if (!cancelled) setError(e.message || "Failed to load");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => { cancelled = true; };
  }, [API_URL]);

  // Ollie brand-ish palette (adjust if needed)
  const COLORS = [
    "#402D8B", // indigo
    "#0AEBFF", // blue
    "#040404", // black (use sparingly)
    "#EBEBEB", // gray
    "#9CA3AF", // neutral gray
  ];

  const labels = useMemo(() => items.map(i => i.category), [items]);
  const values = useMemo(() => items.map(i => Number(i.amount || 0)), [items]);
  const total = useMemo(() => values.reduce((a, b) => a + b, 0), [values]);

  // Build chart data from mock
  const data = useMemo(() => ({
  labels,
  datasets: [
    {
      data: values.length ? values : [1],     // avoid empty dataset crash
      backgroundColor: (values.length ? COLORS.slice(0, values.length) : ["#EBEBEB"]),
      borderWidth: 0,
      hoverOffset: 6,
    },
  ],
}), [labels, values]);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: "60%",
    animation: {
      animateRotate: true,
      animateScale: true,
      duration: 1200,
      easing: "easeOutQuart",
    },
    plugins: {
      legend: {
        display: true,
        position: "right",
        labels: {
          usePointStyle: true,
          pointStyle: "circle",
          boxWidth: 8,
          padding: 12,
          color: "#111827",
          font: { size: 12, family: "ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial" },
        },
      },
      tooltip: {
        callbacks: {
          label(ctx) {
            const label = ctx.label || "";
            const value = ctx.raw ?? 0;
            return `${label}: $${Number(value).toFixed(2)}`;
          },
        },
      },
    },
  };

  return (
    <div className="rounded-2xl border border-gray-200 p-6 bg-white shadow-sm">
      <div className="grid gap-6 md:grid-cols-[1fr,260px] items-center">
        <div className="h-80 md:h-96 flex items-center justify-center">
          <Doughnut data={data} options={options} aria-label="Spending by category chart" />
        </div>

        <div className="space-y-2">
          <h3 className="text-lg font-semibold">Spending by Category (30 days)</h3>
          <p className="text-sm text-gray-600">
            Quick snapshot of where money went. Categories and amounts are mock data for the demo.
          </p>
          <div className="mt-4 rounded-xl border p-4">
            <div className="text-sm text-gray-600">Total spend</div>
            <div className="text-2xl font-bold">${total.toFixed(2)}</div>
          </div>
        </div>
      </div>
    </div>
  );
}