module.exports = {
  theme: {
    extend: {
      colors: {
        green: '#0F493F',
      },
    },
    fontFamily: {
      display: ['Work Sans', 'sans-serif'],
      post: ['Josefin Slab', 'serif']
    },
  },
  variants: {},
  plugins: [
    function({ addBase, config }) {
      addBase({
        'h1': { fontWeight: config('theme.fontWeight.'),
                fontSize: config('theme.fontSize.xxl'),
        },
        'h2': { fontSize: config('theme.fontSize.xl') },
        'h3': { fontSize: config('theme.fontSize.lg') }
      })
    }
  ]
}
