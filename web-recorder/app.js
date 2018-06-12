//Set up requirements
var express = require("express");
var Request = require('request');
var bodyParser = require('body-parser');
var _ = require('underscore');
var jsonfile = require('jsonfile');
var fs = require('fs')
// Change this file to actual json file!
var file = '../web-recorder/public/test.json'
var Buffer = require('buffer');
var multer  = require('multer');

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

var storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, './')
  },
  filename: function (req, file, cb) {
    crypto.pseudoRandomBytes(16, function (err, raw) {
      cb(null, raw.toString('hex') + Date.now() + '.' + mime.extension(file.mimetype));
    });
  }
});

var upload = multer({ dest: __dirname + '/public/uploads/' },{storage:storage});
var type = upload.single('blob');

//Main Page Route - Show ALL data VIEW
app.get("/", function(req, res){
	res.render('index', {page: 'get all data'});
});

//GET objects from the database
//Also a JSON Serving route (ALL Data)
// sort json here too
app.get("/api/all", function(req,res){
  res.json(jsonfile.readFileSync(file));
});

// Update an answer entry in the JSON database
app.post("/update", function(req,res){
	var theObj = req.body;
  jsonfile.writeFileSync(file,theObj,function(err){
    console.error(err);
  });
});

// Save a recorded video in the file system as specified by multer upload, see above
app.post("/save",type, function(req,res){
  console.log(req.file);
  fs.rename(__dirname + '/public/uploads/'  + req.file.filename, __dirname + '/public/uploads/' + req.file.originalname, (err) => {
      if (err) throw err;
      console.log('Rename complete!');
    });
})

app.listen(3000);
console.log('Express started on port 3000');
