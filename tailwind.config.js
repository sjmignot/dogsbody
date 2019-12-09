module.exports = {
  theme: {
    extend: {
      colors: {
        green: '#0F493F',
      },
    },
    fontFamily: {
      display: ['Avenir Next', 'sans-serif'],
      body: ['Graphik', 'sans-serif'],
    },
  },
  variants: {},
  plugins: [
    function({ addBase, config }) {
      addBase({
        'h1': { fontSize: config('theme.fontSize.2xl') },
        'h2': { fontSize: config('theme.fontSize.xl') },
        'h3': { fontSize: config('theme.fontSize.lg') },
      })
    }
  ]
}
