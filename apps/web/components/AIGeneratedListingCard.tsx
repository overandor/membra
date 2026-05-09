interface ListingCardProps {
  title: string;
  price: string;
  category: string;
  distance?: string;
  risk: 'Low' | 'Medium' | 'High';
  verified?: boolean;
  aiGenerated?: boolean;
  onClick?: () => void;
}

export function AIGeneratedListingCard({
  title,
  price,
  category,
  distance,
  risk,
  verified = false,
  aiGenerated = true,
  onClick
}: ListingCardProps) {
  const categoryColors: Record<string, string> = {
    tools: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
    seating: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
    storage: 'bg-green-500/20 text-green-400 border-green-500/30',
    electronics: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30',
    pantry: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
    services: 'bg-pink-500/20 text-pink-400 border-pink-500/30',
    default: 'bg-zinc-500/20 text-zinc-400 border-zinc-500/30'
  };

  const riskColors: Record<string, string> = {
    Low: 'bg-green-500/20 text-green-400 border-green-500/30',
    Medium: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
    High: 'bg-red-500/20 text-red-400 border-red-500/30'
  };

  const categoryColor = categoryColors[category.toLowerCase()] || categoryColors.default;

  return (
    <div 
      onClick={onClick}
      className="rounded-2xl border border-zinc-800 bg-zinc-950 p-4 hover:border-amber-500/50 transition cursor-pointer"
    >
      {/* AI-generated visual placeholder */}
      <div className="aspect-video rounded-xl bg-zinc-900 mb-4 flex items-center justify-center border border-zinc-800">
        <div className="text-center">
          <div className="text-4xl mb-2">📦</div>
          <div className="text-xs text-zinc-500">AI-generated visual</div>
        </div>
      </div>

      {/* Verification badges */}
      <div className="flex gap-2 mb-3">
        {aiGenerated && (
          <span className="px-2 py-1 text-xs rounded border border-zinc-700 bg-zinc-900 text-zinc-400">
            AI-generated visual
          </span>
        )}
        {verified && (
          <span className="px-2 py-1 text-xs rounded border border-green-500/30 bg-green-500/10 text-green-400">
            Verified
          </span>
        )}
      </div>

      {/* Title and price */}
      <h3 className="text-lg font-bold mb-1">{title}</h3>
      <div className="text-2xl font-black text-amber-500 mb-2">{price}</div>

      {/* Category and risk badges */}
      <div className="flex gap-2 mb-2">
        <span className={`px-2 py-1 text-xs rounded border ${categoryColor}`}>
          {category}
        </span>
        <span className={`px-2 py-1 text-xs rounded border ${riskColors[risk]}`}>
          {risk} Risk
        </span>
      </div>

      {/* Distance if provided */}
      {distance && (
        <div className="text-sm text-zinc-400">{distance}</div>
      )}
    </div>
  );
}
