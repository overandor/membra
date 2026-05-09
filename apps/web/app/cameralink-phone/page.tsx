export default function CameraLinkPhonePage() {
  return (
    <main className="min-h-screen bg-[#070707] text-white">
      <section className="mx-auto max-w-md px-6 py-8">
        <header className="mb-8 text-center">
          <div className="text-4xl mb-2">📱</div>
          <h1 className="text-2xl font-bold mb-2">MEMBRA CameraLink</h1>
          <p className="text-zinc-400 text-sm">Connected to: Hero Dashboard</p>
        </header>
        <div className="space-y-4">
          <button className="w-full rounded-2xl border border-amber-500/20 bg-zinc-950 p-6 text-left hover:border-amber-400/60 transition">
            <div className="text-3xl mb-2">📸</div>
            <div className="font-bold text-white">Start Scan</div>
            <div className="text-xs text-zinc-500">Begin live camera session</div>
          </button>
          <button className="w-full rounded-2xl border border-zinc-800 bg-zinc-950 p-6 text-left hover:border-zinc-700 transition">
            <div className="text-3xl mb-2">🖼️</div>
            <div className="font-bold text-white">Take Photo</div>
            <div className="text-xs text-zinc-500">Capture single image</div>
          </button>
          <button className="w-full rounded-2xl border border-zinc-800 bg-zinc-950 p-6 text-left hover:border-zinc-700 transition">
            <div className="text-3xl mb-2">📊</div>
            <div className="font-bold text-white">Scan Barcode</div>
            <div className="text-xs text-zinc-500">Scan product barcode</div>
          </button>
          <button className="w-full rounded-2xl border border-zinc-800 bg-zinc-950 p-6 text-left hover:border-zinc-700 transition">
            <div className="text-3xl mb-2">🧾</div>
            <div className="font-bold text-white">Upload Receipt</div>
            <div className="text-xs text-zinc-500">Import from photos</div>
          </button>
        </div>
        <button className="mt-6 w-full rounded-xl bg-zinc-800 px-4 py-3 font-bold text-white hover:bg-zinc-700">
          End Session
        </button>
      </section>
    </main>
  );
}
