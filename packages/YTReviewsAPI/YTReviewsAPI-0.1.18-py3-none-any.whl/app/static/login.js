function checkAuth (user_name, pass_word) {
	var user = { username: user_name, password: pass_word};

	fetch('http://127.0.0.1:5000/api/authentication', {
		method: 'POST',
		body: JSON.stringify(user),
		headers:{
    		'Content-Type': 'application/json'
  		}
	}).then(function(response) {
	    return response.status;
	});
}



