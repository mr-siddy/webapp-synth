import { useState } from 'react'

const QA = [
  { q: 'Do you take reservations?', a: 'Yes, for parties of two or more, online or by phone.' },
  { q: 'Are there vegan options?', a: 'Several — the menu marks every vegan and gluten-free dish.' },
  { q: 'Is there parking?', a: 'Street parking, plus a lot behind the building after 6pm.' },
]

export function FAQ() {
  // BROKEN: each opened item is added to a set, so multiple stay open at once.
  const [open, setOpen] = useState<Set<number>>(new Set())

  function toggle(i: number) {
    setOpen((prev) => {
      const next = new Set(prev)
      next.has(i) ? next.delete(i) : next.add(i)
      return next
    })
  }

  return (
    <section id="faq" className="mx-auto max-w-2xl px-4 py-16">
      <h2 className="text-center text-3xl font-bold">Good to know</h2>
      <ul className="mt-8 divide-y">
        {QA.map((item, i) => (
          <li key={item.q} className="py-3">
            <button
              type="button"
              data-testid="faq-question"
              aria-expanded={open.has(i)}
              onClick={() => toggle(i)}
              className="flex w-full justify-between text-left font-medium"
            >
              {item.q}
            </button>
            {open.has(i) && <p data-testid="faq-answer" className="mt-2 text-slate-600">{item.a}</p>}
          </li>
        ))}
      </ul>
    </section>
  )
}
