import DemoChart from "./components/DemoChart";
import Hero from "./components/Hero";

export default function App() {
  return (
    <div>
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 bg-black text-white px-3 py-2 rounded"
      >
        Skip to content
      </a>

      <header className="sticky top-0 z-10 backdrop-blur bg-white/70 border-b">
        <div className="mx-auto max-w-6xl px-4 py-3 flex items-center justify-between">
          <a href="#" className="font-bold text-lg" aria-label="Ollie home">
            Ollie
          </a>
          <nav className="space-x-6 text-sm">
            <a href="#features" className="hover:underline">Features</a>
            <a href="#demo" className="hover:underline">Demo</a>
            <a href="#roadmap" className="hover:underline">Roadmap</a>
            <a href="#faq" className="hover:underline">FAQ</a>
          </nav>
        </div>
      </header>

      <main id="main">
        <Hero />

        <section id="features" className="mx-auto max-w-6xl px-4 py-16">
          <h2 className="text-2xl md:text-3xl font-semibold">Features</h2>
          <p className="mt-2 text-gray-600">We’ll wire this next.</p>
        </section>
        
        <section id="demo" className="mx-auto max-w-6xl px-4 py-16 bg-gray-50">
          <h2 className="text-2xl md:text-3xl font-semibold mb-6">Demo</h2>
          <p className="text-gray-600 mb-6">
            Here’s a peek at how Ollie helps you visualize spending.
          </p>
          <DemoChart />
        </section>

        <section id="roadmap" className="mx-auto max-w-6xl px-4 py-16">
          <h2 className="text-2xl md:text-3xl font-semibold">Roadmap</h2>
          <p className="mt-2 text-gray-600">We’ll drop the list after the chart.</p>
        </section>

        <section id="faq" className="mx-auto max-w-6xl px-4 py-16">
          <h2 className="text-2xl md:text-3xl font-semibold">FAQ</h2>
          <p className="mt-2 text-gray-600">Coming soon.</p>
        </section>
      </main>

      <footer className="border-t">
        <div className="mx-auto max-w-6xl px-4 py-8 text-sm text-gray-500 flex items-center justify-between">
          <span>© {new Date().getFullYear()} Ollie</span>
          <a href="#faq" className="hover:underline">Contact</a>
        </div>
      </footer>
    </div>
  );
}