import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from 'tailwindcss'
import autoprefixer from 'autoprefixer'

const tailwindConfig = fileURLToPath(new URL('./tailwind.config.js', import.meta.url))

export default defineConfig({
  plugins: [react()],
  css: {
    postcss: {
      plugins: [
        tailwindcss({ config: tailwindConfig }),
        autoprefixer(),
      ],
    },
  },
  server: {
    port: 5173,
  },
})