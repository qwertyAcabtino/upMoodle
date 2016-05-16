angular.module('upmApp').factory('api', function($http, $cookies, $upload, $window){
	var base_url = 'http://127.0.0.1:8000/';
	var user_pics_url = base_url;

	return {

		auth : {

			login : function(userEmail, userPassword){
				return $http({ 
					method: 'POST', 
					url:  base_url + 'auth/login/',
					headers: {'Content-Type': 'application/json'},
					data : {
						email: userEmail, 
						password: userPassword
					}
				});
			},

			logout : function(){
				return $http({ 
					method: 'POST', 
					url:  base_url + 'auth/logout/'
				});	
			},

			signup : function(user){
				return $http({ 
					method: 'post', 
					url:  base_url + 'auth/signup/',
					headers: {'Content-Type': 'application/json'},
					data : {
						email: user.email, 
						password: user.password, 
						nick: user.nick, name: 
						user.name
					}
				});
			},

			confirmEmail : function(token){  
				return $http({     
					method: 'POST',      
					url:  base_url + 'confirm_email/',
					headers: {'Content-Type': 'application/json'},
					data: {
						token: token
					}
				});
			},

			recoverPassword : function(email){
				return $http({ 
					method: 'POST', 
					url:  base_url + 'auth/recover_password/',
					headers: {'Content-Type': 'application/json'},
					data: {
						email: email
					}
				});	
			}
		},

		userMe : {
			get : function(){
				return $http({ 
					method: 'GET', 
					url:  base_url + 'user/'
				});
			},

			update : function(user){
				var userData = {
					email: user.email, 
					name: user.name, 
					nick: user.nick, 
					password: user.password
				};

				if(user.password){
					userData.password = user.password;
				}
				return $http({ 
					method: 'POST', 
					url:  base_url + 'user/',
					headers: {'Content-Type': 'application/json'},
					data: userData
				});
			},

			updateSubjects : function (subjects) {
				return $http({ 
					method: 'post', 
					url:  base_url + 'user/subjects/',
					headers: {'Content-Type': 'application/json'},
					data : {
						ids: subjects || [] 
					}
				});
			},

			updateAvatar : function( avatar ){
				console.log( avatar );
				return $http({
					method: 'POST',
					url: base_url + 'user/avatar/',
					headers: {
						'Content-Type': 'multipart/form-data'
					},
					data: {
						avatar: avatar
					},
					transformRequest: function (data, headersGetter) {
						var formData = new FormData();
						angular.forEach(data, function (value, key) {
							formData.append(key, value);
						});

						var headers = headersGetter();
						delete headers['Content-Type'];

						return formData;
					}
				});
			},
		},

		note : {
			update : function (data) {
				return $http({
					method: 'PUT', 
					url:  base_url + 'note/' + data.id +'/',
					headers: {'Content-Type': 'application/json'},
					data : {text: data.text, topic: data.topic, level_id: data.level.id}
				});
			},

			delete:  function(noteId){
				return $http.delete(base_url + 'note/' + noteId +'/');
			},

			create : function(data){
				return $http({
					method: 'post', 
					url:  base_url + 'note/',
					headers: {'Content-Type': 'application/json'},
					data : {
						text: data.text, 
						topic: data.topic, 
						level_id: data.level_id
					}
				});
			},
		},

		calendar : {
			month : function(month){
				return $http({
					method: 'GET',
					url: base_url + 'calendar/month/' + new Date().getFullYear() +'-' + month + '/_user'
				});
			}
		},

		notes : {
			latest : function(){
				return $http({
					method: 'GET',
					url: base_url + 'note/_latest'
				});
			},
		},

		files : {
			latest : function(){
				return $http({
					method: 'GET',
					url: base_url + 'file/_latest'
				});
			},
		},
		
		level : {
			getTree : function(){
				return $http({
					method: 'GET',
					url: base_url + 'level/_tree'
				});
			},

			getNotes : function(levelId, recursive){
				recursive = recursive || false;
				return $http({
					method: 'GET',
					url: base_url + 'level/' + levelId +"/notes" + "?recursive=" + recursive
				});
			},

			getFiles : function(levelId){
				return $http({
					method: 'GET',
					url: base_url + 'level/' + levelId +"/files"
				});
			},
		},

		filetype : {

			getAll : function(){
				return $http({
					method: 'GET',
					url: base_url + 'filetype/_all'
				});
			}
		},

		file : {

			_getBinary : function(hash){
				var url = base_url + 'file/' + hash;
				$window.open( url );
			},

			_getMetadata : function(hash){
				return $http.get(
					base_url + 'file/' + hash,
					{
						headers: {'Accept': 'application/json'}
					}
				);
			},

			get : function (hash, type) {
				switch (type) {
					case 'binary':
						return this._getBinary(hash);
					case 'metadata':
						return this._getMetadata(hash);
					default:
						throw "Not implemented function";
				}
			},

			delete : function (hash) {
				return $http.delete(base_url + 'file/' + hash);
			},

			_updateMetadata : function (file){
				return $http({
					method: 'PUT', 
					url:  base_url + 'file/' + file.hash,
					headers: {'Content-Type': 'application/json'},
					data : {
						text: file.text, 
						name: file.name,
						fileType_id : file.fileType.id
					}
				});
			},

			update : function(data, type){
				switch (type) {
					case 'metadata':
						return this._updateMetadata(data);
					default:
						throw "Not implemented function";
				}
			},

			create : function(binary, metadata) {
				return $http({
					method: 'POST',
					url: base_url + 'file/',
					headers: {
						'Content-Type': 'multipart/form-data'
					},
					data: {
						subject_id: metadata.subjectId,
						uploader_id : metadata.userId,
						name : metadata.fileInfo.name,
						text : metadata.fileInfo.text,
						fileType_id : metadata.fileType.id,
						file: binary
					},
					transformRequest: function (metadata, headersGetter) {
						var formData = new FormData();
						angular.forEach(metadata, function (value, key) {
							formData.append(key, value);
						});

						var headers = headersGetter();
						delete headers['Content-Type'];

						return formData;
					}
				});
			}
		},
	};
});  