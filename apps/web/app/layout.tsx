import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'MEMBRA - A marketplace you talk to',
  description: 'Need nearby. Earn locally. Turn assets into access.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
