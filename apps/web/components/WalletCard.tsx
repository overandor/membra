type WalletCardProps = {
  balanceUsd: number;
  credits: number;
};

export function WalletCard({ balanceUsd, credits }: WalletCardProps) {
  return (
    <div className="rounded-2xl border border-amber-500/20 bg-zinc-950 px-5 py-3 text-right">
      <div className="text-xs text-zinc-500">Wallet</div>
      <div className="font-bold text-white">${balanceUsd.toFixed(2)}</div>
      <div className="text-xs text-amber-300">{credits} credits</div>
    </div>
  );
}
