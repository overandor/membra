import { InventoryVisionScanner } from "../../components/InventoryVisionScanner";

export default function InventoryPage() {
  return (
    <main className="min-h-screen bg-[#070707] text-white">
      <section className="mx-auto max-w-7xl px-6 py-8">
        <header className="mb-8 flex items-center justify-between">
          <div>
            <a href="/" className="text-2xl font-black tracking-tight text-white hover:text-amber-500 transition">
              MEMBRA
            </a>
            <p className="text-sm text-zinc-400">
              Inventory Scanner
            </p>
          </div>
          <nav className="flex gap-4">
            <a href="/" className="text-zinc-400 hover:text-white">Home</a>
            <a href="/hero" className="text-amber-500 font-semibold">Hero Dashboard</a>
          </nav>
        </header>

        <h1 className="text-3xl font-bold mb-4">Inventory Scanner</h1>
        <p className="text-zinc-400 mb-8">
          Use AI vision to scan and inventory your household assets automatically.
        </p>

        <InventoryVisionScanner />
      </section>
    </main>
  );
}
