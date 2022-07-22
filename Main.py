from Mail import Mail
from Detector import Detector
import time
import winsound
import sys

def sendEmptyMail():
    sender_address = 'botggrama@gmail.com'
    sender_pass = 'tgragacg1'
    receiver_address = 'gabriel.grama95@gmail.com'
    
    mail = Mail(sender_address, sender_pass)
    mail.send(receiver_address, "Test!", "", [])

def soundAlarm():
	duration = 3000  # milliseconds
	freq = 750  # Hz
	winsound.Beep(freq, duration)

def mailAlarm(mail, receiver_address, info, filePath):
	mail, receiver_address
	mail.send(receiver_address, "Notify; noreply !", info, [filePath]) 
	time.sleep(60*90)

def adapterAlarm(alarm, context=None):
	if alarm is soundAlarm:
		return lambda params: soundAlarm()
	elif alarm is mailAlarm:
		return lambda params: mailAlarm(context['mail'], context['receiver_address'], params['info'], params['filepath'])

def doJob(withAutoLock):
    sender_address = 'botggrama@gmail.com'
    sender_pass = 'tgragacg1'
    receiver_address = 'gabriel.grama95@gmail.com'
    
    mail = Mail(sender_address, sender_pass)
    
    Detector([
		#adapterAlarm(mailAlarm, context={'mail':mail, 'receiver_address':receiver_address}),
		adapterAlarm(soundAlarm),
        ], withAutoLock=withAutoLock).run()

def main():
    #sendEmptyMail()
    argv = sys.argv[1:]
    withAutoLock = True if len(argv)>0 else False
    doJob(withAutoLock=withAutoLock)
    
if __name__ == "__main__":
    # execute only if run as a script
    main()