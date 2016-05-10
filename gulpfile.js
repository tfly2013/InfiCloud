var gulp = require('gulp');
var shell = require('gulp-shell');
var argv = require('yargs')
  .default('tag', "v1.0")
  .alias('t', 'tag')
  .argv;

console.log(argv.tag);

gulp.task('build', shell.task([
  'python -m compileall *.py'
]));

gulp.task('dist', ['build'], function () {
  gulp.src(["*.pyc", "*.csv"])
    .pipe(gulp.dest('dist'));
});

gulp.task('default', ['build', 'dist']);

gulp.task('package', ['default'], shell.task([
  'docker build -t shuliyey/twitter_miner:' + argv.tag + ' .',
  'docker push shuliyey/twitter_miner:' + argv.tag
]));