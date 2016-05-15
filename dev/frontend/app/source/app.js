var app = angular.module("upmApp", ['ngRoute', 'ngCookies', 'angular.snackbar', 'ui.bootstrap', 'angular-loading-bar', 'angularFileUpload', 'ui.calendar'])
	.filter('split', function() {
        return function(input, splitChar, splitIndex) {
            // do some bounds checking here to ensure it has that index
            return input.split(splitChar)[splitIndex];
        };
    });  

app.config(['$routeProvider', '$locationProvider', '$httpProvider', 'cfpLoadingBarProvider', 
	function($routeProvider, $locationProvider, $httpProvider, cfpLoadingBarProvider) {

		cfpLoadingBarProvider.includeSpinner = false;

		var userPromise = ['User', function(User){ return User.get(); }];
		var subjectsPromise = ['SubjectsTree', function(SubjectsTree){ return SubjectsTree.get(); }];
		var subjectsTreePromise = ['api', function(api){ return api.level.getTree(); }];

		$httpProvider.defaults.withCredentials = true;
		$routeProvider
		.when('/login', {
			templateUrl: 'views/login.html',
			controller: 'loginController',
			css: [
		        {
		          href: 'page4/page4.css',
		          persist: true
		        }, {
		          href: 'page4/page4.mobile.css',
		          /* Media Query support via window.matchMedia API
		           * This will only add the stylesheet if the breakpoint matches */
		          media: 'screen and (max-width : 768px)'
		        }, {
		          href: 'page4/page4.print.css',
		          media: 'print'
		        }
		    ]
		})
		.when('/signup', {
			templateUrl: 'views/signup.html',
			controller: 'signUpCtrl',
		})
		.when('/recoverPassword', {
			templateUrl: 'views/recoverPassword.html',
			controller: 'recoverPasswordCtrl',
		})
		.when('/confirm_email/:token', {
			templateUrl: 'views/confirm_email.html',
			controller: 'confirmEmailCtrl',
		})
		.when('/dashboard', {
			templateUrl: 'views/dashboard.html',
			controller: 'dashboardCtrl',
			resolve : {  
				userModel : userPromise
			}
		})
		.when('/subjects', {
			templateUrl: 'views/subjects.html',
			controller: 'subjectsCtrl',
			resolve : {  
				userModel : userPromise
			}
		})
		.when('/subject/:id', {
			templateUrl: 'views/subject.html',
			controller: 'subjectCtrl',
			resolve : {  
				userModel : userPromise,
				subjectsNestModel : subjectsPromise,
			}
		})
		.when('/editSubjects', {
			templateUrl: 'views/editSubjects.html',
			controller: 'editSubjectsCtrl',
			resolve : {  
				userModel : userPromise,
				subjectsNestModel : subjectsPromise,
			}
		})
		.when('/profile', {
			templateUrl: 'views/profile.html',
			controller: 'profileCtrl',
			resolve : {
				userModel : userPromise
			}
		})
		.when('/notes', {
			templateUrl: 'views/notes.html',
			controller: 'notesCtrl',
			resolve : {
				userModel : userPromise,
				subjectsNestModel : subjectsPromise,
			}
		})
		.when('/calendar', {
			templateUrl: 'views/calendar.html',
			controller: 'calendarController',
			resolve : {
				userModel : userPromise,
				subjectsNestModel : subjectsPromise,
			}
		})
		.otherwise({
			redirectTo: '/login'
		});
	}])
.run(function($location, $http, $cookies, api, User){
	api.userMe.get().
	success(function(data, status, headers, config) {
		User.set(data);
	})	
	.error(function(data, status, headers, config) {
		if( 
			$location.path().indexOf("recoverPassword")!=-1 &&
			$location.path().indexOf("confirm_email")!=-1 &&
			$location.path().indexOf("signup")!=-1 
		)
			$location.path('/login');
	});
});