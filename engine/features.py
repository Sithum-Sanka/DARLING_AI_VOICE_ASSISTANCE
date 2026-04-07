from playsound import playsound
import eel
#sound function for playing sound

def playAssistantSound():
    music_dir="www\\assets\\Audio\\female-robotic-voice-how-are-you.wav"
    playsound(music_dir)

#click sound for mic btn
@eel.expose
def playClickSound():
    music_dir="www\\assets\\Audio\\resampled-voice-sfx.wav"
    playsound(music_dir)