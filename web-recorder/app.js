//Set up requirements
var express = require("express");
var Request = require('request');
var mkdirp = require('mkdirp');
var bodyParser = require('body-parser');
var _ = require('underscore');
var jsonfile = require('jsonfile');
var fs = require('fs');
// Change this file to actual json file!
//var file = '../web-recorder/public/test.json'

// NEED TO FIGURE OUT HOW TO SAVE TO NEW FILE - ask user to give name and save to it
// make button through which can save json file to new thing
var file = '../web-recorder/public/template-scripts/temp_file.json';
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

//GET objects from the database
//Also a JSON Serving route (ALL Data)
// sort json here too
app.get("/api/all", function(req,res){
  console.log(file);
  res.json(jsonfile.readFileSync(file));
});

app.get("/script", function(req,res){
  res.render('pick-script', {page: 'get all data'});
});

app.get("/scripts", function(req,res){
  console.log("DID THIS");
  const scriptFolder = './public/avatar-garden/';
  const fs = require('fs');
  const scriptPaths = [];
  fs.readdir(scriptFolder, (err, files) => {
    files.forEach(file => {
      if(String(file)!="avatars.txt" && String(file)!="README.txt") {
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

app.post("/filename", function(req,res) {
  console.log(req.body.name);
  file = req.body.name;
  var fs = require('fs');
  var json = JSON.parse(fs.readFileSync(file));
  console.log(file);
  json = JSON.stringify(json, null, 4);
  fs.writeFile("../web-recorder/public/template-scripts/temp_file.json",json);
  file = "../web-recorder/public/template-scripts/temp_file.json";
});

// Update an answer entry in the JSON database
app.post("/update", function(req,res){
	var theObj = req.body;
  jsonfile.writeFileSync(file,theObj,function(err){
    console.error(err);
  });
});

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
});

// Save a recorded video in the file system as specified by multer upload, see above
app.post("/save",type, function(req,res){
  console.log(req.file);
  console.log("SAVING");
  console.log(req.file.originalname.substr(0,req.file.originalname.indexOf('_')));
  var avatarName = req.file.originalname.substr(0,req.file.originalname.indexOf('_'));
  fs.rename(__dirname + '/public/uploads/' + req.file.filename, __dirname + '/public/avatar-garden/' + avatarName + '/' + req.file.originalname, (err) => {
      if (err) throw err;
      console.log('Rename complete!');
    });
})

app.post("/saveAvatar", function(req,res) {
  console.log(req.body.name);
  folder = req.body.name;
  var json = jsonfile.readFileSync("../web-recorder/public/template-scripts/temp_file.json");
  json = JSON.stringify(json, null, 4);
  console.log(json);
  var fs = require('fs');
  fs.writeFile("../web-recorder/public/avatar-garden/"+folder+"/script.json",json);
});

app.get("/updateAvatarList", function(req,res){
  console.log("UPDATING AVATARS");
  const scriptFolder = './public/avatar-garden/';
  const fs = require('fs');
  const scriptPaths = [];
  fs.readdir(scriptFolder, (err, files) => {
    files.forEach(file => {
      if(String(file)!="avatars.txt" && String(file)!="README.txt" && String(file)!=".DS_Store") {
        scriptPaths.push(String(file));
      }
    });
  })
  setTimeout(function(){
    console.log(scriptPaths);
    console.log(scriptPaths.toString());
    fs.writeFile("../web-recorder/public/avatar-garden/avatars.txt",scriptPaths.toString());
    res.send("done");
  }, 1000);
});

app.listen(3000);
console.log('Express started on port 3000');
