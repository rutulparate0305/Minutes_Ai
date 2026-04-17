const API_URL = "http://127.0.0.1:8000/transcribe";


// Upload audio manually
async function uploadAudio(event) {
    event.preventDefault();

    const fileInput = document.getElementById("audioFile");

    if (!fileInput.files.length) {

        alert("Select file first");
        return;
    }

    const file = fileInput.files[0];

    let formData = new FormData();

    formData.append("file", file);

    try {

        let response = await fetch(API_URL, {

            method: "POST",
            body: formData

        });

        let data = await response.json();

        displayResults(data);

        addMeetingHistory(file.name);

    }

    catch (error) {

        console.error("Upload failed:", error);

    }

}


// Display transcript + summary
function displayResults(data) {

    document.getElementById("transcriptBox").value =
        data.transcript || "";

    document.getElementById("summaryBox").value =
        data.summary || "";

    document.getElementById("speakerBox").value =
        data.speakers || "";

    document.getElementById("actionBox").value =
        data.action_items || "";

}


// Sidebar history update
function addMeetingHistory(filename) {

    let history = document.getElementById("meetingHistory");

    let item = document.createElement("li");

    item.className = "list-group-item";

    item.innerText = filename;

    history.appendChild(item);

}


// 🎤 Microphone recording support

let recorder;

let audioChunks = [];

let isRecording = false;


// START recording

async function startRecording() {

    if (isRecording) {

        alert("Already recording");

        return;

    }

    try {

        let stream = await navigator.mediaDevices.getUserMedia({

            audio: true

        });

        recorder = new MediaRecorder(stream);

        audioChunks = [];

        recorder.ondataavailable = event => {

            audioChunks.push(event.data);

        };

        recorder.start();

        isRecording = true;

        alert("Recording started 🎤");

    }

    catch (error) {

        alert("Microphone permission denied");

        console.error(error);

    }

}


// STOP recording

function stopRecording() {

    if (!isRecording) {

        alert("Recording not started yet");

        return;

    }

    recorder.stop();

    recorder.onstop = uploadRecording;

    isRecording = false;

    alert("Recording stopped ⛔");

}


// Upload recorded audio automatically

async function uploadRecording() {

    let blob = new Blob(audioChunks, {

        type: "audio/wav"

    });

    let formData = new FormData();

    formData.append("file", blob, "meeting.wav");

    try {

        let response = await fetch(API_URL, {

            method: "POST",

            body: formData

        });

        let data = await response.json();

        displayResults(data);

        addMeetingHistory("Recorded Meeting");

    }

    catch (error) {

        console.error("Recording upload failed:", error);

    }

}