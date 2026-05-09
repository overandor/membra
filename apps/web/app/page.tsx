'use client'

import { useState } from 'react'
import { Search, ArrowRight, Sparkles, TrendingUp, Package, Home as HomeIcon, Truck, BookOpen, DollarSign, Shield, Store, Users } from 'lucide-react'
import Link from 'next/link'

const services = [
  { id: 'rent', name: 'Rent', icon: Package, color: 'from-blue-500/20 to-blue-600/10', description: 'Borrow items nearby' },
  { id: 'buy', name: 'Buy', icon: DollarSign, color: 'from-green-500/20 to-green-600/10', description: 'Purchase locally' },
  { id: 'split', name: 'Split', icon: Users, color: 'from-purple-500/20 to-purple-600/10', description: 'Group purchases' },
  { id: 'store', name: 'Store', icon: Store, color: 'from-orange-500/20 to-orange-600/10', description: 'Storage space' },
  { id: 'access', name: 'Access', icon: HomeIcon, color: 'from-cyan-500/20 to-cyan-600/10', description: 'On-site use' },
  { id: 'move', name: 'Move', icon: Truck, color: 'from-red-500/20 to-red-600/10', description: 'Relay delivery' },
  { id: 'book', name: 'Book', icon: BookOpen, color: 'from-pink-500/20 to-pink-600/10', description: 'Reserve time' },
  { id: 'supply', name: 'Supply', icon: Package, color: 'from-yellow-500/20 to-yellow-600/10', description: 'Sell inventory' },
  { id: 'earn', name: 'Earn', icon: TrendingUp, color: 'from-emerald-500/20 to-emerald-600/10', description: 'Hero Dashboard' },
  { id: 'trust', name: 'Trust', icon: Shield, color: 'from-indigo-500/20 to-indigo-600/10', description: 'Proof & reputation' },
]

export default function Home() {
  const [query, setQuery] = useState('')

  return (
    <main className="min-h-screen bg-black">
      <div className="max-w-7xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Sparkles className="w-8 h-8 text-yellow-500" />
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-yellow-400 to-yellow-600 bg-clip-text text-transparent">
              MEMBRA
            </h1>
          </div>
          <p className="text-xl text-zinc-400 mb-2">A marketplace you talk to</p>
          <p className="text-zinc-500">Need nearby. Earn locally.</p>
        </div>

        <div className="max-w-2xl mx-auto mb-12">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-zinc-500" />
            <input
              type="text"
              placeholder="What do you need, have, or want to earn from?"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full bg-zinc-900 border border-zinc-800 rounded-2xl py-4 pl-12 pr-4 text-white placeholder-zinc-500 focus:outline-none focus:border-yellow-500 transition-colors"
            />
            <button className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-yellow-500 text-black px-4 py-2 rounded-xl font-semibold hover:bg-yellow-400 transition-colors">
              Ask MEMBRA
            </button>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-12">
          {services.map((service) => {
            const Icon = service.icon
            return (
              <Link
                key={service.id}
                href={`/${service.id === 'earn' ? 'hero' : service.id}`}
                className={`group relative bg-gradient-to-br ${service.color} rounded-2xl p-6 border border-zinc-800 hover:border-yellow-500/50 transition-all duration-200`}
              >
                <div className="flex flex-col items-center text-center">
                  <div className="w-12 h-12 rounded-xl bg-zinc-900 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                    <Icon className="w-6 h-6 text-yellow-500" />
                  </div>
                  <h3 className="font-semibold text-white mb-1">{service.name}</h3>
                  <p className="text-xs text-zinc-400">{service.description}</p>
                </div>
                <ArrowRight className="absolute bottom-4 right-4 w-4 h-4 text-zinc-600 group-hover:text-yellow-500 group-hover:translate-x-1 transition-all opacity-0 group-hover:opacity-100" />
              </Link>
            )
          })}
        </div>

        <div className="max-w-4xl mx-auto">
          <div className="grid md:grid-cols-3 gap-4">
            <Link href="/scan" className="bg-gradient-to-br from-yellow-500/10 to-yellow-600/5 rounded-2xl p-6 border border-yellow-500/20 hover:border-yellow-500/50 transition-colors">
              <div className="flex items-center gap-3 mb-2">
                <CameraIcon className="w-6 h-6 text-yellow-500" />
                <h3 className="font-semibold text-white">Scan Your Home</h3>
              </div>
              <p className="text-zinc-400 text-sm">Take photos. MEMBRA creates listings.</p>
            </Link>

            <Link href="/marketplace" className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800 hover:border-zinc-700 transition-colors">
              <div className="flex items-center gap-3 mb-2">
                <Package className="w-6 h-6 text-yellow-500" />
                <h3 className="font-semibold text-white">Browse Marketplace</h3>
              </div>
              <p className="text-zinc-400 text-sm">Find what you need nearby.</p>
            </Link>

            <Link href="/hero" className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800 hover:border-zinc-700 transition-colors">
              <div className="flex items-center gap-3 mb-2">
                <TrendingUp className="w-6 h-6 text-yellow-500" />
                <h3 className="font-semibold text-white">Hero Dashboard</h3>
              </div>
              <p className="text-zinc-400 text-sm">Track earnings and listings.</p>
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8 border-t border-zinc-900">
        <p className="text-center text-zinc-600 text-sm">
          MEMBRA turns every apartment into the nearest warehouse, every useful object into a potential SKU, and every chat into a path from need into income.
        </p>
      </div>
    </main>
  )
}

function CameraIcon({ className }: { className: string }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z" />
      <circle cx="12" cy="13" r="3" />
    </svg>
  )
}
