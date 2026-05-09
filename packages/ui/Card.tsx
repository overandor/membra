export function Card({ children }: { children: React.ReactNode }) {
  return (
    <div className="rounded-3xl border border-zinc-800 bg-zinc-950 p-6 shadow-xl">
      {children}
    </div>
  );
}
