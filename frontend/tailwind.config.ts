import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        canvas: "#0D0D1A",
        correct: "#22C55E",
        wrong: "#EF4444",
        selected: "#3B82F6",
      },
    },
  },
  plugins: [],
};

export default config;