import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'node:path'

// This file is executed from <repo>/.eca_checks/vitest.config.ts at scoring time,
// so ../src is always the candidate repo's source.
export default defineConfig({
  plugins: [react()],
  resolve: { alias: { '@app': path.resolve(__dirname, '../src') } },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: [path.resolve(__dirname, 'setup.ts')],
    include: [path.resolve(__dirname, '*.test.tsx')],
  },
})
