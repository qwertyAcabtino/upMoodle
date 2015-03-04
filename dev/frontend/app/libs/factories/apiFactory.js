angular.module('upmApp').factory('api', function($http, $cookies){
	base_url = 'http://127.0.0.1:8000/';
	return {
		getUser : function(){
			return $http({ 
				method: 'GET', 
				url:  base_url + 'user/'
			});
		},

		login : function(userEmail, userPassword){
			return $http({ 
				method: 'post', 
				url:  base_url + 'login/',
				headers: {'Content-Type': 'application/x-www-form-urlencoded'},
				transformRequest: function(obj) {
				        var str = [];
				        for(var p in obj)
				        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
				        return str.join("&");
			    },
				data : {email: userEmail, password: userPassword}
			});
		},

		logout : function(){
			return $http({ 
				method: 'POST', 
				url:  base_url + 'logout/'
			});	
		}
	}
});