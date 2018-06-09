// var fs = require('fs');
// var margaritaOriginalText = fs.readFileSync('public/avatar-json/margarita.json');
// var margaritaJSON = JSON.parse(margaritaOriginalText)
// console.log(margaritaJSON);

var sortQuery = {
   "selector": {
      "index": {
         "$gte": 1000
      }
   },
   "fields": [
      "_id",
      "_rev",
      "index",
      "question",
      "answer",
      "video"
   ],
   "sort": [
      {
         "index": "asc"
      }
   ]
};

//Set up requirements
var express = require("express");
var Request = require('request');
var bodyParser = require('body-parser');
var _ = require('underscore');
var jsonfile = require('jsonfile');
var fs = require('fs')
var file = '../web-recorder/public/test.json'

//Create an 'express' object
var app = express();

//Set up the views directory
app.set("views", __dirname + '/views');
//Set EJS as templating language WITH html as an extension
app.engine('.html', require('ejs').__express);
app.set('view engine', 'html');
//Add connection to the public folder for css & js files
app.use(express.static(__dirname + '/public'));

// Enable json body parsing of application/json
app.use(bodyParser.json());

//Main Page Route - Show ALL data VIEW
app.get("/", function(req, res){
	console.log(req.params);
	res.render('index', {page: 'get all data'});
});



//GET objects from the database
//Also a JSON Serving route (ALL Data)
// sort json here too
app.get("/api/all", function(req,res){
  res.json(jsonfile.readFileSync(file));
});

app.post("/delete", function(req,res){
	console.log("Deleting an object");
	var theObj = req.body;
  jsonfile.writeFileSync(file,theObj,function(err){
    console.error(err);
  });
});

app.listen(3000);
console.log('Express started on port 3000');
