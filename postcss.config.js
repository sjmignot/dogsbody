const purgecss = require("@fullhuman/postcss-purgecss")({
  // Specify the paths to all of the template files in your project
  content: [
    "./templates/*.html",
    "./content/posts/*.md",
    "./content/poetry/*.md",
    "./content/fiction/*.md",
    "./content/other/*.md",
    "blog.py",
    "./static/js/*.js",
    "./content/coding/notebooks/*.md",
  ],
  whitelistPatterns: [/^post/, /^palette/],
  // Include any special characters you're using in this regular expression
  defaultExtractor: (content) => content.match(/[\w-/:]+(?<!:)/g) || [],
});

module.exports = {
  plugins: [
    require("autoprefixer"),
    require("cssnano")({
      preset: "default",
    }),
    ...[purgecss],
  ],
};
