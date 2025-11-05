import { useMemo } from "react";
import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { spendMock } from "../data/mockSpend";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function DemoChart() {
  const COLORS = [
    "#402D8B", // Ollie indigo
    "#0AEBFF", // Ollie blue
    "#040404", // Ollie black
    "#EBEBEB", // Ollie gray
    "#9CA3AF", // neutral gray
  ];

  const data = useMemo(() => {
    const { labels, values } = spendMock;
    return {
      labels,
      datasets: [
        {
          data: values,
          backgroundColor: COLORS.slice(0, values.length),
          borderWidth: 0,
          hoverOffset: 6,
        },
      ],
    };
  }, []);

const options = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: "60%",
  animation: {
    animateRotate: true,
    animateScale: true,
    duration: 1200, // 1.2 seconds for a smooth draw-in
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
        color: "#111827",
        font: { size: 12, family: "ui-sans-serif, system-ui" },
      },
    },
    tooltip: {
      callbacks: {
        label(ctx) {
          return `$${Number(ctx.raw).toFixed(2)}`;
        },
      },
    },
  },
};

  const total = spendMock.values.reduce((a, b) => a + b, 0);

  return (
    <div 
    className="rounded-2xl border border-gray-200 p-6 bg-white shadow-sm transition-all duration-700 ease-out opacity-0 animate-[fadeIn_1s_forwards]"
    >
      <div className="grid gap-6 md:grid-cols-[1fr,260px] items-center">
        <div className="h-80 md:h-96 relative flex items-center justify-center">
          <Doughnut data={data} options={options} />
            {/* <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
              <span className="text-3xl font-bold text-ollie-black">${total.toFixed(2)}</span>
              <span className="text-sm text-gray-500">Total</span>
            </div> */}
        </div>
        
        <div>
          <h3 className="text-lg font-semibold mb-2">
            Spending by Category (30 days)
          </h3>
          <p className="text-sm text-gray-600 mb-4">
            Mock data showing how Ollie visualizes your expenses.
          </p>
          <div className="rounded-lg border p-4">
            <div className="text-sm text-gray-600">Total spend</div>
            <div className="text-2xl font-bold">${total.toFixed(2)}</div>
          </div>
        </div>
      </div>
    </div>
  );
}