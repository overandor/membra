const requestExamples = [
  'I need a vacuum for 20 minutes.',
  'I need one cup of milk for a recipe.',
  'I need a tripod and ring light for a shoot.',
  'I need a couch seat with Wi-Fi for an hour.',
  'Assess my apartment and tell me what I can earn from.',
]

const responseFields = ['Item', 'Price', 'Distance', 'Deposit', 'Pickup / delivery', 'Risk level', 'Action button']

export default function AskPage() {
  return (
    <main className="min-h-screen bg-[#070707] text-white">
      <section className="mx-auto max-w-7xl px-6 py-12">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-yellow-500">MEMBRA Concierge</p>
          <h1 className="mt-3 text-4xl font-black md:text-6xl">What do you need nearby?</h1>
          <p className="mt-4 text-lg text-zinc-400">
            MEMBRA is chat-first: the requester asks for an item, ingredient, space, tool, skill, action, storage, or AI session, then the LLM returns proof-ready structured cards from approved local supply.
          </p>
        </div>

        <div className="mt-10 grid gap-8 lg:grid-cols-[1fr_0.9fr]">
          <div className="rounded-3xl border border-zinc-800 bg-zinc-950 p-5">
            <div className="rounded-2xl border border-zinc-800 bg-black p-4 text-zinc-500">Ask MEMBRA...</div>
            <div className="mt-4 space-y-3">
              {requestExamples.map((example) => (
                <div key={example} className="rounded-2xl border border-yellow-500/20 bg-yellow-500/10 p-4 text-yellow-100">
                  {example}
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-3xl border border-yellow-500/20 bg-yellow-500/10 p-6">
            <h2 className="text-2xl font-bold">LLM response contract</h2>
            <p className="mt-2 text-zinc-300">
              Each match is shown as a card with the commercial terms and safety context needed to request, accept, prove, return, settle, and review.
            </p>
            <div className="mt-6 grid grid-cols-2 gap-3">
              {responseFields.map((field) => (
                <div key={field} className="rounded-xl border border-yellow-500/20 bg-black/60 px-4 py-3 text-sm font-semibold">
                  {field}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </main>
  )
}
