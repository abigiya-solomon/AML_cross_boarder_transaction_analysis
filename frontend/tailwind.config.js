/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        slate: {
          850: '#151e2e',
          900: '#0f172a',
          950: '#090d16',
        },
        aml: {
          blue: '#1e40af',
          red: '#dc2626',
          amber: '#d97706',
          green: '#16a34a',
        }
      }
    },
  },
  plugins: [],
}
