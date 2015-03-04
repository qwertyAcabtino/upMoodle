angular.module('upmApp').factory('User', ['$location', 'api', function($location, api){
	return {
		model : undefined, 
		/*
		id: -1,
	    rol: undefined, 
	    email: undefined,
	    nick: undefined,
	    name: undefined,
	    profilePic: undefined,
	    lastTimeActive: undefined,
	    joined: undefined,
	    banned: false,
	    */	    

	    update : function(userModelIn){
	    	this.model = userModelIn;
	    }, 

	    destroy : function(){
	    	this.model = undefined;
	    },

	    get : function(){
	    	if(this.model==undefined || this.model===undefined)
	    		return api.getUser()
				.then(
					function success(response) { 
						// that.set(response.data);
						return response.data; 
					},
					function error(reason){
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
	}
}]);