import { useMemo } from "react";
import { Doughnut } from "react-chartjs-2";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

import { spendMock } from "../data/mockSpend";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function DemoChart() {
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: "60%", // donut hole size
    plugins: {
      legend: {
        display: true,
        position: "right",
        labels: {
          usePointStyle: true,
          pointStyle: "circle",
          boxWidth: 8,
          padding: 12,
          // Keep legend readable
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

  // Sum for the center label (nice touch)
  const total = spendMock.values.reduce((a, b) => a + b, 0);

  return (
    <div className="rounded-2xl border border-gray-200 p-6">
      <div className="grid gap-6 md:grid-cols-[1fr,260px] items-center">
        <div className="h-80 md:h-96">
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