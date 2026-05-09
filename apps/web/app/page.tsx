'use client'

import { useState } from 'react'
import Link from 'next/link'
import {
  ArrowRight,
  DollarSign,
  Home as HomeIcon,
  Package,
  Search,
  Shield,
  Sparkles,
  Store,
  TrendingUp,
  Truck,
  Users,
} from 'lucide-react'

const exampleRequests = [
  'I need a vacuum for 20 minutes.',
  'I need one cup of milk for a recipe.',
  'I need a tripod and ring light for a shoot.',
  'I need a couch seat with Wi-Fi for an hour.',
  'Assess my apartment and tell me what I can earn from.',
]

const marketplaceModes = [
  { name: 'Sell', description: 'Approved household supplies and micro-SKUs', href: '/marketplace', icon: DollarSign },
  { name: 'Rent', description: 'Tools, gear, appliances, and short-use items', href: '/marketplace', icon: Package },
  { name: 'Split', description: 'Ingredients, boxes, batteries, tape, and bulk buys', href: '/split-order', icon: Users },
  { name: 'Store', description: 'Shelf, closet, fridge, and corner space', href: '/inventory', icon: Store },
  { name: 'Access', description: 'Couch seat, desk, room, Wi-Fi, and creator setup', href: '/ask', icon: HomeIcon },
  { name: 'Help', description: 'Setup, cleaning, organizing, repair, and scans', href: '/hero', icon: Sparkles },
  { name: 'Deliver', description: 'Runner pickup, drop-off, and meet-halfway flow', href: '/relay', icon: Truck },
  { name: 'Assess', description: 'Private earning analysis before anything goes public', href: '/scan', icon: TrendingUp },
]

const operatorModules = [
  ['Inventory Brain', 'Turns photos, receipts, links, voice, and shelves into local SKUs.'],
  ['Concierge', 'Understands nearby requests and clarifies what is needed.'],
  ['Risk Filter', 'Blocks unsafe, regulated, private, or high-liability categories.'],
  ['Matchmaker', 'Matches demand to supply, substitutes, helpers, and runners.'],
]

const structuredCards = [
  { item: 'Cordless vacuum', price: '$4 / 20 min', distance: '2 floors away', deposit: '$25 hold', risk: 'Low', action: 'Request rental' },
  { item: 'Couch seat + Wi-Fi', price: '$9 / hour', distance: '0.2 mi', deposit: 'No deposit', risk: 'Medium', action: 'Book access' },
  { item: 'Inventory scan helper', price: '$18 flat', distance: 'In-building', deposit: 'Proof photo', risk: 'Low', action: 'Hire helper' },
]

export default function Home() {
  const [query, setQuery] = useState('')

  return (
    <main className="min-h-screen overflow-hidden bg-black text-white">
      <section className="relative mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="absolute inset-x-0 top-0 -z-10 mx-auto h-96 max-w-4xl rounded-full bg-yellow-500/10 blur-3xl" />

        <div className="mx-auto max-w-4xl text-center">
          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-yellow-500/30 bg-yellow-500/10 px-4 py-2 text-sm font-medium text-yellow-300">
            <Shield className="h-4 w-4" />
            Private by default. Public only by approval.
          </div>
          <div className="mb-4 flex items-center justify-center gap-3">
            <MembraneMark />
            <h1 className="bg-gradient-to-r from-yellow-300 via-yellow-500 to-amber-700 bg-clip-text text-5xl font-black tracking-tight text-transparent md:text-7xl">
              MEMBRA
            </h1>
          </div>
          <p className="mb-3 text-2xl font-semibold text-zinc-100 md:text-3xl">
            Inventory-as-a-Service for Apartments
          </p>
          <p className="mx-auto max-w-2xl text-lg text-zinc-400">
            Your apartment is the nearest warehouse. MEMBRA turns ordinary residents into local business owners by matching real-time nearby demand to approved household supply, space, tools, services, and access.
          </p>
        </div>

        <div className="mx-auto mt-10 max-w-3xl rounded-3xl border border-yellow-500/20 bg-zinc-950/90 p-3 shadow-2xl shadow-yellow-950/20">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-zinc-500" />
            <input
              type="text"
              placeholder="What do you need nearby?"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              className="w-full rounded-2xl border border-zinc-800 bg-black py-5 pl-12 pr-36 text-white placeholder-zinc-500 outline-none transition-colors focus:border-yellow-500"
            />
            <Link
              href={`/ask${query ? `?q=${encodeURIComponent(query)}` : ''}`}
              className="absolute right-2 top-1/2 -translate-y-1/2 rounded-xl bg-yellow-500 px-5 py-3 font-bold text-black transition-colors hover:bg-yellow-400"
            >
              Ask MEMBRA
            </Link>
          </div>
          <div className="mt-4 flex flex-wrap gap-2 px-1">
            {exampleRequests.map((request) => (
              <button
                key={request}
                onClick={() => setQuery(request)}
                className="rounded-full border border-zinc-800 bg-zinc-900 px-3 py-2 text-left text-xs text-zinc-300 transition-colors hover:border-yellow-500/50 hover:text-yellow-200"
              >
                {request}
              </button>
            ))}
          </div>
        </div>

        <div className="mt-12 grid gap-4 md:grid-cols-3">
          {structuredCards.map((card) => (
            <div key={card.item} className="rounded-3xl border border-zinc-800 bg-zinc-950 p-5">
              <div className="mb-4 flex items-start justify-between gap-3">
                <div>
                  <p className="text-sm text-zinc-500">Structured match card</p>
                  <h3 className="mt-1 text-xl font-bold text-white">{card.item}</h3>
                </div>
                <span className="rounded-full border border-yellow-500/30 bg-yellow-500/10 px-3 py-1 text-xs font-semibold text-yellow-300">
                  {card.risk} risk
                </span>
              </div>
              <dl className="grid grid-cols-2 gap-3 text-sm">
                <div><dt className="text-zinc-500">Price</dt><dd className="font-semibold text-zinc-100">{card.price}</dd></div>
                <div><dt className="text-zinc-500">Distance</dt><dd className="font-semibold text-zinc-100">{card.distance}</dd></div>
                <div className="col-span-2"><dt className="text-zinc-500">Deposit / proof</dt><dd className="font-semibold text-zinc-100">{card.deposit}</dd></div>
              </dl>
              <button className="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-white px-4 py-3 font-bold text-black transition-colors hover:bg-yellow-400">
                {card.action} <ArrowRight className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>

        <div className="mt-16 grid gap-10 lg:grid-cols-[1.1fr_0.9fr]">
          <section>
            <div className="mb-5 flex items-center justify-between gap-4">
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.25em] text-yellow-500">Marketplace modes</p>
                <h2 className="mt-2 text-3xl font-bold">Sell, rent, split, store, access, help, assess, advertise.</h2>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
              {marketplaceModes.map((mode) => {
                const Icon = mode.icon
                return (
                  <Link
                    key={mode.name}
                    href={mode.href}
                    className="group rounded-2xl border border-zinc-800 bg-zinc-950 p-5 transition-all hover:-translate-y-1 hover:border-yellow-500/50"
                  >
                    <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-yellow-500/10 text-yellow-400 group-hover:bg-yellow-500 group-hover:text-black">
                      <Icon className="h-5 w-5" />
                    </div>
                    <h3 className="font-bold">{mode.name}</h3>
                    <p className="mt-2 text-sm text-zinc-500">{mode.description}</p>
                  </Link>
                )
              })}
            </div>
          </section>

          <section className="rounded-3xl border border-zinc-800 bg-gradient-to-br from-zinc-950 to-black p-6">
            <p className="text-sm font-semibold uppercase tracking-[0.25em] text-yellow-500">LLM operator layer</p>
            <h2 className="mt-2 text-3xl font-bold">Apartment commerce operated by agents.</h2>
            <div className="mt-6 space-y-4">
              {operatorModules.map(([module, description]) => (
                <div key={module} className="rounded-2xl border border-zinc-800 bg-black/60 p-4">
                  <h3 className="font-bold text-yellow-200">{module}</h3>
                  <p className="mt-1 text-sm text-zinc-400">{description}</p>
                </div>
              ))}
            </div>
          </section>
        </div>

        <section className="mt-16 rounded-3xl border border-yellow-500/20 bg-yellow-500/10 p-8">
          <div className="grid gap-8 md:grid-cols-[0.8fr_1.2fr] md:items-center">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.25em] text-yellow-400">Best MVP</p>
              <h2 className="mt-2 text-3xl font-black">MEMBRA Requests + Private Inventory Drafts</h2>
              <p className="mt-3 text-zinc-300">
                Google login, LLM chat, post what I need, post what I have, room scan, Amazon and receipt upload, private SKU drafts, manual approval, nearby request board, checkout, proof photos, ratings, and credits.
              </p>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              {['Google login', 'Room/photo scan', 'Amazon link upload', 'Receipt upload', 'Private SKU draft', 'Approve listing', 'Stripe test checkout', 'Proof photo'].map((feature) => (
                <div key={feature} className="rounded-xl border border-yellow-500/20 bg-black/50 px-4 py-3 text-sm font-semibold text-zinc-100">
                  {feature}
                </div>
              ))}
            </div>
          </div>
        </section>
      </section>

      <footer className="border-t border-zinc-900 px-4 py-8 text-center text-sm text-zinc-600">
        Public pitch: MEMBRA lets regular residents turn their homes into local micro-businesses by selling, renting, splitting, storing, delivering, or sharing what they already own.
      </footer>
    </main>
  )
}

function MembraneMark() {
  return (
    <div className="relative h-14 w-14 rounded-full border-2 border-yellow-500/80 bg-black shadow-lg shadow-yellow-500/20">
      <div className="absolute inset-2 rounded-full border border-yellow-300/40" />
      <div className="absolute left-1/2 top-1/2 h-5 w-5 -translate-x-1/2 -translate-y-1/2 rotate-45 rounded-sm border border-yellow-200 bg-yellow-500/20" />
      <div className="absolute right-1 top-2 h-2 w-2 rounded-full bg-yellow-300" />
      <div className="absolute bottom-2 left-1 h-2 w-2 rounded-full bg-yellow-700" />
    </div>
  )
}
