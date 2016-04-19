#!/share/CACHEDEV1_DATA/.qpkg/container-station/bin/python

import sys, os, time, json

class cAudioCmd(object):
	WPIPE_NAME='/tmp/.auwpp'              #client's direction
	RPIPE_NAME='/tmp/.aurpp'
	LOCK_NAME='/tmp/.lock.aupp'
	#
	CMD_INFO='info'
	CMD_ASSIGN='assign'

	# create pipe if not yet
	def __init__(self):
		if not os.path.exists(self.WPIPE_NAME):
			os.mkfifo(self.WPIPE_NAME)
			os.mkfifo(self.RPIPE_NAME)
			os.chmod(self.WPIPE_NAME, 0o777)
			os.chmod(self.RPIPE_NAME, 0o777)


	# todo, time limit, say if server doesn't exist
	def _acquire(self):
		acquired=False
		myID=str(os.getpid())
		while not acquired:
			if not os.path.exists(self.LOCK_NAME):
				os.system('echo '+myID+' >'+self.LOCK_NAME)
				os.chmod(self.LOCK_NAME, 0o777)
			with open(self.LOCK_NAME, 'r') as rfd:
				ownerID=rfd.readline().strip()
				if ownerID == myID:
					acquired=True
				else:
					if not os.path.exists('/proc/'+ownerID):
						os.system('rm -f '+self.LOCK_NAME)
				rfd.close()


	def _release(self):		
		os.system('rm -f '+self.LOCK_NAME)


	# sending command to server
	# json command array = [<command_string>, <command_arg_object>]
	# todo, it blocks if server not present
	# response
	# json response object = {'success': <result_boolean>, 'message': <msg_string>|null, 'data': <value>|null}
	# In : cmdArray - command in json array 
	# Ret: server returned json object (dict)
	def _command(self, cmdArray):
		self._acquire()
		response={}
		#access pipe
		try:
			ppOut=open(self.WPIPE_NAME, 'wt')
			ppOut.writelines('%s\n' %json.dumps(cmdArray))
			ppOut.close()
			ppIn=open(self.RPIPE_NAME, 'r')
			ret=ppIn.readline()[:-1]
			ppIn.close()
			response=json.loads(ret)   #should be a dict
		except:
			pass
		self._release()
		return response

	# json command array = [<command_string>, <command_arg_object>]
	# command string = "info"
	# info_arg_obj = null
	# response dict = {'success':<bool>, 'message': <string> , 'data' : {card_num: ['card-name', 'domain'], card_num: []}
	# Ret : response object (dict)
	def _cmdInfo(self):
		cmdList=[self.CMD_INFO]
		cmdList.append(None)
		return self._command(cmdList)

		
	# json command array = [<command_string>, <command_arg_object>]
	# command string = "assign"
	# assign_arg_obj = {"card":<num>, "domain":"domain_string"}
	# In : num - int card nr.
	#      domain - string domain to assign
	# Ret : response object (dict)
	def _cmdAssign(self, num, domain):
		cmdList=[self.CMD_ASSIGN]
		dict={}
		dict['card']=str(num)
		dict['domain']=domain
		cmdList.append(dict)
		return self._command(cmdList)


	# process info command
	def info(self):
		response=self._cmdInfo()
		if type(response) is dict:
			try:
				if response['success']:
					print '===== response ====='
					dataDict=response['data']
					for key in sorted(dataDict.keys()):
						dataList=dataDict[key]
						id=dataList[0]
						domain=dataList[1]
						print 'Card '+key+': '+id+' ('+domain+')'
					print
				elif response['message']:
					print 'Error info: '+response['message']
			except:
				pass
		else: print 'Response type error'


	# json command array = [<command_string>, <command_arg_object>]
	# command string = "assign"
	# assign_arg_obj = {"card":<num>, "domain":"domain_string"}
	# Ret : response object (dict)
	def assign(self):
		response=self._cmdInfo()
		if type(response) is dict:
			try:
				if response['success']:
					dataDict=response['data']
					#dataDict.keys() = card number list
				else: return
			except: return
		else: return
		if len(dataDict.keys()) == 0:
			print 'No sound card installed'
			return
		msg='Please select the device ('
		idx=0
		for cardNr in sorted(dataDict.keys()):
			if idx:	msg+=', '+cardNr
			else: msg+=cardNr
			idx+=1
		msg+='): '
		num=raw_input(msg)
		
		if not num in dataDict.keys():
			print 'Invalid card selected'
			return
		#command
		if dataDict[num] == 'system':
			response=self._cmdAssign(num, 'Container')
		else:
			response=self._cmdAssign(num, 'system')
		if type(response) is dict:
			try:
				if not response['success']:
					if response['message']:
						print 'Error assign: '+response['message']
			except: pass
		else: print 'Response type error'


if __name__ == '__main__':
	obj=cAudioCmd()
	stop=False
	menu = {}
	menu['1']='Show device info.'
	menu['2']='Assign device to domain'
	menu['3']='Exit'
	while True:
		options=menu.keys()
		options.sort()
		for item in options:
			print item, menu[item]
			
		select=raw_input("Please select: ")
		if select == '1':
			obj.info()
			continue			
		elif select == '2':
			obj.assign()
			continue
		elif select == '3':
			break
		else:
			print 'Unknown command'
			continue
		#exam response
		if response['success']:
			print 'Success !'
		else:
			if response['message']:
				print 'Fail: '+response['message']
			else:
				print 'Fail'
			if response['data']: print str(response['data'])
		print

			

