type ListingCardProps = {
  title: string;
  mode: string;
  price: string;
  risk: string;
};

export function ListingCard({ title, mode, price, risk }: ListingCardProps) {
  return (
    <article className="rounded-3xl border border-zinc-800 bg-zinc-950 p-5 shadow-xl">
      <div className="mb-4 h-36 rounded-2xl bg-gradient-to-br from-zinc-900 to-black" />
      <div className="mb-2 flex items-center justify-between">
        <span className="rounded-full bg-amber-400/10 px-3 py-1 text-xs font-bold text-amber-300">
          {mode}
        </span>
        <span className="text-xs text-zinc-500">Risk: {risk}</span>
      </div>
      <h3 className="text-lg font-bold text-white">{title}</h3>
      <p className="mt-1 text-amber-300">{price}</p>
      <button className="mt-5 w-full rounded-xl bg-white px-4 py-3 font-bold text-black hover:bg-amber-300">
        Book
      </button>
    </article>
  );
}
