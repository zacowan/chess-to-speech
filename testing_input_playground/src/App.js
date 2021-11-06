import React, { useState } from "react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

const SESSION_ID = "TEST_SESSION" + Math.round(Math.random() * 10000);

const App = () => {
  const [recordingTimeStart, setRecordingTimeStart] = useState();
  const [boardStr, setBoardStr] = useState("");
  const [data, setData] = useState();
  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
  } = useSpeechRecognition();

  const handleOnStart = () => {
    setRecordingTimeStart(new Date());
    SpeechRecognition.startListening({ continuous: true });
  };

  const handleOnStop = async () => {
    SpeechRecognition.stopListening();
    const endTime = new Date();
    const recordingTimeMs = endTime.getTime() - recordingTimeStart.getTime();
    try {
      let urlString = `http://127.0.0.1:5000/api/get-response?session_id=${SESSION_ID}?board_str=${boardStr}?detected_text=${transcript}?recording_time_ms=${recordingTimeMs}`;
      const response = await fetch(urlString, {
        method: "POST",
        body: new Blob(),
        mode: "no-cors",
      });
      const data = await response.json();
      console.log(data);
      setData(JSON.parse(data));
    } catch (error) {
      console.log(error);
    } finally {
      resetTranscript();
    }
  };

  if (!browserSupportsSpeechRecognition) {
    return (
      <div className="App">
        <p>This browser does not support speech recognition. Try Chrome.</p>
      </div>
    );
  }

  return (
    <div className="App">
      <h1>Testing Input Playground</h1>
      <p>Use the audio input button below to test audio input to Andy.</p>
      <button onClick={handleOnStart} type="button">
        Start
      </button>
      <button onClick={() => handleOnStop()} type="button">
        Stop
      </button>
      <p>Listening: {listening ? "On" : "Off"}</p>
      {data && (
        <React.Fragment>
          <h2>Detected Audio</h2>
          <p>{transcript || "Nothing's here."}</p>
          <h2>Detected Intent</h2>
          <p>{data["fulfillment_info"]["intent_name"] || "Nothing's here."}</p>
          <h2>Andy's Response</h2>
          <p>{data["response_text"] || "Nothing's here."}</p>
        </React.Fragment>
      )}
    </div>
  );
};

export default App;
