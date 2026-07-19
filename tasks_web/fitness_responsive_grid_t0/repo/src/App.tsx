import { Classes } from './components/Classes'

export default function App() {
  return (
    <div className="min-h-screen bg-white text-slate-900">
      <main>
        <section id="hero" className="mx-auto max-w-5xl px-4 py-16 text-center">
          <h1 className="text-4xl font-bold">Ironleaf Studio</h1>
          <p className="mt-2 text-slate-600">Small-group strength and mobility classes.</p>
        </section>
        <Classes />
      </main>
      <footer className="border-t">
        <div className="mx-auto max-w-5xl px-4 py-8 text-sm text-slate-500">© 2026 Ironleaf Studio.</div>
      </footer>
    </div>
  )
}
