/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        ink: {
          900: '#0a0e17',
          800: '#0f1420',
          700: '#161b29',
          600: '#222a3d',
          500: '#2f3950',
        },
        accent: {
          DEFAULT: '#3b82f6',
          soft: '#60a5fa',
        },
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        glow: '0 0 0 1px rgba(59,130,246,0.15), 0 8px 24px -8px rgba(59,130,246,0.25)',
        card: '0 1px 0 0 rgba(255,255,255,0.03) inset, 0 8px 24px -12px rgba(0,0,0,0.6)',
      },
      keyframes: {
        'fade-in': { '0%': { opacity: 0, transform: 'translateY(4px)' }, '100%': { opacity: 1, transform: 'none' } },
        'pulse-ring': { '0%': { boxShadow: '0 0 0 0 rgba(239,68,68,0.5)' }, '70%': { boxShadow: '0 0 0 8px rgba(239,68,68,0)' }, '100%': { boxShadow: '0 0 0 0 rgba(239,68,68,0)' } },
      },
      animation: {
        'fade-in': 'fade-in 0.35s ease-out',
        'pulse-ring': 'pulse-ring 2s infinite',
      },
    },
  },
  plugins: [],
}