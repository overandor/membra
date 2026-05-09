'use client'

import { useState } from 'react'
import { Camera, Upload, CheckCircle, AlertCircle, XCircle, ChevronRight } from 'lucide-react'

export default function ScanPage() {
  const [selectedScanType, setSelectedScanType] = useState<string | null>(null)
  const [scanning, setScanning] = useState(false)
  const [scanResults, setScanResults] = useState<any>(null)

  const scanTypes = [
    { id: 'closet', name: 'Scan Closet', icon: '👕', priority: 1 },
    { id: 'shelf', name: 'Scan Shelf', icon: '📚', priority: 2 },
    { id: 'room', name: 'Scan Room', icon: '🏠', priority: 3 },
    { id: 'garage', name: 'Scan Garage', icon: '🚗', priority: 4 },
    { id: 'desk', name: 'Scan Desk', icon: '💻', priority: 5 },
    { id: 'toolbox', name: 'Scan Toolbox', icon: '🔧', priority: 6 },
    { id: 'storage_bins', name: 'Scan Storage Bins', icon: '📦', priority: 7 },
  ]

  const handleScan = async (scanType: string) => {
    setSelectedScanType(scanType)
    setScanning(true)
    
    // Mock scan - in production, this would call the API
    setTimeout(() => {
      setScanResults({
        scan_type: scanType,
        detected_items_count: 9,
        generated_listings_count: 9,
        ready_to_approve: 7,
        needs_confirmation: 2,
        compliance_review: 0,
        blocked: 0,
        estimated_monthly_earnings_min: 84,
        estimated_monthly_earnings_max: 260,
        message: 'MEMBRA found local earning opportunities. I created 9 draft listings. Nothing is public yet.',
        generated_listings: [
          {
            listing_id: 'draft_123',
            detected_item: 'Ring Light',
            title: 'Ring Light for Creator Setup',
            description: 'Borrow this ring light for video calls, streaming, photos, or product shots.',
            category: 'Creator Equipment',
            modes: ['rent'],
            suggested_price: { rent_per_hour: 8, deposit: 15 },
            condition_estimate: 'good',
            confidence: 0.86,
            risk_level: 'low',
            status: 'ready_to_approve'
          },
          {
            listing_id: 'draft_124',
            detected_item: 'Storage Bin',
            title: 'Storage Bin for Moving or Organization',
            description: 'Use this storage bin for moving, closet organization, or temporary storage.',
            category: 'Storage',
            modes: ['rent', 'sell'],
            suggested_price: { rent_per_week: 3, sale_price: 8 },
            condition_estimate: 'good',
            confidence: 0.92,
            risk_level: 'low',
            status: 'ready_to_approve'
          },
          {
            listing_id: 'draft_125',
            detected_item: 'Camera Tripod',
            title: 'Camera Tripod for Photography',
            description: 'Use this tripod for steady shots, video recording, or product photography.',
            category: 'Camera',
            modes: ['rent'],
            suggested_price: { rent_per_hour: 10, deposit: 20 },
            condition_estimate: 'good',
            confidence: 0.78,
            risk_level: 'low',
            status: 'needs_confirmation'
          }
        ]
      })
      setScanning(false)
    }, 2000)
  }

  const handleApprove = (listingIds: string[]) => {
    console.log('Approving listings:', listingIds)
    // In production, call API to approve listings
  }

  const handleReject = (listingIds: string[]) => {
    console.log('Rejecting listings:', listingIds)
    // In production, call API to reject listings
  }

  const handleConfirm = (listingId: string, confirmation: string) => {
    console.log('Confirming item:', listingId, confirmation)
    // In production, call API to confirm ambiguous item
  }

  if (scanning) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center p-4">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-yellow-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-yellow-500 text-lg">Scanning your {selectedScanType}...</p>
          <p className="text-gray-500 text-sm mt-2">MEMBRA is detecting monetizable assets</p>
        </div>
      </div>
    )
  }

  if (scanResults) {
    return (
      <div className="min-h-screen bg-black p-4">
        <div className="max-w-lg mx-auto">
          <button
            onClick={() => setScanResults(null)}
            className="text-gray-500 mb-4"
          >
            ← Back
          </button>

          <div className="bg-gradient-to-br from-yellow-500/10 to-yellow-600/5 rounded-2xl p-6 mb-6 border border-yellow-500/20">
            <h1 className="text-2xl font-bold text-white mb-2">
              Scan Complete
            </h1>
            <p className="text-gray-400 mb-4">{scanResults.message}</p>
            
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="bg-black/50 rounded-lg p-4">
                <div className="text-3xl font-bold text-green-500">{scanResults.ready_to_approve}</div>
                <div className="text-gray-500 text-sm">Ready to approve</div>
              </div>
              <div className="bg-black/50 rounded-lg p-4">
                <div className="text-3xl font-bold text-yellow-500">{scanResults.needs_confirmation}</div>
                <div className="text-gray-500 text-sm">Needs review</div>
              </div>
            </div>

            <div className="bg-black/50 rounded-lg p-4">
              <div className="text-gray-400 text-sm mb-1">Estimated monthly earnings</div>
              <div className="text-2xl font-bold text-yellow-500">
                ${scanResults.estimated_monthly_earnings_min} - ${scanResults.estimated_monthly_earnings_max}
              </div>
            </div>
          </div>

          <div className="space-y-3">
            <h2 className="text-lg font-semibold text-white mb-4">Draft Listings</h2>
            
            {scanResults.generated_listings.map((listing: any) => (
              <div key={listing.listing_id} className="bg-zinc-900 rounded-xl p-4 border border-zinc-800">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <h3 className="text-white font-semibold mb-1">{listing.title}</h3>
                    <p className="text-gray-500 text-sm">{listing.description}</p>
                  </div>
                  <div className="ml-4">
                    {listing.status === 'ready_to_approve' && (
                      <CheckCircle className="w-6 h-6 text-green-500" />
                    )}
                    {listing.status === 'needs_confirmation' && (
                      <AlertCircle className="w-6 h-6 text-yellow-500" />
                    )}
                    {listing.status === 'blocked' && (
                      <XCircle className="w-6 h-6 text-red-500" />
                    )}
                  </div>
                </div>

                <div className="flex items-center justify-between text-sm">
                  <div className="flex gap-2">
                    <span className="bg-zinc-800 px-2 py-1 rounded text-gray-400">
                      {listing.category}
                    </span>
                    <span className="bg-zinc-800 px-2 py-1 rounded text-gray-400">
                      {listing.modes.join(', ')}
                    </span>
                  </div>
                  <div className="text-yellow-500 font-semibold">
                    ${Object.values(listing.suggested_price)[0]}
                  </div>
                </div>

                {listing.status === 'needs_confirmation' && (
                  <div className="mt-3 pt-3 border-t border-zinc-800">
                    <p className="text-gray-500 text-sm mb-2">Is this item working?</p>
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleConfirm(listing.listing_id, 'works')}
                        className="flex-1 bg-green-500/20 text-green-500 py-2 rounded-lg text-sm font-semibold"
                      >
                        Works
                      </button>
                      <button
                        onClick={() => handleConfirm(listing.listing_id, 'not_sure')}
                        className="flex-1 bg-yellow-500/20 text-yellow-500 py-2 rounded-lg text-sm font-semibold"
                      >
                        Not sure
                      </button>
                      <button
                        onClick={() => handleConfirm(listing.listing_id, 'do_not_list')}
                        className="flex-1 bg-red-500/20 text-red-500 py-2 rounded-lg text-sm font-semibold"
                      >
                        Don't list
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="flex gap-3 mt-6">
            <button
              onClick={() => handleApprove(scanResults.generated_listings.map((l: any) => l.listing_id))}
              className="flex-1 bg-yellow-500 text-black py-4 rounded-xl font-bold"
            >
              Approve All
            </button>
            <button
              onClick={() => setScanResults(null)}
              className="flex-1 bg-zinc-800 text-white py-4 rounded-xl font-semibold"
            >
              Review
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black p-4">
      <div className="max-w-lg mx-auto">
        <h1 className="text-3xl font-bold text-white mb-2">
          What can your home earn from?
        </h1>
        <p className="text-gray-500 mb-6">
          Take photos. MEMBRA creates listings. You approve.
        </p>

        <div className="space-y-3">
          {scanTypes.map((scanType) => (
            <button
              key={scanType.id}
              onClick={() => handleScan(scanType.id)}
              className="w-full bg-zinc-900 hover:bg-zinc-800 rounded-xl p-4 flex items-center justify-between border border-zinc-800 transition-colors"
            >
              <div className="flex items-center gap-4">
                <div className="text-3xl">{scanType.icon}</div>
                <div className="text-left">
                  <div className="text-white font-semibold">{scanType.name}</div>
                  <div className="text-gray-500 text-sm">
                    AI-powered inventory scan
                  </div>
                </div>
              </div>
              <ChevronRight className="w-6 h-6 text-gray-500" />
            </button>
          ))}
        </div>

        <div className="mt-6 grid grid-cols-2 gap-3">
          <button className="bg-zinc-900 hover:bg-zinc-800 rounded-xl p-4 flex items-center gap-3 border border-zinc-800 transition-colors">
            <Camera className="w-6 h-6 text-yellow-500" />
            <div className="text-left">
              <div className="text-white font-semibold text-sm">Import Amazon</div>
              <div className="text-gray-500 text-xs">Link your account</div>
            </div>
          </button>
          <button className="bg-zinc-900 hover:bg-zinc-800 rounded-xl p-4 flex items-center gap-3 border border-zinc-800 transition-colors">
            <Upload className="w-6 h-6 text-yellow-500" />
            <div className="text-left">
              <div className="text-white font-semibold text-sm">Upload Receipt</div>
              <div className="text-gray-500 text-xs">OCR scanning</div>
            </div>
          </button>
        </div>
      </div>
    </div>
  )
}
