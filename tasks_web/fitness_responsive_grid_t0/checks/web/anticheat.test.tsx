import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '@app/App'

describe('anti-cheat', () => {
  it('keeps the class grid with its cards', () => {
    render(<App />)
    expect(screen.getByTestId('class-grid')).toBeInTheDocument()
    expect(screen.getAllByTestId('class-card').length).toBeGreaterThanOrEqual(3)
  })
})
