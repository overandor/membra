export function Input({ placeholder, value, onChange }: { placeholder?: string; value?: string; onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void }) {
  return (
    <input
      className="flex-1 bg-transparent px-4 text-white outline-none placeholder:text-zinc-600"
      placeholder={placeholder}
      value={value}
      onChange={onChange}
    />
  );
}
