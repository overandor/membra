export function CameraLinkSession({ sessionId, mode }: { sessionId: string; mode: string }) {
  return (
    <div className="rounded-3xl border border-zinc-800 bg-zinc-950 p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-white">CameraLink Session</h2>
        <span className="text-xs text-zinc-500">{mode === 'live_scan' ? 'Live Scan' : 'Snapshot'}</span>
      </div>
      <div className="space-y-4">
        <div className="flex items-center justify-between p-4 rounded-xl border border-zinc-800 bg-zinc-900">
          <span className="text-white">Status</span>
          <span className="text-green-400">Connected</span>
        </div>
        <div className="flex items-center justify-between p-4 rounded-xl border border-zinc-800 bg-zinc-900">
          <span className="text-white">Photos Captured</span>
          <span className="text-zinc-400">0</span>
        </div>
        <div className="flex items-center justify-between p-4 rounded-xl border border-zinc-800 bg-zinc-900">
          <span className="text-white">Detections</span>
          <span className="text-amber-300">Waiting...</span>
        </div>
      </div>
    </div>
  );
}
