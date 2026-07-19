import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '@app/App'

// Block deleting the form / fields to trivially pass "no success shown".
describe('anti-cheat', () => {
  it('keeps the contact form and its three labeled fields', () => {
    render(<App />)
    expect(screen.getByTestId('contact-form')).toBeInTheDocument()
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/message/i)).toBeInTheDocument()
  })
  it('keeps the submit button', () => {
    render(<App />)
    expect(screen.getByRole('button', { name: /request appointment/i })).toBeInTheDocument()
  })
})
