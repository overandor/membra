const creationSteps = [
  'Google login',
  'Scan room / upload receipt / paste Amazon link / speak inventory',
  'LLM detects objects and actions',
  'Private inventory drafts are created',
  'Resident approves public listings',
  'Approved listings become local micro-SKUs',
]

const skuTypes = [
  ['Item', 'Vacuum, tripod, charger, extension cord'],
  ['Supply', '10 cups, tape, batteries, boxes'],
  ['Ingredient', '1 egg, 1 cup of milk'],
  ['Space', 'Couch seat, desk, shelf, fridge space'],
  ['Tool', 'Drill, ladder, ring light'],
  ['Skill', 'Setup help, delivery, cleaning, inventory scan'],
  ['Action', 'Vacuum room, stage photo corner, bring chair'],
  ['Storage', 'Closet space, shelf space, corner space'],
  ['AI session', 'Transcript, recording, livestream, proof artifact'],
]

export default function InventoryPage() {
  return (
    <main className="min-h-screen bg-[#070707] text-white">
      <section className="mx-auto max-w-7xl px-6 py-12">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-yellow-500">Inventory Brain</p>
          <h1 className="mt-3 text-4xl font-black md:text-6xl">Private inventory drafts before public supply.</h1>
          <p className="mt-4 text-lg text-zinc-400">
            MEMBRA converts household items, ingredients, spaces, tools, skills, actions, storage, and AI session artifacts into local micro-SKUs only after resident approval.
          </p>
        </div>

        <div className="mt-10 grid gap-8 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="rounded-3xl border border-yellow-500/20 bg-yellow-500/10 p-6">
            <h2 className="text-2xl font-bold">Creation flow</h2>
            <ol className="mt-6 space-y-4">
              {creationSteps.map((step, index) => (
                <li key={step} className="flex gap-4 rounded-2xl border border-yellow-500/20 bg-black/60 p-4">
                  <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-yellow-500 font-black text-black">{index + 1}</span>
                  <span className="text-zinc-100">{step}</span>
                </li>
              ))}
            </ol>
          </div>

          <div className="rounded-3xl border border-zinc-800 bg-zinc-950 p-6">
            <h2 className="text-2xl font-bold">What becomes a SKU</h2>
            <div className="mt-6 overflow-hidden rounded-2xl border border-zinc-800">
              {skuTypes.map(([asset, example]) => (
                <div key={asset} className="grid grid-cols-[0.35fr_0.65fr] border-b border-zinc-800 last:border-b-0">
                  <div className="bg-black/70 p-4 font-bold text-yellow-200">{asset}</div>
                  <div className="p-4 text-zinc-300">{example}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </main>
  )
}
