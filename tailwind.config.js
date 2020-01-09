module.exports = {
  theme: {
    extend: {
      colors: {
        green: '#0F493F',
      },
      spacing: {
        '72': '18rem',
        '84': '21rem',
        '96': '24rem',
        '108': '27rem',
        '120': '30rem',
        '132': '33rem',
        '144': '36rem',
        '166': '39rem',
        '178': '42rem',
        '190': '45rem',
        '202': '48rem'
      }
    },
    fontFamily: {
      header: ['Gotham', 'sans-serif'],
      posttitle: ['Helvetica', 'sans-serif'],
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
