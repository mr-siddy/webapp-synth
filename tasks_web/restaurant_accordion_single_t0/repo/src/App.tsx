import { FAQ } from './components/FAQ'

export default function App() {
  return (
    <div className="min-h-screen bg-white text-slate-900">
      <main>
        <section id="hero" className="mx-auto max-w-3xl px-4 py-16 text-center">
          <h1 className="text-4xl font-bold">Olive & Thyme</h1>
          <p className="mt-2 text-slate-600">Seasonal Mediterranean plates in the heart of town.</p>
        </section>
        <FAQ />
      </main>
      <footer className="border-t">
        <div className="mx-auto max-w-3xl px-4 py-8 text-sm text-slate-500">
          © 2026 Olive &amp; Thyme.
        </div>
      </footer>
    </div>
  )
}
