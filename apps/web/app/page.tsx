import { ChatBar } from "@/components/ChatBar";
import { ServiceGrid } from "@/components/ServiceGrid";
import { ListingCard } from "@/components/ListingCard";
import { WalletCard } from "@/components/WalletCard";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-[#070707] text-white">
      <section className="mx-auto max-w-7xl px-6 py-8">
        <header className="mb-8 flex items-center justify-between">
          <div>
            <div className="text-3xl font-black tracking-tight text-white">
              MEMBRA
            </div>
            <p className="text-sm text-zinc-400">
              A marketplace you talk to.
            </p>
          </div>
          <WalletCard balanceUsd={42.75} credits={1850} />
        </header>
        <section className="rounded-3xl border border-amber-500/20 bg-zinc-950/80 p-6 shadow-[0_0_80px_rgba(245,158,11,0.12)]">
          <h1 className="mb-3 text-4xl font-black tracking-tight">
            What do you need, have, or want to earn from?
          </h1>
          <p className="mb-6 max-w-2xl text-zinc-400">
            Ask MEMBRA for nearby needs, local inventory, split orders,
            Relay delivery, or what your home can earn from.
          </p>
          <ChatBar />
        </section>
        <section className="mt-8">
          <ServiceGrid />
        </section>
        <section className="mt-10 grid gap-5 md:grid-cols-3">
          <ListingCard
            title="Couch Seat + Wi-Fi"
            mode="Rent"
            price="$8/hour"
            risk="Low"
          />
          <ListingCard
            title="Power Drill"
            mode="Rent"
            price="$7/hour"
            risk="Low"
          />
          <ListingCard
            title="Package Holding"
            mode="Store"
            price="$3/day"
            risk="Low"
          />
        </section>
      </section>
    </main>
  );
}
