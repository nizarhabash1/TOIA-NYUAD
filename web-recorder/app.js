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

/*---------------
//DATABASE CONFIG
----------------*/
// Below is for testing purpose
// var cloudant_USER = 'mh3833';
// var cloudant_DB = 'solarfarms';
// var cloudant_KEY = 'incelyarkationgeofterpos';
// var cloudant_PASSWORD = 'af79f43826f9067910f4f08b6dea917be3a06abb';

// Below is the cloudant database
var cloudant_USER = 'mh3833';
var cloudant_DB = 'toia';
var cloudant_KEY = 'froactsingeoverfutyrecea';
var cloudant_PASSWORD = '226b5468fc05661c704be400b468308d3d4fe291';

var cloudant_URL = "https://" + cloudant_USER + ".cloudant.com/" + cloudant_DB;

//Main Page Route - Show ALL data VIEW
app.get("/", function(req, res){
	console.log(req.params);
	res.render('index', {page: 'get all data'});
});


//SAVE an object to the db
app.post("/save", function(req,res){
	console.log("A POST!!!!");
	//Get the data from the body
	var data = req.body;
	// console.log(data);
	//Send the data to the db
	Request.post({
		url: cloudant_URL,
		auth: {
			user: cloudant_KEY,
			pass: cloudant_PASSWORD
		},
		json: true,
		body: data
	},
	function (error, response, body){
		if (!error && response.statusCode == 201){
			console.log("Saved!");
			res.json(body);
		}
		else{
			console.log("Uh oh...");
			console.log("Error: " + res.statusCode);
			console.log(data);
			res.send("Something went wrong...");
		}
 });
});

//GET objects from the database
//Also a JSON Serving route (ALL Data)
var all_json = require('../web-recorder/public/margarita2.json');

app.get("/api/all", function(req,res){
  //
	// console.log('Making a db request for all entries');
  // console.log(all_json);
  res.json(all_json.rows);

	// // Use the Request lib to GET the data in the CouchDB on Cloudant
	// Request.get({
	// 	url: cloudant_URL + "/_all_docs?include_docs=true",
	// 	auth: {
	// 		user: cloudant_KEY,
	// 		pass: cloudant_PASSWORD
	// 	},
	// 	json: true
	// },
	// function (error, response, body){
	// 	var theRows = body.rows;
	// 	//Send the data
	// 	res.json(theRows);
	// });
});

app.get("/api/sorted", function(req, res) {
	console.log('get dem sorts yay');
	Request.post({
		url: cloudant_URL + '/_find',
		auth: {
			user: cloudant_KEY,
			pass: cloudant_PASSWORD
		},
		json: true,
		body: sortQuery
	},
	function(err, response, body) {
		// do shit
		if (res.statusCode == 201 || res.statusCode == 200){
			console.log("Updated!");
			res.json(body);
		}
		else{
			console.log("Uh oh...");
			console.log("Error: " + res.statusCode);
			res.send("Something went wrong...");
		}
	});

});


//UPDATE an object in the database
app.post('/update/', function(req,res){
	console.log("Updating an object");
	var theObj = req.body;
	//Send the data to the db
	Request.post({
		url: cloudant_URL,
		auth: {
			user: cloudant_KEY,
			pass: cloudant_PASSWORD
		},
		json: true,
		body: theObj
	},
	function (error, response, body){
		if (response.statusCode == 201){
			console.log("Updated!");
			res.json(body);
		}
		else{
			console.log("Uh oh...");
			console.log("Error: " + res.statusCode);
			res.send("Something went wrong...");
		}
	});
});

//DELETE an object from the database
app.post("/delete", function(req,res){
	console.log("Deleting an object");
	var theObj = req.body;
	//The URL must include the obj ID and the obj REV values
	var theURL = cloudant_URL + '/' + theObj._id + '?rev=' + theObj._rev;
	//Need to make a DELETE Request
	Request.del({
		url: theURL,
		auth: {
			user: cloudant_KEY,
			pass: cloudant_PASSWORD
		},
		json: true
	},
	function (error, response, body){
		console.log(body);
		res.json(body);
	});
});

app.listen(3000);
console.log('Express started on port 3000');
