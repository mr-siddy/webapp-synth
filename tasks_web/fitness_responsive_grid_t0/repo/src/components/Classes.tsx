const CLASSES = [
  { name: 'Foundations', body: 'Barbell basics with coaching on every rep.' },
  { name: 'Mobility Flow', body: 'Joint-by-joint mobility to move without pain.' },
  { name: 'Conditioning', body: 'Short, hard intervals that build engine.' },
]

export function Classes() {
  return (
    <section id="classes" className="mx-auto max-w-5xl px-4 py-16">
      <h2 className="text-center text-3xl font-bold">Our classes</h2>
      {/* BROKEN: fixed 3 columns — does not collapse on small screens. */}
      <div data-testid="class-grid" className="mt-10 grid grid-cols-3 gap-6">
        {CLASSES.map((c) => (
          <div key={c.name} data-testid="class-card" className="rounded-xl border p-6">
            <h3 className="text-lg font-semibold">{c.name}</h3>
            <p className="mt-2 text-slate-600">{c.body}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
