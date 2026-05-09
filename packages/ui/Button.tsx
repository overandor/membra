export function Button({ children, onClick }: { children: React.ReactNode; onClick?: () => void }) {
  return (
    <button
      onClick={onClick}
      className="rounded-xl bg-amber-400 px-5 py-3 font-bold text-black hover:bg-amber-300"
    >
      {children}
    </button>
  );
}
