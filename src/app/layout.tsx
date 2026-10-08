import type { Metadata, Viewport } from 'next'
import '../ui/styles.css'

export const metadata: Metadata = {
  title: 'Lighthouse Keeper',
  appleWebApp: { capable: true, statusBarStyle: 'black-translucent' },
}
export const viewport: Viewport = { width: 'device-width', initialScale: 1, userScalable: false, viewportFit: 'cover' }

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en-GB">
      <body>
        <div id="root">{children}</div>
      </body>
    </html>
  )
}
