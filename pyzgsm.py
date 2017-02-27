#!/usr/bin/python
import serial
import time
import convert
import binascii
from messaging.sms import SmsDeliver
import threading



class Zgsm():
	"""docstring for Zgsm"""
	def __init__(self,portD,baudrateD):

		self.ser=serial.Serial(portD, dsrdtr=True, rtscts=True,baudrate=baudrateD, timeout=10)
		# self.ser.timeout(5)
		self.MANUFACTURER = ""
		self.MODEL = ""
		self.MODE = ""
		# self.initDevice(pin)

	def sendCommand(self,com):
		self.ser.write(com+"\r\n")
		time.sleep(2)
		ret = []
		while self.ser.inWaiting() > 0:
			msg = self.ser.readline().strip()
			msg = msg.replace("\r","")
			msg = msg.replace("\n","")
			if msg!="":
				ret.append(msg)
		return ret

	def manufacturer(self):
		rep = self.sendCommand("AT+CGMI")
		if len(rep)>1:
			for item in rep:
				if item !="OK":
					self.MANUFACTURER = item
		print self.MANUFACTURER

	def model(self):
		rep = self.sendCommand("AT+CGMM")
		print rep
		if len(rep)>1:
			for item in rep:
				if item !="OK":
					self.MODEL = item
		print self.MODEL

	def connect(self,pin):#Initialisation du dongle
		print "eee" 
		self.manufacturer()
		self.model()

		rep = self.sendCommand("ATZ")
		
		rep = self.sendCommand("at")
		if len(rep)!=0:
			print rep
			for item in rep:
				if 'OK' in item:
					
					repCpin = self.sendCommand("at+cpin?")
					print repCpin
					inserrtCode = False
					for itemCpin in repCpin:
						print itemCpin
						
						if "READY" in itemCpin:
							inserrtCode = True
						
					print inserrtCode,"inserrtCode"						
					if not inserrtCode:
						# pin = raw_input("Entrez le code PIN")

						pinRep = self.sendCommand("at+cpin='{}'".format(pin))
						print pinRep
						for itemPin in pinRep:
							if "OK" in itemPin:
								self.init()
								return True
							elif "ERROR" in itemPin:
								return False 
					else:
						self.init()
						return True

	def readSMS(self):
		print("LOOKING FOR SMS")
		list = self.sendCommand("AT+CMGL=0")
		print list

		ret = []
		if "ZTE" in self.MANUFACTURER and self.MODEL == "MF192":
			print len(list)	
			if len(list)>2 and "+CMGL" in list[1]:
				print "Liste ",list[2]
				ret.append(SmsDeliver(list[2]))
		else:
			for item in list:
				#print item
				if item.startswith("+CMGL:") == False:
					print item
					if item!="OK":
						ret.append(SmsDeliver(item))
		# print ret
		# print len(list)
		# print list[1]
		# print self.MANUFACTURER,self.MODEL,str(list[1]).startswith("+CGML:")
		return ret

	def sendUssd(self,cmd): #execution des codes USSD
		self.MODE= "USSD"
		print self.MANUFACTURER,self.MODEL
		if self.MODEL!= "MF192":
			cmd = convert.toPDU(cmd)
		print 'AT+CUSD=1,"{}",15'.format(cmd)
		rep = self.sendCommand('AT+CUSD=1,"{}",15'.format(cmd))
		self.sendCommand("at")

		print rep 
		# time.sleep(2)
		rep1 = []
		message = ""
		for item in rep:
			print item
			if "ERROR" in item:
				self.MODE= "SMS"
				return None 
			elif "+CUSD" in item:
				msg =  item.split(',')[1]
				if "ZTE" != self.MANUFACTURER :
					print self.MANUFACTURER,self.MODEL
					message =  convert.toText(eval(msg))
				elif self.MODEL == "MF192":
					if len(rep)>3:
						del rep[0]
						del rep[-1]
						message = ' '.join(rep)
						message = message.split(',')
						message = message[1]
					else:
						message = msg

		if message:
			self.MODE= "SMS"
			return message
		# while len(rep1)<=2:
				
		# 	rep = self.sendCommand('AT')
		# 	print rep,"fff"
		# 	for item in rep:
		# 		if "ERROR" in item:
		# 			return None
		# msg = list(rep[0].split(","))[1]

		# print msg
		# print convert.toText(eval(msg))
		# print msg

	def killSMS(self):
		print("DELETING ALL MESSAGES")
		print self.sendCommand("AT+CMGD=1,1")

	def init(self):
		# self.initDevice(self.PIN)
		print("SENDING HELLO")
		com="ERROR"
		count=0
		if len(com)>1:
			com = com[1]
		else :
			com = com[0]		
		while(com!="OK"):
			com=self.sendCommand("AT")
			if len(com)>1:
				com = com[1]
			else:
				com = com[0]
			print com
			count+=1
			if(count>5):
				print "COULD NOT GET A HELLO, all I got was "+com
				return
		print("OK")
		

		# rxThread = threading.Thread(target=self.readSMS)
		# rxThread.daemon = True
		# rxThread.start()

		time.sleep(1)
		print("CHANGING MESSAGE FORMAT")
		print(self.sendCommand("AT+CMGF=0"))
		self.MODE = "SMS"
		# while(True):

		# 	sms = self.readSMS()
			
		# 	for s in sms:
		# 		print ""
		# 		print "SMS"
		# 		print s.text
		# 		print s.date
		# 		time.sleep(1)
			
			# time.sleep(.1)
			
		# while 1:
		# 	inp = raw_input("Code: ")
		# 	print self.sendUssd(inp)


if __name__ == "__main__":

	modem = Zgsm()
	if modem.ser.isOpen():
		modem.main()
	else:
		print "ERROR: CAN't OPEN CONNECTION"
	modem.ser.close()

