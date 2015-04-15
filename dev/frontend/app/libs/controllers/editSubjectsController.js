 angular.module('upmApp')
 .controller( 'editSubjectsCtrl', 
 	['$scope', '$cookies', 'api', 'User', 'userModel', 'snackbar', '$location',
 	function($scope, $cookies, api, User, userModel, snackbar, $location){
 	api.subjectsTree()
 	.success(function(data, status, headers, config){
 		$scope.university = data[0];
 	})
 	.error(function(data, status, headers, config) {
 	});


 	$scope.isAUserSubject = function (subject) {
 		subject.signedUp = User.isSignedInSubject(subject.id);
 		return User.isSignedInSubject(subject.id);
 	};


 	$scope.updateUserSubjects = function(){
 		var subjectsCheck = [];
 		angular.forEach($scope.university.children, function(career, index){
 			angular.forEach(career.children, function(course, index){
 				angular.forEach(course.children, function(subject, index){
 					if(subject.signedUp)
 						subjectsCheck.push(subject.id); 
 				});
 			});
 		});
 		api.updateUserSubjects(subjectsCheck)
 		.success(function(data, status, headers, config) {
 			snackbar.message(data);
 			api.getUser().
 			success(function(data, status, headers, config) {
 				User.set(data);
				$location.path('/subjects');
 			})	
 		})
 		.error(function(data, status, headers, config) {
 			snackbar.error(data.error);
 		});
 	}
 }]);  