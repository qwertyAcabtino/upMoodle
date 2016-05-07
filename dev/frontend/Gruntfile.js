module.exports = function(grunt) {
	grunt.loadNpmTasks('grunt-contrib-compass');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks('grunt-contrib-jshint');
	grunt.loadNpmTasks('grunt-contrib-concat');
	grunt.loadNpmTasks('grunt-bg-shell');

	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),

		'meta': {
			'externalDependencies': [
				'bower_components/angular/angular.js',
				'bower_components/angular-cookies/angular-cookies.js',
				'bower_components/angular-bootstrap/ui-bootstrap-tpls.js',
				'bower_components/angular-route/angular-route.js',
				'bower_components/ng-file-upload/angular-file-upload.js',
				'bower_components/ng-file-upload/ng-file-upload.js',
				'bower_components/angular-loading-bar/build/loading-bar.js',
				'app/libs/snackbar/angular.snackbar.js',
			],

			'projectJsFiles': ['app/js/**/*.js']
		},
		
		bgShell: {
			runExpress: {
				cmd: 'node server.js',
				bg: true
			}
		},
		compass: {
			dist: {
				options: {
					sassDir: 'app/stylesheets/sass',
					cssDir: 'app/stylesheets/'
				}
			}
		},
		watch: {
			css: {
				files: '**/*.scss',
				tasks: ['compass'],
				options: {
					livereload: true,
				}			
			},
			jsShelf:{
				files: 'app/js/**/*.js',
				tasks: ['build'],
				options: {
					livereload: true,
				}			
			},
		},

		'jshint': {
      		'beforeconcat': ['<%= meta.projectJsFiles %>'],
		},

		'concat': {
	    	'dist': {
        		'src': ['<%= meta.externalDependencies %>','<%= meta.projectJsFiles %>'],
		        'dest': 'app/dist/<%= pkg.namelower %>-<%= pkg.version %>.js'
      		}
    	},

		'uglify': {
      		'options': {
        		'mangle': false
      		},  
	      	'dist': {
        		'files': {
          			'app/dist/<%= pkg.namelower %>-<%= pkg.version %>.min.js': ['app/dist/<%= pkg.namelower %>-<%= pkg.version %>.js']
        		}
      		}
    	},
	});
	grunt.registerTask('build', ['jshint', 'concat', 'uglify']);
	grunt.registerTask('server', ['bgShell:runExpress', 'build', 'watch']);
};