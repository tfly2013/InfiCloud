var gulp = require('gulp');
var shell = require('gulp-shell');
var clean = require('gulp-clean');
var argv = require('yargs')
  .default('tag', "v1.0")
  .alias('t', 'tag')
  .argv;

gulp.task('clean-dist', shell.task([
  'rm -rf dist'
]));

gulp.task('build', ['clean-dist'], shell.task([
  'python -m compileall *.py'
]));

gulp.task('dist', ['build'], function () {
  gulp.src(["*.pyc", "*.csv"])
    .pipe(gulp.dest('dist'));
});

gulp.task('default', ['build', 'dist']);

gulp.task('docker-publish', ['default'], shell.task([
  'docker build -t shuliyey/twitter_miner:' + argv.tag + ' .',
  'docker push shuliyey/twitter_miner:' + argv.tag
]));