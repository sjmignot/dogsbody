var gulp = require('gulp');
var postcss = require('gulp-postcss');
var imagemin = require('gulp-imagemin');
var rename = require("gulp-rename");
var responsive = require('gulp-responsive')

gulp.task('css', function () {
  return gulp.src('static/css/styles.css')
  .pipe(postcss())
  .pipe(gulp.dest('dist/'));
});

gulp.task('resize-all', function() {
 return gulp
  .src('static/img/**/*.jpg')
  .pipe(
     responsive({
       '*.*': [
         {
           width: 1024,
           format: 'jpeg',
           rename: '*-lg.jpg',
           withoutEnlargement: true,
           errorOnEnlargement: false
         },
         {
           width: 640,
           format: 'jpeg',
           rename: '*-md.jpg',
           withoutEnlargement: true,
           errorOnEnlargement: false
         },
         {
           width: 320,
           format: 'jpeg',
           rename: '*-sm.jpg',
           withoutEnlargement: true,
           errorOnEnlargement: false
         }
       ]
     })
  )
  .pipe(gulp.dest('dist'))
});
