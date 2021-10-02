import React, { useState } from "react";
import { ReactMic } from "react-mic";

const App = () => {
  const [isRecording, setIsRecording] = useState(false);

  const handleOnStop = (recordedBlob) => {
    console.log("recordedBlob is: ", recordedBlob);
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
    </div>
  );
};

export default App;
