//Set up requirements
var express = require("express");
var Request = require('request');
var mkdirp = require('mkdirp');
var bodyParser = require('body-parser');
var _ = require('underscore');
var jsonfile = require('jsonfile');
var fs = require('fs');
script = "../web-recorder/public/template-scripts/temp_file.json";
console.log(script)

var Buffer = require('buffer');
var multer  = require('multer');

//console.log(main.file_name);

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
app.use(bodyParser.urlencoded({extended: true}))


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

// Get the script directories
app.get("/scripts", function(req,res){
  console.log("DID THIS");
  const scriptFolder = './public/avatar-garden/';
  const fs = require('fs');
  const scriptPaths = [];
  fs.readdir(scriptFolder, (err, files) => {
    files.forEach(file => {
      if(String(file)!="recorder_README.md" && String(file)!="player_README.md") {
        scriptPaths.push(String(file));
        console.log(scriptPaths);
        console.log(file);
      }
    });
  })
  setTimeout(function(){
    console.log(scriptPaths);
    res.send(JSON.stringify(scriptPaths));
  }, 1000);
});

// Update the script file
app.post("/filename", function(req,res) {
  console.log(req.body.name);
  script = req.body.name;
  var fs = require('fs');
  var json = JSON.parse(fs.readFileSync(script));
  script = "../web-recorder/public/avatar-garden/"+req.body.avatar+'/script.json';
  console.log(script);
  console.log(json["name_of_avatar"]);
  json["name_of_avatar"] = req.body.avatar;
  json = JSON.stringify(json, null, 4);
  fs.writeFile("../web-recorder/public/template-scripts/temp_file.json",json);
  fs.writeFile("../web-recorder/public/avatar-garden/"+req.body.avatar+'/script.json',json);  
});

//GET objects from the database
//Also a JSON Serving route (ALL Data)
// sort json here too
app.get("/api/all", function(req,res){
  console.log(script);
  res.json(jsonfile.readFileSync(script));
});

// Update an answer entry in the JSON database
app.post("/update", function(req,res){
  console.log("updating");
	var theObj = req.body.json;
  jsonfile.writeFileSync("../web-recorder/public/avatar-garden/"+req.body.avatar+'/script.json',theObj,function(err){
    console.error("WHAT IS GOING ON");
  });
  jsonfile.writeFileSync("../web-recorder/public/template-scripts/temp_file.json",theObj,function(err){
    console.error("SECOND TIME");
  });
});

// Create an avatar directory 
app.post("/makedir", function(req,res) {
  var directoryName = req.body.name;
  mkdirp('../web-recorder/public/avatar-garden/'+directoryName, function(err) { 
    console.log("Made avatar directory");
  });
  mkdirp('../web-recorder/public/avatar-garden/'+directoryName+'/videos', function(err) {
    console.log("Made videos directory");
  });
  mkdirp('../web-recorder/public/avatar-garden/'+directoryName+'/subtitles', function(err) {
    console.log("Made subtitles directory");
  });
  var inStr = fs.createReadStream('../web-recorder/public/sample-avatar/still.png');
  var outStr = fs.createWriteStream('../web-recorder/public/avatar-garden/'+directoryName+'/still.png');
  inStr.pipe(outStr);
  var playerInStr = fs.createReadStream('../web-recorder/public/avatar-garden/player_README.md');
  var playerOutStr = fs.createWriteStream('../web-recorder/public/avatar-garden/'+directoryName+'/player_README.md');
  playerInStr.pipe(playerOutStr);
  var recorderInStr = fs.createReadStream('../web-recorder/public/avatar-garden/recorder_README.md');
  var recorderOutStr = fs.createWriteStream('../web-recorder/public/avatar-garden/'+directoryName+'/recorder_README.md');
  recorderInStr.pipe(recorderOutStr);
});

// Save a recorded video in the file system as specified by multer upload, see above
app.post("/save",type, function(req,res){
  console.log(req.file);
  console.log("SAVING");
  console.log(req.file.originalname.substr(0,req.file.originalname.indexOf('_')));
  var avatarName = req.file.originalname.substr(0,req.file.originalname.indexOf('_'));
  fs.rename(__dirname + '/public/uploads/' + req.file.filename, __dirname + '/public/avatar-garden/' + avatarName + '/videos/' + req.file.originalname, (err) => {
      if (err) throw err;
      console.log('Rename complete!');
    });
})

app.listen(3000);
console.log('Express started on port 3000');
