import { describe, it, expect } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '@app/App'

describe('TaskFlow landing — structure', () => {
  it('renders the hero headline', () => {
    render(<App />)
    expect(screen.getByRole('heading', { level: 1, name: /taskflow/i })).toBeInTheDocument()
  })
  it('hero has a call to action', () => {
    render(<App />)
    expect(screen.getByTestId('hero-cta')).toBeInTheDocument()
  })
  it('features grid uses responsive column classes', () => {
    render(<App />)
    const grid = screen.getByTestId('features-grid')
    expect(grid.className).toContain('grid-cols-1')
    expect(grid.className).toContain('md:grid-cols-3')
  })
  it('renders three feature cards', () => {
    render(<App />)
    expect(screen.getAllByTestId('feature-card')).toHaveLength(3)
  })
  it('renders three pricing tiers', () => {
    render(<App />)
    expect(screen.getAllByTestId('pricing-tier')).toHaveLength(3)
  })
  it('marks exactly one tier most popular', () => {
    render(<App />)
    expect(screen.getAllByTestId('popular-badge')).toHaveLength(1)
  })
  it('renders a footer landmark', () => {
    render(<App />)
    expect(screen.getByRole('contentinfo')).toBeInTheDocument()
  })
})

describe('TaskFlow landing — behavior', () => {
  it('FAQ expands an answer when its question is clicked', async () => {
    const user = userEvent.setup()
    render(<App />)
    expect(screen.queryByTestId('faq-answer')).toBeNull()
    await user.click(screen.getAllByTestId('faq-question')[0])
    expect(screen.getByTestId('faq-answer')).toBeInTheDocument()
  })

  // The planted defect: navigating from the mobile menu must close it.
  for (const label of ['Features', 'Pricing', 'FAQ']) {
    it(`mobile menu closes after tapping ${label}`, async () => {
      const user = userEvent.setup()
      render(<App />)
      await user.click(screen.getByTestId('nav-toggle'))
      const menu = screen.getByTestId('mobile-menu')
      await user.click(within(menu).getByRole('link', { name: label }))
      expect(screen.queryByTestId('mobile-menu')).toBeNull()
    })
  }
})
