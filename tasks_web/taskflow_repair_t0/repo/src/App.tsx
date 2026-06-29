import { useState } from 'react'
import { Nav } from './components/Nav'
import { MobileMenu } from './components/MobileMenu'
import { Hero, Features, Pricing, FAQ, Footer } from './components/Sections'

export default function App() {
  const [menuOpen, setMenuOpen] = useState(false)
  const closeMenu = () => setMenuOpen(false)
  return (
    <div className="min-h-screen bg-white text-slate-900">
      <Nav menuOpen={menuOpen} onToggle={() => setMenuOpen((o) => !o)} />
      <MobileMenu open={menuOpen} onNavigate={closeMenu} />
      <main>
        <Hero />
        <Features />
        <Pricing />
        <FAQ />
      </main>
      <Footer />
    </div>
  )
}
