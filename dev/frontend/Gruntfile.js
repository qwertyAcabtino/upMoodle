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
				tasks: ['compass']
			}
		}
	});
	grunt.loadNpmTasks('grunt-contrib-compass');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-bg-shell');
	grunt.registerTask('server', ['bgShell:runNode', 'watch']);
};