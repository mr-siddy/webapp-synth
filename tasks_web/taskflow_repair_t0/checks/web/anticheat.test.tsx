import { describe, it, expect } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '@app/App'

// Prevent the trivial cheat of deleting the mobile menu so "menu closes"
// passes vacuously: the menu must open and expose all three destinations.
describe('anti-cheat', () => {
  it('mobile menu toggle exists', () => {
    render(<App />)
    expect(screen.getByTestId('nav-toggle')).toBeInTheDocument()
  })
  it('opened mobile menu exposes all three navigation links', async () => {
    const user = userEvent.setup()
    render(<App />)
    await user.click(screen.getByTestId('nav-toggle'))
    const menu = screen.getByTestId('mobile-menu')
    for (const label of ['Features', 'Pricing', 'FAQ']) {
      expect(within(menu).getByRole('link', { name: label })).toBeInTheDocument()
    }
  })
})
