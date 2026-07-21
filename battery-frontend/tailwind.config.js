/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Exact palette from the project spec - every teammate's screen
        // should pull colors from here, not hardcode hex values.
        background: "#0a0e14",
        card: "#131822",
        accent: "#3b82f6",
        success: "#22c55e",
        warning: "#eab308",
        danger: "#ef4444",
      },
      fontFamily: {
        // Inter for UI text, JetBrains Mono for all numeric/data display
        sans: ["Inter", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
    },
  },
  plugins: [],
};
