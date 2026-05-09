export function ChatBar() {
  return (
    <div className="flex rounded-2xl border border-amber-500/20 bg-black p-2">
      <input
        className="flex-1 bg-transparent px-4 text-white outline-none placeholder:text-zinc-600"
        placeholder="Ask MEMBRA anything nearby..."
      />
      <button className="rounded-xl bg-amber-400 px-5 py-3 font-bold text-black hover:bg-amber-300">
        Ask
      </button>
    </div>
  );
}
