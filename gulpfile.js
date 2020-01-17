const gulp = require('gulp');
const postcss = require('gulp-postcss');
const imagemin = require('gulp-imagemin');
const imageminMozjpeg = require('imagemin-mozjpeg');
const rename = require("gulp-rename");
const imageResize = require('gulp-image-resize');

gulp.task('css', function () {
  return gulp.src('static/css/styles.css')
  .pipe(postcss())
  .pipe(rename((path) => {
    path.basename = 'output'
  }))
  .pipe(gulp.dest('build/static/css/'));
});

gulp.task('images', () => {
  const sizes = [
    { width: 320, quality: 40, suffix: 'sm' },
    { width: 640, quality: 60, suffix: 'md' },
    { width: 1024, quality: 80, suffix: 'lg' },
  ];
  let stream;
  sizes.forEach((size) => {
    stream = gulp
      .src('static/img/**/*.jpg')
      .pipe(imageResize({ width: size.width }))
      .pipe(
        rename((path) => {
          path.basename += `-${size.suffix}`;
        }),
      )
      .pipe(
        imagemin(
          [
            imageminMozjpeg({
              quality: size.quality,
            }),
          ],
          {
            verbose: true,
          },
        ),
      )
      .pipe(gulp.dest('build/static/img/'));
  });
  return stream;
});
