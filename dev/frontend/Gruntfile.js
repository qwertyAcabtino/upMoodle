module.exports = function(grunt) {
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		
		bgShell: {
			runNode: {
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
				files: 'app/libs/{controllers,services,factories,directives}/*.js',
				tasks: ['uglify:my_target'],
				options: {
			      livereload: true,
			    }			
			},
			jsThid:{
				files: 'app/libs/third-party/**/*.js',
				tasks: ['uglify:my_target_third_party']
			}
		},
		uglify: {
			options: {
				mangle: false
			},
			my_target: {
				files: {
					'app/libs/services.min.js': ['app/libs/services/*.js'],
					'app/libs/factories.min.js': ['app/libs/factories/*.js'],
					'app/libs/controllers.min.js': ['app/libs/controllers/*.js'],
					'app/libs/directives.min.js': ['app/libs/directives/*.js']
				}
			},
			my_target_third_party: {
				files: {
					'app/libs/third-party/snackbar/angular.snackbar.min.js': ['app/libs/third-party/snackbar/angular.snackbar.js'],
					'app/libs/_dependencies.min.js': ['app/libs/third-party/**/*min.js']
				}
			}
		}
	});
	grunt.loadNpmTasks('grunt-contrib-compass');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks('grunt-bg-shell');
	grunt.registerTask('server', ['bgShell:runNode', 'uglify', 'watch']);
};