module.exports = {
  theme: {
    fontSize: {
      'xs': '.75rem',
      'sm': '.875rem',
      'tiny': '.875rem',
      'base': '1rem',
      'lg': '1.125rem',
      'xl': '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
      '4xl': '2.25rem',
      '5xl': '3rem',
      '6xl': '4rem',
      '7xl': '5rem',
    },
    extend: {
      colors: {
        green: '#0F493F',
        red: '#C73E1D',
        orange: '#F18F01',
      },
      spacing: {
        '27': '7.27rem',
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
      header: ['Fira Sans', 'sans-serif'],
      posttitle: ['Josefin Slab', 'serif'],
      postheader: ['Klinic Slab', 'serif'],
      display: ['Work Sans', 'sans-serif'],
      post: ['Lato', 'sans-serif']
    },
  },
  variants: {
    fill: ['responsive', 'hover'],
    stroke: ['responsive', 'hover', 'focus'],
    opacity: ['responsive', 'hover', 'focus', 'group-hover'],
  },
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
