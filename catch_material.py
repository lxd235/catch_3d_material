#coding:utf-8
import requests
import re
import time
from threading import Thread
import os

def find_all_url():

	url_list=['http://www.3d66.com/material_1_'+str(i)+'.html' for i in range(87,101)]
	url_list1=[]
	if os.path.exists('all_url.txt'):
		return True
	for i in range(0,14):
		#查看是否有分页
		flag=True
		try:
			html=requests.get(url_list[i])
		except IOError:
			print 'An error accoured when open '+url_list[i]
			flag=False
		finally:
			if  os.path.exists('all_url.txt') and (not flags):
				os.remove('all_url.txt')	
		parser_list=[]
		parser_list.append(url_list[i])
		pattern2=r'<a href=(.*?)>(\d)</a>'
		find_curr=re.findall(pattern2,html.text)
		if len(find_curr)>0:
			for i in find_curr:
				new_url='http://www.3d66.com'+i[0].strip("'")
				if 'material' in i[0] :
					parser_list.append(new_url)
		url_list1.extend(parser_list)
	if not os.path.exists('all_url.txt'):
		for i in url_list1:
			with open('all_url.txt','a') as f:
				f.write(i+'\r\n')
	return True


def find_all_down():

	if os.path.exists('find_all_down.txt'):
		return True
	f=open('all_url.txt','r')
	url_list=map(lambda x : x.rstrip('\r\n'),f.readlines())
	f.close()
	flags=True
	url_list1=[]
	for i in url_list:
		try:
			html=requests.get(i)
		except IOError:
			print 'An error accoured when open '+i
			flag=False
		finally:
			if  os.path.exists('find_all_down.txt') and (not flags):
				os.remove('find_all_down.txt')	
		pattern=r'<a href=(.*?) target="_blank">'
		result=re.findall(pattern,html.text)
		result=map(lambda i:'http://www.3d66.com'+i.strip("'") ,result)
		url_list1.extend(result)
	if not os.path.exists('find_all_down.txt'):
		for i in url_list1:
			with open('find_all_down.txt','a') as f:
				f.write(i+'\r\n')
	return True

def find_all_down1():

	if os.path.exists('find_all_down1.txt'):
		return True					
	f=open('find_all_down.txt','r')
	url_list=map(lambda x : x.rstrip('\r\n').split(','),f.readlines())
	f.close()
	flags=True
	url=[]
	loop=True
	counts=1
	while loop:
		for i in url_list:
			try:
				if i[1]=='True':
					continue
				else:
					html=requests.get(i[0])
			except IOError:
				print 'an error accoured when open '+i[0]
				flags=False
			# finally:
			# 	if os.path.exists('find_all_down1.txt') and (not flags):
			# 		os.remove('find_all_down1.txt')
			i[1]='True'
			pattern=r'<a href=(.*?) target="_blank">.*?RAR.*?</a>'
			result=re.findall(pattern,html.text)
			result=map(lambda i:i.strip('"') ,result)
			url.append('http://www.3d66.com'+result[0])
			# print result[0],counts
			# counts=counts+1
		else:
			loop=False

	if not os.path.exists('find_all_down1.txt'):
		for i in url:
			with open('find_all_down1.txt','a') as f:
				f.write(i+'\r\n')
	return True

def find_all_down2():

	if os.path.exists('find_all_down2.txt'):
		return True	
	f=open('find_all_down1.txt','r')
	url_list=map(lambda x : x.rstrip('\r\n').split(','),f.readlines())
	f.close()
	flags=True
	url_down=[]
	loop=True
	counts=1
	while loop:				
		for i in url_list:
			try:
				if i[1]=='True':
					continue
				else:
					html=requests.get(i[0])
			except IOError:
				print 'an error accoured when open '+i[0]
				flags=False
			# finally:
			# 	if os.path.exists('find_all_down2.txt') and (not flags):
			# 		os.remove('find_all_down2.txt')
			i[1]='True'
			pattern=r'<a href=(.*?) target="_blank" title=(.*?) onclick=(.*?)>.*?RAR.*?</a>'
			result=re.findall(pattern,html.text)
			pos=result[0][0].find('/')
			url_down.append(('http://hsdown.3d66.com:88'+result[0][0][pos:]).rstrip('"'))
			print result[0][0][pos:],counts
			counts=counts+1
		else:
			loop=False
	if not os.path.exists('find_all_down2.txt'):
		for i in url_down:
			with open('find_all_down2.txt','a') as f:
				f.write(i+'\r\n')
	return True

def mulit_thread(url_list,job):

	threading_list=[Thread(target=job,args=(url_list[i],)) for i in range(2)]
	for i in threading_list:
		i.start()
	for i in threading_list:
		i.join()	

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

if __name__=='__main__':
	while True:
		if find_all_url():
			print 'find_all_url over'
			break
	while True:
		if find_all_down():
			print 'find_all_down over'
			break
	while True:
		if find_all_down1():
			print 'find_all_down1 over'
			break
	while True:
		if find_all_down2():
			print 'find_all_down2 over'
			break



