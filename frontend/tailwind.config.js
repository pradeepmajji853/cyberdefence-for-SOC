/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Professional dark theme base
        'dark': {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
        // Professional cybersecurity palette
        'cyber': {
          'primary': '#3b82f6',     // Professional blue
          'secondary': '#10b981',   // Professional green
          'accent': '#f59e0b',      // Professional amber
          'danger': '#ef4444',      // Professional red
          'warning': '#f97316',     // Professional orange
          'success': '#22c55e',     // Professional green
          'info': '#06b6d4',       // Professional cyan
        },
        // Background colors
        'bg': {
          'primary': '#0f172a',     // Main dark background
          'secondary': '#1e293b',   // Card backgrounds
          'tertiary': '#334155',    // Subtle accents
          'hover': '#475569',       // Hover states
        },
        // Text colors
        'text': {
          'primary': '#f8fafc',     // Main text
          'secondary': '#cbd5e1',   // Secondary text
          'muted': '#94a3b8',       // Muted text
          'accent': '#3b82f6',      // Accent text
        },
        // Border colors
        'border': {
          'primary': '#334155',     // Main borders
          'secondary': '#475569',   // Secondary borders
          'accent': '#3b82f6',      // Accent borders
        },
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        'mono': ['JetBrains Mono', 'Monaco', 'Cascadia Code', 'Fira Code', 'monospace'],
      },
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1rem', { lineHeight: '1.5rem' }],
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          'from': {
            'text-shadow': '0 0 5px #00d4ff, 0 0 10px #00d4ff, 0 0 15px #00d4ff',
          },
          'to': {
            'text-shadow': '0 0 10px #00d4ff, 0 0 20px #00d4ff, 0 0 30px #00d4ff',
          }
        }
      }
    },
  },
  plugins: [],
}
