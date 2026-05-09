'use client';

import { useState } from 'react';

export default function HeroPage() {
  const [activeTab, setActiveTab] = useState('overview');
  const [searchQuery, setSearchQuery] = useState('');

  const tabs = [
    'overview', 'inventory', 'listings', 'requests', 'oracle', 
    'replenishment', 'hero-house', 'orders', 'compliance', 'earnings'
  ];

  const nearbyDemand = [
    { item: 'USB-C cables', searches: 47 },
    { item: 'detergent pods', searches: 32 },
    { item: 'eggs', searches: 28 },
    { item: 'vacuum access', searches: 24 },
    { item: 'storage shelf', searches: 19 }
  ];

  const suggestedStock = [
    { item: '20 USB-C cables', estimatedRevenue: '$45–$90/month', risk: 'Low' },
    { item: '12 detergent pods', estimatedRevenue: '$18–$36/month', risk: 'Low' },
    { item: '1 vacuum', estimatedRevenue: '$30–$60/month', risk: 'Low' },
    { item: '2 storage bins', estimatedRevenue: '$24–$48/month', risk: 'Low' }
  ];

  const currentListings = [
    { item: 'Couch Seat + Wi-Fi', price: '$8/hour', status: 'Active' },
    { item: 'Power Drill', price: '$5/20min', status: 'Active' },
    { item: 'Package Holding', price: '$3/day', status: 'Active' },
    { item: 'TV Access', price: '$4/hour', status: 'Pending' }
  ];

  return (
    <main className="min-h-screen bg-[#070707] text-white">
      <section className="mx-auto max-w-7xl px-6 py-8">
        <header className="mb-8 flex items-center justify-between">
          <div>
            <a href="/" className="text-2xl font-black tracking-tight text-white hover:text-amber-500 transition">
              MEMBRA
            </a>
            <p className="text-sm text-zinc-400">
              Hero Dashboard
            </p>
          </div>
          <nav className="flex gap-4">
            <a href="/" className="text-zinc-400 hover:text-white">Home</a>
            <a href="/user" className="text-amber-500 font-semibold">User App</a>
          </nav>
        </header>

        <section className="mb-8">
          <h1 className="text-3xl font-bold mb-4">What do you want to monetize today?</h1>
          <div className="flex gap-4">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search inventory, add listings, or check demand..."
              className="flex-1 px-6 py-4 rounded-xl border border-zinc-800 bg-zinc-950 text-white placeholder-zinc-500 focus:outline-none focus:border-amber-500"
            />
            <button className="px-8 py-4 bg-amber-500 hover:bg-amber-600 text-black font-bold rounded-lg transition">
              Add Listing
            </button>
          </div>
        </section>

        <nav className="flex gap-2 mb-8 overflow-x-auto pb-2">
          {tabs.map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 rounded-lg font-semibold transition whitespace-nowrap ${
                activeTab === tab 
                  ? 'bg-amber-500 text-black' 
                  : 'border border-zinc-800 text-zinc-400 hover:text-white hover:border-zinc-700'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1).replace('-', ' ')}
            </button>
          ))}
        </nav>

        {activeTab === 'overview' && (
          <div className="space-y-6">
            <section className="grid gap-6 md:grid-cols-3">
              <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
                <h3 className="text-lg font-bold mb-2">Total Earnings</h3>
                <div className="text-3xl font-black text-amber-500">$1,247.50</div>
                <div className="text-sm text-zinc-400">This month</div>
              </div>
              <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
                <h3 className="text-lg font-bold mb-2">Active Listings</h3>
                <div className="text-3xl font-black text-white">12</div>
                <div className="text-sm text-zinc-400">Across inventory</div>
              </div>
              <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
                <h3 className="text-lg font-bold mb-2">Completed Orders</h3>
                <div className="text-3xl font-black text-white">47</div>
                <div className="text-sm text-zinc-400">This month</div>
              </div>
            </section>

            <section className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
              <h3 className="text-xl font-bold mb-4">People Near You Searched For</h3>
              <div className="grid gap-3 md:grid-cols-5">
                {nearbyDemand.map((item, index) => (
                  <div key={index} className="p-3 border border-zinc-800 rounded-lg text-center">
                    <div className="font-semibold">{item.item}</div>
                    <div className="text-sm text-zinc-400">{item.searches} searches</div>
                  </div>
                ))}
              </div>
            </section>

            <section className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
              <h3 className="text-xl font-bold mb-4">Suggested Stock</h3>
              <div className="space-y-3">
                {suggestedStock.map((item, index) => (
                  <div key={index} className="flex items-center justify-between p-4 border border-zinc-800 rounded-lg">
                    <div>
                      <div className="font-semibold">{item.item}</div>
                      <div className="text-sm text-zinc-400">{item.estimatedRevenue}</div>
                    </div>
                    <div className="px-3 py-1 bg-green-500/20 text-green-500 rounded-full text-sm font-semibold">
                      {item.risk}
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-4 p-4 rounded-lg bg-amber-900/20 border border-amber-500/30">
                <div className="text-sm text-amber-300">
                  Estimated monthly revenue from suggested stock: $117–$234
                </div>
              </div>
            </section>
          </div>
        )}

        {activeTab === 'inventory' && (
          <section className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
            <h3 className="text-xl font-bold mb-4">Your Inventory</h3>
            <div className="text-center py-8 text-zinc-400">
              Inventory scanner coming soon. Use manual listing for now.
            </div>
          </section>
        )}

        {activeTab === 'listings' && (
          <section className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
            <h3 className="text-xl font-bold mb-4">Current Listings</h3>
            <div className="space-y-3">
              {currentListings.map((listing, index) => (
                <div key={index} className="flex items-center justify-between p-4 border border-zinc-800 rounded-lg">
                  <div>
                    <div className="font-semibold">{listing.item}</div>
                    <div className="text-sm text-zinc-400">{listing.price}</div>
                  </div>
                  <div className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    listing.status === 'Active' 
                      ? 'bg-green-500/20 text-green-500' 
                      : 'bg-yellow-500/20 text-yellow-500'
                  }`}>
                    {listing.status}
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {activeTab === 'earnings' && (
          <section className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
            <h3 className="text-xl font-bold mb-4">Earnings Dashboard</h3>
            <div className="grid gap-4 md:grid-cols-2">
              <div className="p-4 border border-zinc-800 rounded-lg">
                <div className="text-sm text-zinc-400 mb-1">Available for Payout</div>
                <div className="text-2xl font-bold text-amber-500">$342.50</div>
              </div>
              <div className="p-4 border border-zinc-800 rounded-lg">
                <div className="text-sm text-zinc-400 mb-1">Pending Settlement</div>
                <div className="text-2xl font-bold text-zinc-300">$127.00</div>
              </div>
            </div>
            <button className="mt-6 px-6 py-3 bg-amber-500 hover:bg-amber-600 text-black font-bold rounded-lg transition">
              Request Payout
            </button>
          </section>
        )}

        {activeTab === 'oracle' && (
          <section className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
            <h3 className="text-xl font-bold mb-4">Price Oracle</h3>
            <p className="text-zinc-400 mb-4">Compare your prices against Amazon, Temu, Alibaba, and local stores.</p>
            <div className="text-center py-8 text-zinc-400">
              Price Oracle tool coming soon.
            </div>
          </section>
        )}

        {activeTab === 'hero-house' && (
          <section className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
            <h3 className="text-xl font-bold mb-4">Hero House Status</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 border border-zinc-800 rounded-lg">
                <div>
                  <div className="font-semibold">Current Status</div>
                  <div className="text-sm text-zinc-400">Active Hero House</div>
                </div>
                <div className="px-3 py-1 bg-green-500/20 text-green-500 rounded-full text-sm font-semibold">
                  Active
                </div>
              </div>
              <div className="p-4 border border-amber-500/30 rounded-lg bg-amber-500/5">
                <div className="text-sm text-amber-300">
                  Your Hero House can become an Alpha Hub with more inventory, higher ratings, and faster fulfillment.
                </div>
              </div>
            </div>
          </section>
        )}

        {['requests', 'replenishment', 'orders', 'compliance'].includes(activeTab) && (
          <section className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
            <h3 className="text-xl font-bold mb-4 capitalize">{activeTab.replace('-', ' ')}</h3>
            <div className="text-center py-8 text-zinc-400">
              {activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} module coming soon.
            </div>
          </section>
        )}
      </section>
    </main>
  );
}
