export function CameraLinkQRCode({ sessionId, status }: { sessionId: string; status: string }) {
  return (
    <div className="flex flex-col items-center justify-center rounded-3xl border border-zinc-800 bg-zinc-950 p-8">
      <h2 className="text-2xl font-bold text-white mb-4">Scan your {status === 'waiting_for_pairing' ? 'closet' : 'room'} with your phone</h2>
      <div className="mb-4 h-48 w-48 rounded-2xl bg-white p-2">
        <div className="h-full w-full bg-zinc-900 flex items-center justify-center">
          <div className="text-4xl">📱</div>
        </div>
      </div>
      <p className="text-zinc-400 text-center">
        {status === 'waiting_for_pairing' ? 'Waiting for phone...' : 'Connected!'}
      </p>
      <p className="text-xs text-zinc-600 mt-2">Session: {sessionId}</p>
    </div>
  );
}
