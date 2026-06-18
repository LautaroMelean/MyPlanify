/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Neon violet — inverted scale: low numbers = dark bg tints, high = bright text
        primary: {
          50:  '#150b2e',
          100: '#1f1142',
          200: '#321a6e',
          300: '#5b2fc9',
          400: '#7c3aed',
          500: '#8b5cf6',
          600: '#a78bfa',
          700: '#c4b5fd',
          900: '#ede9fe',
        },
        // Inverted gray scale: 50=darkest page bg, 900=brightest heading text
        gray: {
          50:  '#07060f',
          100: '#0e0c1e',
          200: '#1a1830',
          300: '#2e2b4a',
          400: '#504c72',
          500: '#706d98',
          600: '#9e9bc0',
          700: '#c6c3de',
          800: '#dddaf5',
          900: '#f0eeff',
        },
        electric: {
          cyan:  '#00d4f5',
          green: '#00ff88',
          pink:  '#ff1dcf',
        },
      },
      boxShadow: {
        'neon-sm':   '0 0 12px rgba(139, 92, 246, 0.35)',
        'neon':      '0 0 22px rgba(139, 92, 246, 0.55), 0 0 45px rgba(139, 92, 246, 0.2)',
        'neon-cyan': '0 0 20px rgba(0, 212, 245, 0.45)',
        'glass':     '0 8px 32px rgba(0, 0, 0, 0.5)',
        'glass-sm':  '0 4px 16px rgba(0, 0, 0, 0.4)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
