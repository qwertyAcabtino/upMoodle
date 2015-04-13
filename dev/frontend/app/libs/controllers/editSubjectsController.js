 angular.module('upmApp')
 .controller( 'editSubjectsCtrl', ['$scope', '$cookies', 'api', 'User', 'userModel', 'snackbar', function($scope, $cookies, api, User, userModel, snackbar){
 	api.subjectsTree()
 	.success(function(data, status, headers, config){
 		$scope.careers = data;
 	})
 	.error(function(data, status, headers, config) {
 	});


 	$scope.isAUserSubject = function (subject) {
 		subject.signedUp = User.isSignedInSubject(subject.id);
 		return User.isSignedInSubject(subject.id);
 	};


 	$scope.updateUserSubjects = function(){
 		var subjectsCheck = [];
 		angular.forEach($scope.careers, function(career, index){
 			angular.forEach(career.children, function(course, index){
 				angular.forEach(course.children, function(subject, index){
 					if(subject.signedUp)
 						subjectsCheck.push(subject.id); 
 				});
 			});
 		});
 		api.updateUserSubjects(subjectsCheck)
 		.success(function(data, status, headers, config) {
 			snackbar.message(data.message);
 			api.getUser().
 			success(function(data, status, headers, config) {
 				snackbar.message(data);
 				User.set(data);
 			})	
 		})
 		.error(function(data, status, headers, config) {
 			snackbar.error(data.error);
 		});
 	}
 }]);  