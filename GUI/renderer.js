// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process because
// `nodeIntegration` is turned off. Use `preload.js` to
// selectively enable features needed in the rendering
// process.
var ipc = require('electron').ipcRenderer;

var authButton = document.getElementById('analysisBtn');
authButton.addEventListener('click', function(){
    console.log("onCLick")
    ipc.once('actionReply', function(event, response){
        processResponse(response);
    })
    ipc.send('invokeAction', 'someData');
});