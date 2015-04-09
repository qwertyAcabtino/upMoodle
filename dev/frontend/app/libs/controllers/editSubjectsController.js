 angular.module('upmApp')
 .controller( 'editSubjectsCtrl', ['$scope', '$cookies', 'api', 'User', 'userModel', function($scope, $cookies, api, User, userModel){
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
		console.log(subjectsCheck);	
 	}
 }]);  