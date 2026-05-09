const services = [
  "Ask MEMBRA",
  "Scan Room",
  "Import Amazon",
  "Rent Tools",
  "Split Bulk",
  "Relay Delivery",
  "Hero Dashboard",
  "Alpha Hub",
  "Wallet",
  "Trust",
];

export function ServiceGrid() {
  return (
    <div className="grid grid-cols-2 gap-4 md:grid-cols-5">
      {services.map((service) => (
        <button
          key={service}
          className="rounded-2xl border border-zinc-800 bg-zinc-950 p-5 text-left shadow-lg transition hover:border-amber-400/60 hover:bg-zinc-900"
        >
          <div className="mb-3 h-9 w-9 rounded-xl bg-amber-400/10 shadow-[0_0_30px_rgba(245,158,11,0.25)]" />
          <div className="font-semibold text-white">{service}</div>
          <div className="mt-1 text-xs text-zinc-500">
            Local utility layer
          </div>
        </button>
      ))}
    </div>
  );
}
