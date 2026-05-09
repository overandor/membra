"use client";

import { useState, useEffect } from "react";

export default function HomePage() {
  const [listings, setListings] = useState<any[]>([]);
  const [chatMessage, setChatMessage] = useState("");
  const [chatResponse, setChatResponse] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [chatLoading, setChatLoading] = useState(false);

  useEffect(() => {
    fetchListings();
  }, []);

  const fetchListings = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/v1/marketplace");
      const data = await response.json();
      setListings(data.listings || []);
    } catch (error) {
      console.error("Failed to fetch listings:", error);
      // Set mock data if API is unavailable
      setListings([
        { id: 1, title: "USB-C Charger", category: "Electronics", mode: "rent", price: "$2/hr", distance: "0.2mi" },
        { id: 2, title: "Power Drill", category: "Tools", mode: "rent", price: "$7/hr", distance: "0.5mi" },
        { id: 3, title: "Storage Bin", category: "Storage", mode: "rent", price: "$3/day", distance: "0.3mi" },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChat = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatMessage.trim()) return;

    setChatLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/v1/chat/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "user_123",
          message: chatMessage,
        }),
      });
      const data = await response.json();
      setChatResponse(data.response);
      setChatMessage("");
    } catch (error) {
      console.error("Failed to send chat:", error);
      setChatResponse("I'm MEMBRA, a marketplace you talk to. You can ask me to find what you need nearby, discover what you can earn from your home, or get local recommendations.");
    } finally {
      setChatLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-black text-white">
      <section className="mx-auto max-w-7xl px-6 py-8">
        <header className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-black tracking-tight">MEMBRA</h1>
            <p className="text-sm text-gray-400">A marketplace you talk to</p>
          </div>
          <div className="flex gap-4">
            <div className="rounded-lg bg-gray-900 px-4 py-2">
              <span className="text-2xl font-bold">$42.75</span>
              <span className="text-sm text-gray-400"> balance</span>
            </div>
          </div>
        </header>

        <section className="mb-8 rounded-2xl border border-yellow-500/30 bg-gray-900/50 p-8">
          <h2 className="mb-4 text-3xl font-bold">
            What do you need, have, or want to earn from?
          </h2>
          <p className="mb-6 text-gray-400">
            Ask MEMBRA for nearby needs, local inventory, or what your home can earn from.
          </p>
          <form onSubmit={handleChat} className="flex gap-4">
            <input
              type="text"
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
              placeholder="Ask MEMBRA anything..."
              className="flex-1 rounded-lg bg-black px-4 py-3 text-white border border-gray-700 focus:border-yellow-500 focus:outline-none"
            />
            <button
              type="submit"
              className="rounded-lg bg-yellow-500 px-8 py-3 font-bold text-black hover:bg-yellow-400"
            >
              Send
            </button>
          </form>
          {chatResponse && (
            <div className="mt-4 rounded-lg bg-black/50 p-4 text-gray-300">
              {chatResponse}
            </div>
          )}
        </section>

        <section className="mb-8">
          <h3 className="mb-4 text-2xl font-bold">Available Listings</h3>
          <div className="grid gap-4 md:grid-cols-3">
            {listings.map((listing: any) => (
              <div
                key={listing.id}
                className="rounded-lg border border-gray-800 bg-gray-900/50 p-6 hover:border-yellow-500/50"
              >
                <h4 className="mb-2 text-xl font-bold">{listing.title}</h4>
                <p className="mb-2 text-gray-400">{listing.category}</p>
                <div className="mb-2 flex items-center gap-2">
                  <span className="rounded bg-yellow-500/20 px-2 py-1 text-sm text-yellow-500">
                    {listing.mode}
                  </span>
                  <span className="text-sm text-gray-400">{listing.price}</span>
                </div>
                <p className="text-sm text-gray-500">{listing.distance} away</p>
              </div>
            ))}
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-3">
          <div className="rounded-lg border border-gray-800 bg-gray-900/50 p-6">
            <h4 className="mb-2 text-lg font-bold">Your Inventory</h4>
            <p className="text-3xl font-bold text-yellow-500">2 items</p>
            <p className="text-sm text-gray-400">Available to rent</p>
          </div>
          <div className="rounded-lg border border-gray-800 bg-gray-900/50 p-6">
            <h4 className="mb-2 text-lg font-bold">Earnings This Month</h4>
            <p className="text-3xl font-bold text-green-500">$57.00</p>
            <p className="text-sm text-gray-400">From rentals</p>
          </div>
          <div className="rounded-lg border border-gray-800 bg-gray-900/50 p-6">
            <h4 className="mb-2 text-lg font-bold">Active Rentals</h4>
            <p className="text-3xl font-bold text-blue-500">3</p>
            <p className="text-sm text-gray-400">Currently active</p>
          </div>
        </section>
      </section>
    </main>
  );
}
