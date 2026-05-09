import { CameraLinkQRCode } from "../../components/CameraLinkQRCode";
import { CameraLinkSession } from "../../components/CameraLinkSession";
import { CameraLinkDetections } from "../../components/CameraLinkDetections";

export default function CameraLinkPage() {
  return (
    <main className="min-h-screen bg-[#070707] text-white">
      <section className="mx-auto max-w-7xl px-6 py-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold mb-2">MEMBRA CameraLink</h1>
          <p className="text-zinc-400">Cross-account camera bridge for inventory scanning</p>
        </header>
        <div className="grid gap-6 md:grid-cols-2">
          <CameraLinkQRCode sessionId="scan_abc123" status="waiting_for_pairing" />
          <CameraLinkSession sessionId="scan_abc123" mode="snapshot" />
        </div>
        <section className="mt-6">
          <CameraLinkDetections />
        </section>
      </section>
    </main>
  );
}
