var gulp = require('gulp');
var shell = require('gulp-shell');

gulp.task('build', shell.task([
  'python -m compileall *.py'
]));

gulp.task('dist', ['build'], function () {
  gulp.src("*.pyc")
    .pipe(gulp.dest('dist'));
});

gulp.task('default', ['build', 'dist']);