'use client'

import { useState } from 'react'
import { Cpu, Database, MessageSquare, Activity, Zap, Layers, Globe, Shield, Clock, TrendingUp } from 'lucide-react'

const osModules = [
  { id: 'inventory-os', name: 'InventoryOS', icon: Database, description: 'Turn home into machine-readable asset graph', status: 'active', color: 'from-blue-500/20 to-blue-600/10' },
  { id: 'intent-os', name: 'IntentOS', icon: MessageSquare, description: 'Inventory user needs and monetizable intentions', status: 'active', color: 'from-purple-500/20 to-purple-600/10' },
  { id: 'listing-os', name: 'ListingOS', icon: Layers, description: 'Turn household assets into SKU-like offerings', status: 'active', color: 'from-green-500/20 to-green-600/10' },
  { id: 'match-os', name: 'MatchOS', icon: Globe, description: 'Local supply-demand matching engine', status: 'active', color: 'from-cyan-500/20 to-cyan-600/10' },
  { id: 'relay-os', name: 'RelayOS', icon: Activity, description: 'Multi-node fulfillment routing', status: 'active', color: 'from-orange-500/20 to-orange-600/10' },
  { id: 'trust-os', name: 'TrustOS', icon: Shield, description: 'Proof capture and reputation system', status: 'active', color: 'from-indigo-500/20 to-indigo-600/10' },
]

const systemMetrics = [
  { label: 'Active Nodes', value: '1,247', change: '+12%', icon: Globe },
  { label: 'Daily Transactions', value: '8,432', change: '+8%', icon: Activity },
  { label: 'Total Listings', value: '24,891', change: '+15%', icon: Layers },
  { label: 'System Uptime', value: '99.97%', change: '+0.01%', icon: Clock },
]

export default function OSPage() {
  const [selectedModule, setSelectedModule] = useState<string | null>(null)
  const [chatMessages, setChatMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string }>>([
    { role: 'assistant', content: 'Welcome to MEMBRA OS. I am the operating layer that converts household assets into permissioned market supply. Ask me anything about inventory, listings, matching, or fulfillment.' }
  ])
  const [inputValue, setInputValue] = useState('')

  const handleSendMessage = () => {
    if (!inputValue.trim()) return
    
    setChatMessages(prev => [...prev, { role: 'user', content: inputValue }])
    setInputValue('')
    
    // Simulate AI response
    setTimeout(() => {
      setChatMessages(prev => [...prev, { 
        role: 'assistant', 
        content: `Processing your request through MEMBRA OS modules...\n\nI've analyzed your input across InventoryOS, IntentOS, and MatchOS. Based on your query, I recommend activating the ${selectedModule || 'InventoryOS'} module for optimal results.` 
      }])
    }, 1000)
  }

  return (
    <div className="min-h-screen bg-black">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <Cpu className="w-10 h-10 text-yellow-500" />
            <div>
              <h1 className="text-3xl font-bold text-white">MEMBRA OS</h1>
              <p className="text-zinc-400">LLM-Powered Operating Layer</p>
            </div>
          </div>
          <div className="flex items-center gap-2 bg-zinc-900 px-4 py-2 rounded-xl border border-zinc-800">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-green-500 text-sm font-medium">All Systems Operational</span>
          </div>
        </div>

        {/* System Metrics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {systemMetrics.map((metric) => {
            const Icon = metric.icon
            return (
              <div key={metric.label} className="bg-zinc-900 rounded-xl p-4 border border-zinc-800">
                <div className="flex items-center justify-between mb-2">
                  <Icon className="w-5 h-5 text-yellow-500" />
                  <span className="text-green-500 text-xs font-medium">{metric.change}</span>
                </div>
                <div className="text-2xl font-bold text-white mb-1">{metric.value}</div>
                <div className="text-zinc-400 text-sm">{metric.label}</div>
              </div>
            )
          })}
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* OS Modules */}
          <div className="lg:col-span-2">
            <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800 mb-6">
              <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
                <Zap className="w-5 h-5 text-yellow-500" />
                Active OS Modules
              </h2>
              <div className="grid md:grid-cols-2 gap-4">
                {osModules.map((module) => {
                  const Icon = module.icon
                  return (
                    <button
                      key={module.id}
                      onClick={() => setSelectedModule(module.id)}
                      className={`group relative bg-gradient-to-br ${module.color} rounded-xl p-5 border ${selectedModule === module.id ? 'border-yellow-500' : 'border-zinc-700'} hover:border-yellow-500/50 transition-all text-left`}
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div className="w-10 h-10 rounded-lg bg-zinc-900 flex items-center justify-center">
                          <Icon className="w-5 h-5 text-yellow-500" />
                        </div>
                        <div className="flex items-center gap-1">
                          <div className={`w-2 h-2 rounded-full ${module.status === 'active' ? 'bg-green-500' : 'bg-zinc-500'}`} />
                          <span className="text-xs text-zinc-400 capitalize">{module.status}</span>
                        </div>
                      </div>
                      <h3 className="font-semibold text-white mb-1">{module.name}</h3>
                      <p className="text-sm text-zinc-400">{module.description}</p>
                    </button>
                  )
                })}
              </div>
            </div>

            {/* Chat Interface */}
            <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800">
              <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
                <MessageSquare className="w-5 h-5 text-yellow-500" />
                OS Command Interface
              </h2>
              <div className="bg-zinc-950 rounded-xl p-4 mb-4 h-64 overflow-y-auto border border-zinc-800">
                {chatMessages.map((msg, idx) => (
                  <div key={idx} className={`mb-4 ${msg.role === 'user' ? 'text-right' : ''}`}>
                    <div className={`inline-block max-w-[80%] p-3 rounded-lg ${
                      msg.role === 'user' 
                        ? 'bg-yellow-500 text-black' 
                        : 'bg-zinc-800 text-white'
                    }`}>
                      <p className="whitespace-pre-wrap text-sm">{msg.content}</p>
                    </div>
                  </div>
                ))}
              </div>
              <div className="flex gap-3">
                <input
                  type="text"
                  placeholder="Command the OS..."
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                  className="flex-1 bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-3 text-white placeholder-zinc-500 focus:outline-none focus:border-yellow-500 transition-colors"
                />
                <button
                  onClick={handleSendMessage}
                  className="bg-yellow-500 text-black px-6 py-3 rounded-xl font-semibold hover:bg-yellow-400 transition-colors"
                >
                  Send
                </button>
              </div>
            </div>
          </div>

          {/* Knowledge Base */}
          <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-yellow-500" />
              Knowledge Base
            </h2>
            <div className="space-y-3">
              <div className="bg-zinc-950 rounded-xl p-4 border border-zinc-800 hover:border-yellow-500/50 transition-colors cursor-pointer">
                <h3 className="font-semibold text-white mb-1">Multi-OS Architecture</h3>
                <p className="text-sm text-zinc-400">Family of operating systems for household-to-market conversion</p>
              </div>
              <div className="bg-zinc-950 rounded-xl p-4 border border-zinc-800 hover:border-yellow-500/50 transition-colors cursor-pointer">
                <h3 className="font-semibold text-white mb-1">Local Marketplace Evolution</h3>
                <p className="text-sm text-zinc-400">Permissioned market supply and demand matching</p>
              </div>
              <div className="bg-zinc-950 rounded-xl p-4 border border-zinc-800 hover:border-yellow-500/50 transition-colors cursor-pointer">
                <h3 className="font-semibold text-white mb-1">OS Expansion Concepts</h3>
                <p className="text-sm text-zinc-400">Scaling MEMBRA across multiple operating layers</p>
              </div>
              <div className="bg-zinc-950 rounded-xl p-4 border border-zinc-800 hover:border-yellow-500/50 transition-colors cursor-pointer">
                <h3 className="font-semibold text-white mb-1">Alpha Operating System</h3>
                <p className="text-sm text-zinc-400">Confidential alpha generation and regime detection</p>
              </div>
              <div className="bg-zinc-950 rounded-xl p-4 border border-zinc-800 hover:border-yellow-500/50 transition-colors cursor-pointer">
                <h3 className="font-semibold text-white mb-1">MEMBRA Significado</h3>
                <p className="text-sm text-zinc-400">Core concepts and operating principles</p>
              </div>
            </div>

            <div className="mt-6 p-4 bg-yellow-500/10 rounded-xl border border-yellow-500/20">
              <p className="text-sm text-yellow-500">
                <strong>Documentation Loaded:</strong> 5 comprehensive files (112MB) integrated into OS knowledge graph
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
