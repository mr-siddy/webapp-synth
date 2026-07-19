import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '@app/App'

describe('fitness page — structure', () => {
  it('renders the studio name', () => {
    render(<App />)
    expect(screen.getByRole('heading', { level: 1, name: /ironleaf studio/i })).toBeInTheDocument()
  })
  it('renders three class cards', () => {
    render(<App />)
    expect(screen.getAllByTestId('class-card')).toHaveLength(3)
  })
  it('renders a footer', () => {
    render(<App />)
    expect(screen.getByRole('contentinfo')).toBeInTheDocument()
  })
})

describe('fitness class grid — responsive (the defect)', () => {
  it('the grid is a single column on mobile', () => {
    render(<App />)
    expect(screen.getByTestId('class-grid').className).toContain('grid-cols-1')
  })
  it('the grid expands to multiple columns on desktop', () => {
    render(<App />)
    expect(screen.getByTestId('class-grid').className).toMatch(/md:grid-cols-\d/)
  })
})
