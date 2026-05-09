export function CameraLinkDetections() {
  const detections = [
    { object: "power_drill", confidence: 0.92, suggested_price: "$7/hour", status: "ready" },
    { object: "tripod", confidence: 0.88, suggested_price: "$5/hour", status: "ready" },
    { object: "ring_light", confidence: 0.95, suggested_price: "$6/hour", status: "ready" },
    { object: "unknown", confidence: 0.45, suggested_price: "$3/hour", status: "needs_confirmation" },
    { object: "clothing", confidence: 0.72, suggested_price: "$2/hour", status: "needs_confirmation" },
    { object: "food_item", confidence: 0.38, suggested_price: "$1/hour", status: "blocked" },
  ];

  return (
    <div className="rounded-3xl border border-zinc-800 bg-zinc-950 p-6">
      <h2 className="text-2xl font-bold text-white mb-4">Detected Assets</h2>
      <div className="space-y-3">
        {detections.map((d, i) => (
          <div key={i} className="flex items-center justify-between p-4 rounded-xl border border-zinc-800 bg-zinc-900">
            <div>
              <div className="font-semibold text-white">{d.object.replace('_', ' ')}</div>
              <div className="text-xs text-zinc-500">Confidence: {(d.confidence * 100).toFixed(0)}%</div>
            </div>
            <div className="text-right">
              <div className="font-bold text-amber-300">{d.suggested_price}</div>
              <div className={`text-xs ${d.status === 'ready' ? 'text-green-400' : d.status === 'needs_confirmation' ? 'text-yellow-400' : 'text-red-400'}`}>
                {d.status.replace('_', ' ')}
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-6 p-4 rounded-xl bg-amber-900/20 border border-amber-500/30">
        <div className="text-sm text-amber-300">
          MEMBRA found 6 possible assets. 4 ready to approve. 2 need confirmation. 
          Estimated earning range: $64–$210/month.
        </div>
      </div>
    </div>
  );
}
