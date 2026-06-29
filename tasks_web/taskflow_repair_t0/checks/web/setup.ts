import '@testing-library/jest-dom/vitest'
import { vi, beforeEach } from 'vitest'

// Deterministic + offline: no real network, fixed clock and RNG. The Python
// network guard does not reach node's subprocess, so this is mandatory here.
beforeEach(() => {
  vi.stubGlobal(
    'fetch',
    vi.fn(async () => new Response('{}', { status: 200 })),
  )
  vi.spyOn(Date, 'now').mockReturnValue(new Date('2026-01-01T00:00:00Z').valueOf())
  vi.spyOn(Math, 'random').mockReturnValue(0.42)
})
