export function Badge({ children }: { children: React.ReactNode }) {
  return (
    <span className="rounded-full bg-amber-400/10 px-3 py-1 text-xs font-bold text-amber-300">
      {children}
    </span>
  );
}
