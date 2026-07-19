import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '@app/App'

// Block deleting the FAQ so "one open at a time" passes vacuously.
describe('anti-cheat', () => {
  it('keeps an FAQ with at least three question buttons', () => {
    render(<App />)
    expect(screen.getAllByTestId('faq-question').length).toBeGreaterThanOrEqual(3)
  })
})
