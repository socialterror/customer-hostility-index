import type { Config } from 'tailwindcss';

export default {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'Arial', 'sans-serif'],
      },
      colors: {
        ink: '#0a0a0a',
        paper: '#f5f5f0',
      },
    },
  },
  plugins: [],
} satisfies Config;
