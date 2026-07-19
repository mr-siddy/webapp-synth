import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '@app/App'

describe('restaurant page — structure', () => {
  it('renders the restaurant name', () => {
    render(<App />)
    expect(screen.getByRole('heading', { level: 1, name: /olive & thyme/i })).toBeInTheDocument()
  })
  it('renders an FAQ with at least three questions', () => {
    render(<App />)
    expect(screen.getAllByTestId('faq-question').length).toBeGreaterThanOrEqual(3)
  })
  it('renders a footer', () => {
    render(<App />)
    expect(screen.getByRole('contentinfo')).toBeInTheDocument()
  })
  it('opening a question reveals its answer', async () => {
    const user = userEvent.setup()
    render(<App />)
    expect(screen.queryByTestId('faq-answer')).toBeNull()
    await user.click(screen.getAllByTestId('faq-question')[0])
    expect(screen.getByTestId('faq-answer')).toBeInTheDocument()
  })
})

describe('restaurant FAQ — single-open (the defect)', () => {
  it('keeps only one answer open when a second question is clicked', async () => {
    const user = userEvent.setup()
    render(<App />)
    const qs = screen.getAllByTestId('faq-question')
    await user.click(qs[0])
    await user.click(qs[1])
    expect(screen.getAllByTestId('faq-answer')).toHaveLength(1)
  })
  it('opening a third question still leaves exactly one open', async () => {
    const user = userEvent.setup()
    render(<App />)
    const qs = screen.getAllByTestId('faq-question')
    await user.click(qs[0])
    await user.click(qs[1])
    await user.click(qs[2])
    expect(screen.getAllByTestId('faq-answer')).toHaveLength(1)
  })
  it('opening a second question closes the first', async () => {
    const user = userEvent.setup()
    render(<App />)
    const qs = screen.getAllByTestId('faq-question')
    await user.click(qs[0])
    const firstAnswer = screen.getByTestId('faq-answer').textContent
    await user.click(qs[1])
    const openAnswer = screen.getByTestId('faq-answer').textContent
    expect(openAnswer).not.toEqual(firstAnswer)
  })
})
