/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./kioskbear/templates/**/*{html,js}'],
  theme: {
    container: {
      center: true,
    },
    colors: {
        transparent: 'transparent',
        current: 'currentColor',
        'red': '#b91c1c',
        'green': '#15803d',
        'white': '#FFFFFF',
        'lightest': '#F3F3F5',
        'light': '#EAE9E5',
        'mid': '#C3CBDD',
        'dark': '#75664F',
        'darkest': '#514738',
        'brand': '#ACC4AE',
    },
    fontFamily: {
        'sans': ['Inter var', 'sans-serif'],
    },
    extend: {},
  },
  plugins: [require("daisyui")],
}
