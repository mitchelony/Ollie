/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        // Ollie Brand Palette
        ollie: {
          blue: "#0AEBFF",
          indigo: "#402D8B",
          black: "#040404",
          gray: "#EBEBEB",
        },
      },
    },
  },
  plugins: [],
};