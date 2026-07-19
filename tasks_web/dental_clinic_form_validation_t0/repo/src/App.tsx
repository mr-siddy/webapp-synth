import { ContactForm } from './components/ContactForm'

export default function App() {
  return (
    <div className="min-h-screen bg-white text-slate-900">
      <header className="border-b">
        <div className="mx-auto max-w-3xl px-4 py-4">
          <span className="text-lg font-bold">Brightsmile Dental</span>
        </div>
      </header>
      <main className="mx-auto max-w-3xl px-4 py-16">
        <h1 className="text-3xl font-bold">Book your appointment</h1>
        <p className="mt-2 text-slate-600">
          Send us your details and our front desk will confirm your visit.
        </p>
        <ContactForm />
      </main>
      <footer className="border-t">
        <div className="mx-auto max-w-3xl px-4 py-8 text-sm text-slate-500">
          © 2026 All rights reserved.
        </div>
      </footer>
    </div>
  )
}
