import os

from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

speech_key = os.environ["SPEECH_KEY"]
speech_region = os.environ["SPEECH_REGION"]

speech_config = speechsdk.SpeechConfig(
    subscription=speech_key,
    region=speech_region,
)

audio_config = speechsdk.audio.AudioConfig(
    filename="festival_site_report.wav"
)

speech_recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config,
    audio_config=audio_config,
)

def transcribe_report():
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text

    if result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognised in the audio file.")
        return None

    if result.reason == speechsdk.ResultReason.Canceled:
        cancellation = speechsdk.CancellationDetails(result)
        print(f"Speech recognition canceled: {cancellation.reason}")

        if cancellation.error_details:
            print(f"Error details: {cancellation.error_details}")

        return None

if __name__ == "__main__":
    transcript = transcribe_report()

    if transcript:
        print("Transcript:")
        print(transcript)
        print("\nThis transcript is AI-generated and should be reviewed against the recording.")