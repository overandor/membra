'use client'

import { DollarSign, Package, Calendar, Home, TrendingUp, Clock, CheckCircle, AlertTriangle } from 'lucide-react'

export default function HeroPage() {
  return (
    <main className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Hero Dashboard</h1>
          <p className="text-zinc-400">Turn your home into local income</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-zinc-900 rounded-xl p-4 border border-zinc-800">
            <div className="flex items-center gap-2 mb-2">
              <DollarSign className="w-5 h-5 text-yellow-500" />
              <span className="text-zinc-400 text-sm">This Month</span>
            </div>
            <div className="text-2xl font-bold">$347</div>
            <div className="text-green-500 text-sm">+23% vs last month</div>
          </div>

          <div className="bg-zinc-900 rounded-xl p-4 border border-zinc-800">
            <div className="flex items-center gap-2 mb-2">
              <Package className="w-5 h-5 text-yellow-500" />
              <span className="text-zinc-400 text-sm">Active Listings</span>
            </div>
            <div className="text-2xl font-bold">12</div>
            <div className="text-zinc-500 text-sm">3 pending approval</div>
          </div>

          <div className="bg-zinc-900 rounded-xl p-4 border border-zinc-800">
            <div className="flex items-center gap-2 mb-2">
              <Calendar className="w-5 h-5 text-yellow-500" />
              <span className="text-zinc-400 text-sm">Bookings Today</span>
            </div>
            <div className="text-2xl font-bold">4</div>
            <div className="text-zinc-500 text-sm">2 pickups, 2 returns</div>
          </div>

          <div className="bg-zinc-900 rounded-xl p-4 border border-zinc-800">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="w-5 h-5 text-yellow-500" />
              <span className="text-zinc-400 text-sm">Utilization</span>
            </div>
            <div className="text-2xl font-bold">67%</div>
            <div className="text-green-500 text-sm">Above average</div>
          </div>
        </div>

        {/* Hero House Status */}
        <div className="bg-gradient-to-br from-yellow-500/10 to-yellow-600/5 rounded-2xl p-6 mb-8 border border-yellow-500/20">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <Home className="w-8 h-8 text-yellow-500" />
              <div>
                <h2 className="text-xl font-bold">Hero House Status</h2>
                <p className="text-zinc-400 text-sm">Your home as a local fulfillment node</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-green-500" />
              <span className="text-green-500 font-semibold">Active</span>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-black/30 rounded-lg p-3">
              <div className="text-zinc-400 text-xs mb-1">Pickup Capacity</div>
              <div className="text-lg font-bold">8/day</div>
            </div>
            <div className="bg-black/30 rounded-lg p-3">
              <div className="text-zinc-400 text-xs mb-1">Storage Slots</div>
              <div className="text-lg font-bold">12/20</div>
            </div>
            <div className="bg-black/30 rounded-lg p-3">
              <div className="text-zinc-400 text-xs mb-1">Relay Routes</div>
              <div className="text-lg font-bold">3 active</div>
            </div>
            <div className="bg-black/30 rounded-lg p-3">
              <div className="text-zinc-400 text-xs mb-1">Trust Score</div>
              <div className="text-lg font-bold">94/100</div>
            </div>
          </div>
        </div>

        {/* Alpha Hub Eligibility */}
        <div className="bg-zinc-900 rounded-2xl p-6 mb-8 border border-zinc-800">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-xl font-bold">Alpha Hub Eligibility</h2>
              <p className="text-zinc-400 text-sm">High-volume fulfillment and storage node</p>
            </div>
            <div className="bg-yellow-500/20 text-yellow-500 px-3 py-1 rounded-full text-sm font-semibold">
              In Progress
            </div>
          </div>

          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-green-500" />
                <span>30+ completed transactions</span>
              </div>
              <span className="text-green-500">✓</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-green-500" />
                <span>95%+ trust score</span>
              </div>
              <span className="text-green-500">✓</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-green-500" />
                <span>10+ storage capacity</span>
              </div>
              <span className="text-green-500">✓</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Clock className="w-5 h-5 text-yellow-500" />
                <span>Alpha Hub application review</span>
              </div>
              <span className="text-yellow-500">Pending</span>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800">
          <h2 className="text-xl font-bold mb-4">Recent Activity</h2>
          
          <div className="space-y-4">
            <div className="flex items-center gap-4 p-3 bg-black/30 rounded-lg">
              <div className="w-10 h-10 bg-green-500/20 rounded-full flex items-center justify-center">
                <DollarSign className="w-5 h-5 text-green-500" />
              </div>
              <div className="flex-1">
                <div className="font-semibold">Payout received</div>
                <div className="text-zinc-400 text-sm">Ring Light rental - 4 hours</div>
              </div>
              <div className="text-green-500 font-bold">+$32</div>
            </div>

            <div className="flex items-center gap-4 p-3 bg-black/30 rounded-lg">
              <div className="w-10 h-10 bg-blue-500/20 rounded-full flex items-center justify-center">
                <Package className="w-5 h-5 text-blue-500" />
              </div>
              <div className="flex-1">
                <div className="font-semibold">New booking</div>
                <div className="text-zinc-400 text-sm">Storage bin - 1 week</div>
              </div>
              <div className="text-zinc-400 text-sm">Today, 2pm</div>
            </div>

            <div className="flex items-center gap-4 p-3 bg-black/30 rounded-lg">
              <div className="w-10 h-10 bg-yellow-500/20 rounded-full flex items-center justify-center">
                <AlertTriangle className="w-5 h-5 text-yellow-500" />
              </div>
              <div className="flex-1">
                <div className="font-semibold">Proof required</div>
                <div className="text-zinc-400 text-sm">Tripod return photo</div>
              </div>
              <button className="bg-yellow-500 text-black px-3 py-1 rounded-lg text-sm font-semibold">
                Upload
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
