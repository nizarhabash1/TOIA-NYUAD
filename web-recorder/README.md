# Creating new avatar with this web recorder

This is a browser based video recorder for creating new TOIA avatars.

### Scipts
**Camera.js** uses WebRTC library to record videos.

To use different resolution (for a Web cam), update `value` in the `getVideoResolutions` function

**App.js** is Node back-end and handles HTTP get and post requests. App.js uses multer to store video files in the local file system.

**Main.js** handles front-end user interaction and sends requests to app.js.

### Run
To run the app, do `npm install` and `nodemon`

Go to http://localhost:3000/ to view the application.

You will need to grant access for microphone and camera to browser.

