var express = require('express'),
    http = require('http'),
    app = express(),
    httpServer = http.createServer(app);
 
app.configure(function () {
    app.set('port', 3000);
    app.use(express.static(__dirname + '/app'));
});
 
httpServer.listen(app.get('port'), function () {
    console.log("Express server listening on port %s.", httpServer.address().port);
});