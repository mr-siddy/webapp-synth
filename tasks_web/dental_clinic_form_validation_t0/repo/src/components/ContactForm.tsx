import { useState } from 'react'

type Errors = { name?: string; email?: string; message?: string }

export function ContactForm() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState('')
  const [errors] = useState<Errors>({})
  const [submitted, setSubmitted] = useState(false)

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    // BROKEN: confirms the booking without checking the inputs.
    setSubmitted(true)
  }

  return (
    <form data-testid="contact-form" onSubmit={handleSubmit} className="mt-8 space-y-4" noValidate>
      <div>
        <label htmlFor="name" className="block text-sm font-medium">Name</label>
        <input id="name" value={name} onChange={(e) => setName(e.target.value)}
          className="mt-1 w-full rounded border px-3 py-2" />
        {errors.name && <p data-testid="form-error" className="mt-1 text-sm text-red-600">{errors.name}</p>}
      </div>
      <div>
        <label htmlFor="email" className="block text-sm font-medium">Email</label>
        <input id="email" value={email} onChange={(e) => setEmail(e.target.value)}
          className="mt-1 w-full rounded border px-3 py-2" />
        {errors.email && <p data-testid="form-error" className="mt-1 text-sm text-red-600">{errors.email}</p>}
      </div>
      <div>
        <label htmlFor="message" className="block text-sm font-medium">Message</label>
        <textarea id="message" value={message} onChange={(e) => setMessage(e.target.value)}
          className="mt-1 w-full rounded border px-3 py-2" />
        {errors.message && <p data-testid="form-error" className="mt-1 text-sm text-red-600">{errors.message}</p>}
      </div>
      <button type="submit" className="rounded-lg bg-teal-600 px-5 py-2 font-medium text-white">
        Request appointment
      </button>
      {submitted && <p data-testid="form-success" className="text-green-700">Thanks — we'll confirm shortly.</p>}
    </form>
  )
}
