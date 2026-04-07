// Receive status from Python (Listening / Recognizing)
eel.expose(showStatus);

function showStatus(message) {
    document.getElementById("statusText").innerText = message;
}

// Receive recognized text
eel.expose(showUserText);

function showUserText(text) {
    document.getElementById("statusText").innerText = "You said: " + text;
}

// Call Python listen()
async function startListening() {
    let text = await eel.listen()();
    console.log("User said:", text);
}

eel.expose(showHood);

function showHood() {
    $("#Oval").attr("hidden", false);
    $("#Siri-Wave").attr("hidden", true);
}