import pyaudio
import wave
import geocoder
from twilio.rest import Client
import speech_recognition as sr
# Twilio credentials and phone numbers
TWILIO_ACCOUNT_SID = 'xxxxxxxxxxxxxx'
TWILIO_AUTH_TOKEN = 'xxxxxxxxxxxxx'
TWILIO_PHONE_NUMBER = 'xxxxxxxxxx'
CONTACT_PHONE_NUMBER = 'xxxxxxxxx'

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Function to capture audio
def capture_audio():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=1024)

    print("Recording...")

    frames = []

    for _ in range(0, int(RATE / 1024 * RECORD_SECONDS)):
        data = stream.read(1024)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a WAV file
    with wave.open("recorded_audio.wav", 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

# Function to get GPS coordinates
def get_gps_coordinates():
    g = geocoder.ip('me')
    return g.latlng

# Function to send an SMS with location
def send_sms_with_location():
    capture_audio()

    recognizer = sr.Recognizer()
    with sr.AudioFile("recorded_audio.wav") as source:
        print("Listening for voice command...")
        try:
            audio = recognizer.listen(source, timeout=10)
            command = recognizer.recognize_sphinx(audio).lower()
            if command=='help':
                gps_coordinates = get_gps_coordinates()
                latitude, longitude = gps_coordinates
                maps_url=f"https://google.com/maps?q={latitude},{longitude}"
                message = f"Help! I need assistance. My GPS coordinates are: Latitude {latitude:.6f}, Longitude {longitude:.6f}.Location:{maps_url}"

                client.messages.create(
                    body=message,
                    from_=+17854652517,
                    to=+919964300914
                )
                print("Help message sent with GPS coordinates.")
            else:
                print("Unrecognized command:", command)
        except sr.WaitTimeoutError:
            print("No voice command detected. Timeout reached.")

# Main loop
while True:
    user_input = input("Press Enter to start voice recognition (or 'q' to quit): ")

    if user_input.lower() == 'q':
        break

    send_sms_with_location()

