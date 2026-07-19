import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '@app/App'

describe('dental contact page — structure', () => {
  it('renders the clinic name', () => {
    render(<App />)
    expect(screen.getByText(/brightsmile dental/i)).toBeInTheDocument()
  })
  it('renders a contact form', () => {
    render(<App />)
    expect(screen.getByTestId('contact-form')).toBeInTheDocument()
  })
  it('has labeled name, email, and message fields', () => {
    render(<App />)
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/message/i)).toBeInTheDocument()
  })
  it('has a submit button', () => {
    render(<App />)
    expect(screen.getByRole('button', { name: /request appointment/i })).toBeInTheDocument()
  })
  it('renders a footer', () => {
    render(<App />)
    expect(screen.getByRole('contentinfo')).toBeInTheDocument()
  })
})

describe('dental contact page — validation gating (the defect)', () => {
  it('shows errors when submitting an empty form', async () => {
    const user = userEvent.setup()
    render(<App />)
    await user.click(screen.getByRole('button', { name: /request appointment/i }))
    expect(screen.getAllByTestId('form-error').length).toBeGreaterThan(0)
  })
  it('does NOT show success when submitting an empty form', async () => {
    const user = userEvent.setup()
    render(<App />)
    await user.click(screen.getByRole('button', { name: /request appointment/i }))
    expect(screen.queryByTestId('form-success')).toBeNull()
  })
  it('rejects an invalid email', async () => {
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByLabelText(/name/i), 'Ada')
    await user.type(screen.getByLabelText(/email/i), 'not-an-email')
    await user.type(screen.getByLabelText(/message/i), 'Cleaning please')
    await user.click(screen.getByRole('button', { name: /request appointment/i }))
    expect(screen.getAllByTestId('form-error').length).toBeGreaterThan(0)
    expect(screen.queryByTestId('form-success')).toBeNull()
  })
  it('accepts a fully valid submission', async () => {
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByLabelText(/name/i), 'Ada')
    await user.type(screen.getByLabelText(/email/i), 'ada@example.com')
    await user.type(screen.getByLabelText(/message/i), 'Cleaning please')
    await user.click(screen.getByRole('button', { name: /request appointment/i }))
    expect(screen.getByTestId('form-success')).toBeInTheDocument()
  })
})
