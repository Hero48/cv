/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "brand-gold": "#715800",
        "brand-purple": "#dcacfb",
        "brand-black": "#2d2f2f",
        "brand-yellow": "#f8cd50",
        "background": "#f6f6f6",
      },
      fontFamily: {
        "headline": ["Newsreader", "serif"],
        "body": ["Space Grotesk", "sans-serif"],
      },
      boxShadow: {
        'neo': '4px 4px 0px 0px rgba(45, 47, 47, 1)',
        'neo-lg': '8px 8px 0px 0px rgba(45, 47, 47, 1)',
      }
    },
  },
  plugins: [],
}
