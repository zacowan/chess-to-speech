import React, { useState } from "react";
import { ReactMic } from "react-mic";

const SESSION_ID = "TEST_SESSION" + Math.round(Math.random() * 10000);

const App = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [andyResponse, setAndyResponse] = useState();
  const [detectedIntent, setDetectedIntent] = useState();
  const [detectedAudio, setDetectedAudio] = useState();

  const handleOnStop = async (recordedBlob) => {
    const blob = recordedBlob.blob;
    try {
      let urlString =
        "http://localhost:5000/api/get-response?session_id=" + SESSION_ID;
      const response = await fetch(urlString, {
        method: "POST",
        body: blob,
      });
      const data = await response.json();
      setAndyResponse(data.response_text);
      setDetectedIntent(data.detected_intent);
      setDetectedAudio(data.transcribed_audio);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="App">
      <h1>Testing Input Playground</h1>
      <p>Use the audio input button below to test audio input to Andy.</p>
      <ReactMic record={isRecording} onStop={handleOnStop} />
      <button onClick={() => setIsRecording(true)} type="button">
        Start
      </button>
      <button onClick={() => setIsRecording(false)} type="button">
        Stop
      </button>
      <h2>Detected Audio</h2>
      <p>{detectedAudio || "Nothing's here."}</p>
      <h2>Detected Intent</h2>
      <p>{detectedIntent || "Nothing's here."}</p>
      <h2>Andy's Response</h2>
      <p>{andyResponse || "Nothing's here."}</p>
    </div>
  );
};

export default App;
