'use client';

import { useState } from 'react';

export default function UserApp() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedResult, setSelectedResult] = useState<any>(null);

  const mockResults = [
    {
      need: 'USB-C Charger',
      localHero: { price: '$4.00', available: 'Available now', distance: '0.2 mi away' },
      rental: { price: '$1.00/day', option: 'borrow' },
      amazon: { price: '$7.99', delivery: 'Arrives tomorrow' },
      temu: { price: '$2.80', delivery: 'Arrives later' },
      alibaba: { price: '$0.70/unit', note: 'Bulk only' },
      minimumUsefulPrice: '$1.00/day borrow'
    },
    {
      need: 'Power Drill',
      localHero: { price: '$5.00', available: 'Available now', distance: '0.3 mi away' },
      rental: { price: '$2.00/20min', option: 'rent' },
      amazon: { price: '$45.99', delivery: 'Arrives tomorrow' },
      temu: { price: '$18.50', delivery: 'Arrives later' },
      alibaba: { price: '$8.00/unit', note: 'Bulk only' },
      minimumUsefulPrice: '$2.00/20min rent'
    },
    {
      need: 'One Egg',
      localHero: { price: '$0.50', available: 'Available now', distance: '0.1 mi away' },
      rental: { price: 'N/A', option: 'N/A' },
      amazon: { price: '$4.99/dozen', delivery: 'Arrives tomorrow' },
      temu: { price: '$2.50/dozen', delivery: 'Arrives later' },
      alibaba: { price: '$0.15/unit', note: 'Bulk only' },
      minimumUsefulPrice: '$0.50 buy'
    }
  ];

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // In production, this would call the API
    console.log('Searching for:', searchQuery);
  };

  return (
    <main className="min-h-screen bg-[#070707] text-white">
      <section className="mx-auto max-w-7xl px-6 py-8">
        <header className="mb-8 flex items-center justify-between">
          <div>
            <a href="/" className="text-2xl font-black tracking-tight text-white hover:text-amber-500 transition">
              MEMBRA
            </a>
            <p className="text-sm text-zinc-400">
              Find what you need nearby
            </p>
          </div>
          <nav className="flex gap-4">
            <a href="/" className="text-amber-500 font-semibold">Home</a>
            <a href="/hero" className="text-zinc-400 hover:text-white">Hero Dashboard</a>
          </nav>
        </header>

        <section className="mb-8">
          <form onSubmit={handleSearch}>
            <div className="flex gap-4">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="What do you need today?"
                className="flex-1 px-6 py-4 rounded-xl border border-zinc-800 bg-zinc-950 text-white placeholder-zinc-500 focus:outline-none focus:border-amber-500"
              />
              <button
                type="submit"
                className="px-8 py-4 bg-amber-500 hover:bg-amber-600 text-black font-bold rounded-lg transition"
              >
                Search
              </button>
            </div>
          </form>
        </section>

        {searchQuery && (
          <section className="space-y-6">
            {mockResults.map((result, index) => (
              <div key={index} className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
                <h3 className="text-2xl font-bold mb-4">{result.need}</h3>
                
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
                  <div className="p-4 border border-amber-500/30 rounded-lg bg-amber-500/5">
                    <div className="text-sm text-zinc-400 mb-1">Local Hero</div>
                    <div className="text-xl font-bold text-amber-500">{result.localHero.price}</div>
                    <div className="text-sm text-zinc-400">{result.localHero.available}</div>
                    <div className="text-sm text-zinc-400">{result.localHero.distance}</div>
                  </div>
                  
                  <div className="p-4 border border-green-500/30 rounded-lg bg-green-500/5">
                    <div className="text-sm text-zinc-400 mb-1">Rental/Fractional</div>
                    <div className="text-xl font-bold text-green-500">{result.rental.price}</div>
                    <div className="text-sm text-zinc-400">{result.rental.option}</div>
                  </div>
                  
                  <div className="p-4 border border-zinc-700 rounded-lg">
                    <div className="text-sm text-zinc-400 mb-1">Amazon</div>
                    <div className="text-xl font-bold text-zinc-300">{result.amazon.price}</div>
                    <div className="text-sm text-zinc-400">{result.amazon.delivery}</div>
                  </div>
                  
                  <div className="p-4 border border-zinc-700 rounded-lg">
                    <div className="text-sm text-zinc-400 mb-1">Temu</div>
                    <div className="text-xl font-bold text-zinc-300">{result.temu.price}</div>
                    <div className="text-sm text-zinc-400">{result.temu.delivery}</div>
                  </div>
                  
                  <div className="p-4 border border-zinc-700 rounded-lg">
                    <div className="text-sm text-zinc-400 mb-1">Alibaba</div>
                    <div className="text-xl font-bold text-zinc-300">{result.alibaba.price}</div>
                    <div className="text-sm text-zinc-400">{result.alibaba.note}</div>
                  </div>
                </div>

                <div className="mt-6 p-4 rounded-lg bg-zinc-900 border border-zinc-800">
                  <div className="text-sm text-zinc-400 mb-1">Minimum Useful Price</div>
                  <div className="text-2xl font-bold text-white">{result.minimumUsefulPrice}</div>
                </div>

                <div className="mt-6 flex flex-wrap gap-3">
                  <button className="px-6 py-3 bg-amber-500 hover:bg-amber-600 text-black font-bold rounded-lg transition">
                    Buy Nearby
                  </button>
                  <button className="px-6 py-3 border border-white/20 hover:border-white/40 text-white font-bold rounded-lg transition">
                    Rent Nearby
                  </button>
                  <button className="px-6 py-3 border border-white/20 hover:border-white/40 text-white font-bold rounded-lg transition">
                    Order Online
                  </button>
                  <button className="px-6 py-3 border border-white/20 hover:border-white/40 text-white font-bold rounded-lg transition">
                    Ask Hero to Stock
                  </button>
                  <button className="px-6 py-3 border border-amber-500/30 hover:border-amber-500/50 text-amber-500 font-bold rounded-lg transition">
                    Become a Hero for This Item
                  </button>
                </div>
              </div>
            ))}
          </section>
        )}

        {!searchQuery && (
          <section className="text-center py-16">
            <div className="text-zinc-400 mb-4">
              Search for items like: USB-C charger, drill for 20 minutes, couch seat, cook dinner
            </div>
          </section>
        )}
      </section>
    </main>
  );
}
