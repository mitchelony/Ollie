export default function Hero() {
  return (
    <section
      className="mx-auto max-w-6xl px-4 pt-16 pb-20 md:pt-24"
      aria-labelledby="hero-title"
    >
      <div className="grid gap-10 md:grid-cols-2 md:items-center">
        <div>
          <h1
            id="hero-title"
            className="text-ollie-black text-4xl md:text-5xl font-bold leading-tight tracking-tight"
          >
            Money help that talks like a friend, not a bank.
          </h1>

          <p className="mt-4 text-gray-600 text-base md:text-lg">
            Ollie helps students build healthy money habits with simple tracking,
            clear visuals, and gentle nudges—no jargon, no overwhelm.
          </p>

          <div className="mt-6 flex flex-col sm:flex-row gap-3">
            <a
              href="#demo"
              className="inline-flex items-center justify-center px-5 py-3 rounded-lg bg-black text-white hover:opacity-90 transition hover:scale-105 transition-transform"
              aria-label="See the spending demo section"
            >
              See the demo
            </a>
            <a
              href="#features"
              className="inline-flex items-center justify-center px-5 py-3 rounded-lg border border-gray-300 hover:bg-gray-50 transition hover:scale-105 transition-transform"
            >
              Learn more
            </a>
          </div>

          <p className="mt-3 text-xs text-gray-500">
            Private by default. Your data stays yours.
          </p>
        </div>

        <div className="rounded-2xl border border-gray-200 p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-900">This month</span>
            <span className="text-xs text-gray-500">sample data</span>
          </div>

          <ul className="mt-4 space-y-3 text-sm">
            <li className="flex justify-between">
              <span>Food</span><span className="font-medium">$124.50</span>
            </li>
            <li className="flex justify-between">
              <span>Transport</span><span className="font-medium">$48.20</span>
            </li>
            <li className="flex justify-between">
              <span>Subscriptions</span><span className="font-medium">$19.99</span>
            </li>
            <li className="flex justify-between">
              <span>Uni Supplies</span><span className="font-medium">$36.00</span>
            </li>
          </ul>

          <div className="mt-6 flex items-center justify-between border-t pt-4">
            <span className="text-sm text-gray-600">Total spend</span>
            <span className="text-base font-semibold">$228.69</span>
          </div>
        </div>
      </div>
    </section>
  );
}