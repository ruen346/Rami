import speech_recognition as sr
from no_err import noalsaerr

r = sr.Recognizer()

while True:
    with noalsaerr() as n, sr.Microphone() as source:
        print("말하세요!")
        audio = r.listen(source)
        # recognize speech using wit.ai
        print("인식중 입니다...")
        # recognize speech using Wit.ai
        WIT_AI_KEY = "Y4IHSD5VB7NBUKCOM6AZ7KSBTSYO3ZDY" # Wit.ai keys are 32-character uppercase alphanumeric strings
        try:
            print("Wit.ai thinks you said " + r.recognize_wit(audio, key=WIT_AI_KEY))
        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))