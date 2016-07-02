import urllib
from threading import Thread
from multiprocessing import Process
import re

f=open('find_all_down2.txt','r')
url_list=map(lambda x : x.rstrip('\r\n') ,f.readlines())
name=re.compile(r'\d{10,}')

def down(url_list):

	count=1
	for url in url_list:
		file_name=name.findall(url)[0]+'.rar'	
		try:
			urllib.urlretrieve(url,'./res_process/'+file_name)
			#urllib.urlretrieve(url,'./res_thread/'+file_name)
			print url,count
			count=count+1
		except IOError:
			print 'down %s wrong'%url	
	return True

# s='http://hsdown.3d66.com:88/allres/res/9/2012824224019327.rar'
# print name.findall(s)

def div_mission(object_list,num):

	list_len=len(object_list)
	print list_len
	split_len=list_len//num
	return_list=[]
	for i in range(num):
		if i==num-1:
			return_list.append(object_list[i*split_len:])
		else:
			return_list.append(object_list[i*split_len:(i+1)*split_len])

	return return_list
def thread_or_process(method,job,url_list,num):

	thread_object=[method(target=job,args=(url_list[i],)) for i in range(num)]
	for work in thread_object:
		work.start()
	for work in thread_object:
		work.join()



if __name__=='__main__':

	object_list=div_mission(url_list,4)
	thread_or_process(Thread,down,object_list,4)
	thread_or_process(Process,down,object_list,4)




