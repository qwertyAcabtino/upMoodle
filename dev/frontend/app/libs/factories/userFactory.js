angular.module('upmApp').factory('User', ['$location', 'api', function($location, api){
	var returno = {
		model : undefined, 

	    destroy : function(){
	    	returno.model = undefined;
	    },

	    get : function(){
	    	if( this.model===undefined )
	    		return api.getUser()
				.then(
					function success(response) { 
						returno.model = response.data;
						return returno.model; 
					},
					function error(){
						$location.path('/login');
						return false; 
					}
				);
    		else	
    			return this.model;
	    },

	    set : function(model){
	    	this.model = model;
	    }
	};

	return returno;
}]);