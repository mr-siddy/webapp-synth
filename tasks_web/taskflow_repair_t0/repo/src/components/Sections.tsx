import { useState } from 'react'

export function Hero() {
  return (
    <section id="hero" className="mx-auto max-w-6xl px-4 py-20 text-center">
      <h1 className="text-4xl font-bold sm:text-5xl">Ship projects faster with TaskFlow</h1>
      <p className="mx-auto mt-4 max-w-2xl text-lg text-slate-600">
        Plan, track, and deliver work in one place your whole team will actually use.
      </p>
      <a
        href="#pricing"
        data-testid="hero-cta"
        className="mt-8 inline-block rounded-lg bg-indigo-600 px-6 py-3 font-medium text-white"
      >
        Start free trial
      </a>
    </section>
  )
}

const FEATURES = [
  { title: 'Boards', body: 'Visualize every workflow with flexible kanban boards.' },
  { title: 'Timelines', body: 'See dependencies and deadlines on a live timeline.' },
  { title: 'Automations', body: 'Cut busywork with no-code rules and triggers.' },
]

export function Features() {
  return (
    <section id="features" className="mx-auto max-w-6xl px-4 py-16">
      <h2 className="text-center text-3xl font-bold">Everything your team needs</h2>
      <div data-testid="features-grid" className="mt-10 grid grid-cols-1 gap-6 md:grid-cols-3">
        {FEATURES.map((f) => (
          <div key={f.title} data-testid="feature-card" className="rounded-xl border p-6">
            <h3 className="text-lg font-semibold">{f.title}</h3>
            <p className="mt-2 text-slate-600">{f.body}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

const TIERS = [
  { name: 'Starter', price: '$0', popular: false },
  { name: 'Team', price: '$12', popular: true },
  { name: 'Business', price: '$29', popular: false },
]

export function Pricing() {
  return (
    <section id="pricing" className="mx-auto max-w-6xl px-4 py-16">
      <h2 className="text-center text-3xl font-bold">Simple pricing</h2>
      <div className="mt-10 grid grid-cols-1 gap-6 md:grid-cols-3">
        {TIERS.map((t) => (
          <div key={t.name} data-testid="pricing-tier" className="rounded-xl border p-6">
            {t.popular && (
              <span
                data-testid="popular-badge"
                className="rounded-full bg-indigo-600 px-3 py-1 text-xs text-white"
              >
                Most popular
              </span>
            )}
            <h3 className="mt-2 text-lg font-semibold">{t.name}</h3>
            <p className="mt-1 text-3xl font-bold">{t.price}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

const QA = [
  { q: 'Can I cancel anytime?', a: 'Yes, plans are month to month with no lock-in.' },
  { q: 'Do you offer a free trial?', a: 'Every paid plan includes a 14-day free trial.' },
]

export function FAQ() {
  const [open, setOpen] = useState<number | null>(null)
  return (
    <section id="faq" className="mx-auto max-w-3xl px-4 py-16">
      <h2 className="text-center text-3xl font-bold">Frequently asked questions</h2>
      <ul className="mt-8 divide-y">
        {QA.map((item, i) => (
          <li key={item.q} className="py-3">
            <button
              type="button"
              data-testid="faq-question"
              aria-expanded={open === i}
              onClick={() => setOpen(open === i ? null : i)}
              className="flex w-full justify-between text-left font-medium"
            >
              {item.q}
            </button>
            {open === i && (
              <p data-testid="faq-answer" className="mt-2 text-slate-600">
                {item.a}
              </p>
            )}
          </li>
        ))}
      </ul>
    </section>
  )
}

export function Footer() {
  return (
    <footer className="border-t">
      <div className="mx-auto max-w-6xl px-4 py-8 text-sm text-slate-500">
        © 2026 TaskFlow, Inc. All rights reserved.
      </div>
    </footer>
  )
}
