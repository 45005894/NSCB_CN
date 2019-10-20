from urllib.request import urlopen
import requests
try:
	import ujson as json
except:
	import json
import Hex
from binascii import hexlify as hx, unhexlify as uhx
import pykakasi
import os
import Print
from tqdm import tqdm
import time
import csv
import chardet
from googletrans import Translator
import ast

# SET ENVIRONMENT
squirrel_dir=os.path.abspath(os.curdir)
NSCB_dir=os.path.abspath('../'+(os.curdir))

if os.path.exists(os.path.join(squirrel_dir,'ztools')):
	NSCB_dir=squirrel_dir
	zconfig_dir=os.path.join(NSCB_dir, 'zconfig')	  
	ztools_dir=os.path.join(NSCB_dir,'ztools')
	squirrel_dir=ztools_dir
elif os.path.exists(os.path.join(NSCB_dir,'ztools')):
	squirrel_dir=squirrel_dir
	ztools_dir=os.path.join(NSCB_dir, 'ztools')
	zconfig_dir=os.path.join(NSCB_dir, 'zconfig')
else:	
	ztools_dir=os.path.join(NSCB_dir, 'ztools')
	zconfig_dir=os.path.join(NSCB_dir, 'zconfig')

def get_titlesurl(tfile):
	with open(tfile,'rt',encoding='utf8') as csvfile:
		readCSV = csv.reader(csvfile, delimiter='|')	
		i=0	
		for row in readCSV:
			if i==0:
				csvheader=row
				i=1
				if 'URL' in csvheader:
					weburl=csvheader.index('URL')	
				else:break	
			else:	
				url=str(row[weburl])
				return url	
				
def get_otherurl(tfile,dbname):
	with open(tfile,'rt',encoding='utf8') as csvfile:
		readCSV = csv.reader(csvfile, delimiter='|')	
		i=0	
		for row in readCSV:
			if i==0:
				csvheader=row
				i=1
				if 'URL' and 'NAME' in csvheader:
					weburl=csvheader.index('URL')
					name=csvheader.index('NAME')
				else:break	
			else:
				if dbname.lower() == str(row[name]).lower():
					url=str(row[weburl])
					return url

if os.path.exists(zconfig_dir):
	DATABASE_folder=os.path.join(zconfig_dir, 'DB')
	nutdbfile=os.path.join(DATABASE_folder,'nutdb.json')	
	urlconfig=os.path.join(zconfig_dir,'NUT_DB_URL.txt')
	urlregions=os.path.join(zconfig_dir,'NUT_DB_REGIONS_URL.txt')	
	if os.path.exists(urlconfig):
		json_url = get_titlesurl(urlconfig)	
	else:
		urlconfig=os.path.join(squirrel_dir,'NUT_DB_URL.txt')
		urlregions=os.path.join(squirrel_dir,'NUT_DB_REGIONS_URL.txt')		
		DATABASE_folder=squirrel_dir
		if os.path.exists(urlconfig):	
			json_url = get_titlesurl(urlconfig)		
		else:	
			json_url='https://raw.githubusercontent.com/blawar/titledb/master/titles.US.en.json'
else:
	nutdbfile='nutdb.json'
	urlconfig=os.path.join(squirrel_dir,'NUT_DB_URL.txt')
	urlregions=os.path.join(squirrel_dir,'NUT_DB_REGIONS_URL.txt')
	DATABASE_folder=squirrel_dir	
	if os.path.exists(urlconfig):	
		json_url = get_titlesurl(urlconfig)		
	else:	
		json_url='https://raw.githubusercontent.com/blawar/titledb/master/titles.US.en.json'

if not os.path.exists(DATABASE_folder):
	os.makedirs(DATABASE_folder)	
def getnutdb():
	response = requests.get(json_url, stream=True)
	if '<Response [404]>'!=str(response):
		if os.path.exists(nutdbfile):
			try:os.remove(nutdbfile)
			except:pass			
		try:
			with open(nutdbfile,'wb') as nutfile:
				print('Getting NUTDB json')
				for data in response.iter_content(65536):
					nutfile.write(data)
					if not data:
						break
		except BaseException as e:
			Print.error('Exception: ' + str(e))		
			try:os.remove(nutdbfile)
			except:pass	
		return True				
	else:
		print(json_url)
		print("Response 404. Old Files weren't removed")
		return False			

def regionurl(region):	
	with open(urlregions,'rt',encoding='utf8') as csvfile:
		readCSV = csv.reader(csvfile, delimiter='|')	
		i=0	
		for row in readCSV:
			if i==0:
				csvheader=row
				i=1
				if 'REGION' and 'URL' in csvheader:
					reg=csvheader.index('REGION')
					weburl=csvheader.index('URL')	
				else:break	
			else:	
				if str(region).lower()==str(row[reg]).lower():
					url=str(row[weburl])
					return url
					
def region_refresh_time(region):	
	th=24;tm=0;ts=0
	with open(urlregions,'rt',encoding='utf8') as csvfile:
		readCSV = csv.reader(csvfile, delimiter='|')	
		i=0	
		for row in readCSV:
			if i==0:
				csvheader=row
				i=1
				if 'REGION'in csvheader:
					reg=csvheader.index('REGION')
				else:break	
				if 'REFRESH(h)'in csvheader:
					indexh=csvheader.index('REFRESH(h)')
				else:break		
				if 'REFRESH(m)'in csvheader:
					indexm=csvheader.index('REFRESH(m)')
				else:break	
				if 'REFRESH(s)'in csvheader:
					indexs=csvheader.index('REFRESH(s)')
				else:break								
			else:	
				if str(region).lower()==str(row[reg]).lower():
					try:
						th=int(str(row[indexh]))
					except:	pass
					try:
						tm=int(str(row[indexm]))
					except:	pass
					try:
						ts=int(str(row[indexs]))
					except:	pass		
					break
	return th,tm,ts		
	
def others_refresh_time(tfile,dbname):	
	th=24;tm=0;ts=0
	with open(tfile,'rt',encoding='utf8') as csvfile:
		readCSV = csv.reader(csvfile, delimiter='|')	
		i=0	
		for row in readCSV:
			if i==0:
				csvheader=row
				i=1
				if 'NAME'in csvheader:
					name=csvheader.index('NAME')
				else:break	
				if 'REFRESH(h)'in csvheader:
					indexh=csvheader.index('REFRESH(h)')
				else:break		
				if 'REFRESH(m)'in csvheader:
					indexm=csvheader.index('REFRESH(m)')
				else:break	
				if 'REFRESH(s)'in csvheader:
					indexs=csvheader.index('REFRESH(s)')
				else:break								
			else:	
				if str(dbname).lower()==str(row[name]).lower():
					try:
						th=int(str(row[indexh]))
					except:	pass
					try:
						tm=int(str(row[indexm]))
					except:	pass
					try:
						ts=int(str(row[indexs]))
					except:	pass		
					break
	return th,tm,ts		

def titles_refresh_time():	
	th=24;tm=0;ts=0
	with open(urlconfig,'rt',encoding='utf8') as csvfile:
		readCSV = csv.reader(csvfile, delimiter='|')	
		i=0	
		for row in readCSV:
			if i==0:
				csvheader=row
				i=1
				if 'REFRESH(h)'in csvheader:
					indexh=csvheader.index('REFRESH(h)')
				else:break		
				if 'REFRESH(m)'in csvheader:
					indexm=csvheader.index('REFRESH(m)')
				else:break	
				if 'REFRESH(s)'in csvheader:
					indexs=csvheader.index('REFRESH(s)')
				else:break								
			else:	
				try:
					th=int(str(row[indexh]))
				except:	pass
				try:
					tm=int(str(row[indexm]))
				except:	pass
				try:
					ts=int(str(row[indexs]))
				except:	pass		
				break
	return th,tm,ts			
					
def check_region_file(region):	
	try:
		th,tm,ts=region_refresh_time(region)
	except:
		th=24;tm=0;ts=0
	f='nutdb_'+region+'.json'
	regionfile=os.path.join(DATABASE_folder,f)		
	if not os.path.exists(regionfile):
		get_regionDB(region)
		return True			
	elif (time.time() - os.path.getmtime(regionfile)) > (th*60*60+tm*60+ts):
		get_regionDB(region)	
		return True			
	else:
		try:
			with open(regionfile) as json_file:
				pass
				return 'Refresh time limit not reached'
		except:
			get_regionDB(region)	
			return True
	return	False							
			
def check_other_file(dbfile,dbname):	
	if str(dbname.lower()).endswith('_txt'):
		ext='.txt'
		enderf=dbname[:-4]
	else:
		ext='.json'	
		enderf=dbname
	try:
		th,tm,ts=others_refresh_time(dbfile,dbname)
	except:
		th=24;tm=0;ts=0
	f='nutdb_'+enderf+ext
	_dbfile_=os.path.join(DATABASE_folder,f)		
	if not os.path.exists(_dbfile_):
		get_otherDB(dbfile,dbname,f)
		return True
	elif (time.time() - os.path.getmtime(_dbfile_)) > (th*60*60+tm*60+ts):
		get_otherDB(dbfile,dbname,f)	
		return True		
	else:
		try:
			with open(_dbfile_) as json_file:
				pass
				return 'Refresh time limit not reached'
		except:
			get_otherDB(dbfile,dbname,f)
			return True
	return	False

def get_otherDB(dbfile,dbname,f):
	url=get_otherurl(dbfile,dbname)
	_dbfile_=os.path.join(DATABASE_folder,f)	
	response = requests.get(url, stream=True)
	if '<Response [404]>'!=str(response):	
		if os.path.exists(_dbfile_):
			try:os.remove(_dbfile_)
			except:pass		
		try:
			with open(_dbfile_,'wb') as nutfile:
				print('Getting NUTDB json "'+dbname+'"')
				for data in response.iter_content(65536):
					nutfile.write(data)
					if not data:
						break
		except BaseException as e:
			Print.error('Exception: ' + str(e))		
			try:os.remove(_dbfile_)
			except:pass	
		return True				
	else:
		print(json_url)
		print("Response 404. Old Files weren't removed")	
		return False			
		
def get_regionDB(region):
	url=regionurl(region)
	f='nutdb_'+region+'.json'
	regionfile=os.path.join(DATABASE_folder,f)	
	response = requests.get(url, stream=True)	
	if '<Response [404]>'!=str(response):	
		if os.path.exists(regionfile):
			try:os.remove(regionfile)
			except:pass	
		try:
			with open(regionfile,'wb') as nutfile:
				print('Getting NUTDB json "'+region+'"')
				for data in response.iter_content(65536):
					nutfile.write(data)
					if not data:
						break
		except BaseException as e:
			Print.error('Exception: ' + str(e))		
			try:os.remove(regionfile)
			except:pass	
		return True	
	else:
		print(json_url)
		print("Response 404. Old Files weren't removed")
		return False		
		
def force_refresh():
	getnutdb()
	get_regionDB('America')	
	get_regionDB('Europe')	
	get_regionDB('Japan')	
	get_regionDB('Asia')		
	get_otherDB(urlconfig,'versions_txt','nutdb_versions.txt')
	get_otherDB(urlconfig,'cheats','nutdb_cheats.json')		
	return True
					
def check_current():	
	try:
		th,tm,ts=titles_refresh_time()
	except:
		th=24;tm=0;ts=0	
	if not os.path.exists(nutdbfile):
		getnutdb()
		return True			
	elif (time.time() - os.path.getmtime(nutdbfile)) > (th*60*60+tm*60+ts):
		getnutdb()		
		return True			
	else:
		try:
			with open(nutdbfile) as json_file:
				pass
				return 'Refresh time limit not reached'
		except:
			getnutdb()	
			return True
	return	False	
	
def force_update():			
	getnutdb()
	return
try:	
	check_current()
except:pass	
	
def get_contentname(titleid,roman=True,format='tabs'):
	cname=False
	with open(nutdbfile) as json_file:	
		data = json.load(json_file)		
		titleid=titleid.lower()
		for i in data:
			check=False
			for j,k in data[i].items():
				if str(j) == 'id':
					if str(k).lower()==titleid:
						check=True	
				if str(j) == 'name' and check==True:
					cname=str(k)
					break
		if cname != False and roman == True:
			converter = kakashi_conv()
			cname=converter.do(cname)	
			if cname[0] == ' ':
				basename=basename[1:]			
			cname=cname[0].upper()+cname[1:]
			cname=set_roma_uppercases(cname)
		else:pass						
		if cname==False:
			return False
	return 	cname			


def get_contenregions(titleid):
	baseid=get_baseid(titleid);baseid=baseid.lower()	
	langue=False
	rglist=['America','Europe','Japan','Asia']
	regions=list()
	titleid=titleid.lower()	
	if str(titleid).endswith('000'):
		baseid=titleid
	elif str(titleid).endswith('800'):	
		baseid=titleid[:-3]+'000'
	else:
		titleid=titleid.lower()
		baseid=get_dlc_baseid(titleid);baseid=baseid.lower()	
	for region in rglist:
		f='nutdb_'+region+'.json'
		regionfile=os.path.join(DATABASE_folder,f)	
		check_region_file(region)
		with open(regionfile) as json_file:	
			data = json.load(json_file)		
			for i in data:
				dict=data[i]
				if 'id' in dict and not region in regions:
					if str(dict['id']).lower()==baseid:
						regions.append(region)
						break
	return regions
	
def get_icon(titleid):
	baseid=get_baseid(titleid);baseid=baseid.lower()	
	iconUrl=False
	rglist=['America','Europe','Japan','Asia']
	regions=list()
	titleid=titleid.lower()	
	if str(titleid).endswith('000'):
		baseid=titleid
	elif str(titleid).endswith('800'):	
		baseid=titleid[:-3]+'000'
	else:
		titleid=titleid.lower()
		baseid=get_dlc_baseid(titleid);baseid=baseid.lower()	
	for region in rglist:
		f='nutdb_'+region+'.json'
		regionfile=os.path.join(DATABASE_folder,f)	
		check_region_file(region)
		with open(regionfile) as json_file:	
			data = json.load(json_file)		
			for i in data:
				dict=data[i]
				if 'id' in dict and not region in regions:
					if str(dict['id']).lower()==titleid:
						if 'iconUrl' in dict:
							iconUrl=str(dict['iconUrl'])	
							if iconUrl=='None' or iconUrl=='':
								iconUrl=False	
							else:	
								return iconUrl	
	for region in rglist:
		f='nutdb_'+region+'.json'
		regionfile=os.path.join(DATABASE_folder,f)	
		check_region_file(region)
		with open(regionfile) as json_file:	
			data = json.load(json_file)		
			for i in data:
				dict=data[i]
				if 'id' in dict and not region in regions:
					if str(dict['id']).lower()==baseid:
						if 'iconUrl' in dict:
							iconUrl=str(dict['iconUrl'])	
							if iconUrl=='None' or iconUrl=='':
								iconUrl=False	
							else:	
								return iconUrl						
	return regions	


def get_dlcname(titleid,roman=True,format='tabs'):
	cname=False;basename=False;name=False
	with open(nutdbfile) as json_file:			
		data = json.load(json_file)	
		titleid=titleid.lower()
		baseid=get_dlc_baseid(titleid);baseid=baseid.lower()
		for i in data:
			check=False
			for j,k in data[i].items():
				if str(j) == 'id':
					if str(k).lower()==titleid:
						check=True	
				if str(j) == 'name' and check==True:
					cname=str(k)
					break
		for i in data:
			check=False
			for j,k in data[i].items():
				if str(j) == 'id':
					if str(k).lower()==baseid:
						check=True	
				if str(j) == 'name' and check==True:
					basename=str(k)
					break	
		if basename != False and roman == True:
			converter = kakashi_conv()
			basename=converter.do(basename)	
			if basename[0] == ' ':
				basename=basename[1:]
			basename=basename[0].upper()+basename[1:]
			basename=set_roma_uppercases(basename)		
		else:pass		
		if cname != False and roman == True:
			converter = kakashi_conv()
			cname=converter.do(cname)	
			if cname[0] == ' ':
				basename=basename[1:]			
			cname=cname[0].upper()+cname[1:]
			cname=set_roma_uppercases(cname)
		else:pass						
		if cname==False:
			return False
		else:
			if (cname=='None' and basename=='None') or (cname=='None' and basename==False):
				return False
			if basename==False or basename=='None':	
				name=cname
			elif cname!='None':
				name=basename+' '+'['+cname+']'
			else:
				DLCnumb=str(titleid)
				DLCnumb="0000000000000"+DLCnumb[-3:]									
				DLCnumb=bytes.fromhex(DLCnumb)
				DLCnumb=str(int.from_bytes(DLCnumb, byteorder='big'))									
				DLCnumb=int(DLCnumb)	
				name = basename+' '+'['+str(DLCnumb)+']'
		if format!='tabs':
			name=name.replace("[", "- ")
			name=name.replace("]", "")
		name=name.replace("\n", "")	
	return 	name			
				

def get_dlcData(titleid,roman=True,format='tabs'):
	cname=False;basename=False;name=False;editor=False		
	with open(nutdbfile) as json_file:			
		data = json.load(json_file)		
		titleid=titleid.lower()
		baseid=get_dlc_baseid(titleid);baseid=baseid.lower()
		for i in data:
			dict=data[i]
			if 'id' in dict:
				if str(dict['id']).lower()==titleid:
					if 'name' in dict:
						cname=str(dict['name'])
					break
		for i in data:
			dict=data[i]
			if 'id' in dict:
				if str(dict['id']).lower()==baseid:
					if 'name' in dict:
						basename=str(dict['name'])
					if 'publisher' in dict:
						editor=str(dict['publisher'])
					break					
		if basename != False and roman == True and basename != 'None':
			converter = kakashi_conv()
			basename=converter.do(basename)	
			basename=basename[0].upper()+basename[1:]
			basename=set_roma_uppercases(basename)		
		else:pass	
		if editor != False and roman == True and editor != 'None':
			converter = kakashi_conv()
			editor=converter.do(editor)	
			editor=editor[0].upper()+editor[1:]
			editor=set_roma_uppercases(editor)		
		else:pass			
		if cname != False and roman == True and cname != 'None':
			converter = kakashi_conv()
			cname=converter.do(cname)	
			cname=cname[0].upper()+cname[1:]
			cname=set_roma_uppercases(cname)
		else:pass						
		if cname==False:
			return False,False
		else:
			if (cname=='None' and basename=='None') or (cname=='None' and basename==False):
				return False,False
			if basename==False or basename=='None':	
				name=cname
			elif cname!='None':
				name=basename+' '+'['+cname+']'
			else:
				DLCnumb=str(titleid)
				DLCnumb="0000000000000"+DLCnumb[-3:]									
				DLCnumb=bytes.fromhex(DLCnumb)
				DLCnumb=str(int.from_bytes(DLCnumb, byteorder='big'))									
				DLCnumb=int(DLCnumb)	
				name = basename+' '+'['+str(DLCnumb)+']'
		if editor=='None':
			editor=False
		if format!='tabs':
			name=name.replace("[", "- ")
			name=name.replace("]", "")	
		name=name.replace("\n", "")				
	return 	name,editor	
	
def get_content_langue(titleid):	
	langue=False
	rglist=['America','Europe','Japan','Asia']
	titleid=titleid.lower()	
	if str(titleid).endswith('000'):
		baseid=titleid
	elif str(titleid).endswith('800'):	
		baseid=titleid[:-3]+'000'
	else:
		titleid=titleid.lower()
		baseid=get_dlc_baseid(titleid);baseid=baseid.lower()	
	for region in rglist:
		f='nutdb_'+region+'.json'
		regionfile=os.path.join(DATABASE_folder,f)	
		check_region_file(region)
		with open(regionfile) as json_file:	
			data = json.load(json_file)		
			for i in data:
				dict=data[i]
				if 'id' in dict:
					if str(dict['id']).lower()==baseid:
						if 'languages' in dict:
							langue=str(dict['languages'])
							if langue=='None':
								langue=False
						break
		if langue != False:
			try:
				langue=convertlangue(langue,region)
			except BaseException as e:
				Print.error('Exception: ' + str(e))	
				pass	
			break
	return langue
	
def get_list_match(token,roma=True,show=False,Print=False):	
	token=token.lower()
	tokenlist=list();
	include_tk=list();exclude_tk=list();filter_tk=list()
	include_val=list();exclude_val=list();filter_val=list()
	langue='';match=''
	if '{' in token or '}' in token:
		var_=token[1:-1]
		tokenlist=var_.split(".")
		for v in tokenlist:
			if v[0]=='+':
				par=v[1:]
				p_=par.split(":")
				include_tk.append(p_[0])
				include_val.append(p_[1])				
			elif v[0]=='-':
				par=v[1:]
				p_=par.split(":")
				exclude_tk.append(p_[0])
				exclude_val.append(p_[1])					
			elif v[0]=='*':
				par=v[1:]
				p_=par.split(":")
				filter_tk.append(p_[0])
				filter_val.append(p_[1])	
			else:			
				par=v
				p_=par.split(":")
				include_tk.append(p_[0])
				include_val.append(p_[1])			
	# print(include_tk)			
	# print(include_val)
	# print(exclude_tk)			
	# print(exclude_val)
	# print(filter_tk)			
	# print(filter_val)	
	# print(roma)
	# print(show)
	# print(Print)	

	matchdict={};
	rglist=['America','Europe','Japan','Asia']
	for region in rglist:
		f='nutdb_'+region+'.json'
		regionfile=os.path.join(DATABASE_folder,f)	
		check_region_file(region)
		titleid=False;basename=False;version=0
		with open(regionfile) as json_file:	
			data = json.load(json_file)		
			for i in data:
				dict=data[i]
				if 'id' in dict:
					titleid=str(dict['id']).upper()
					if titleid=='NONE':
						break		
					else:	
						baseid=get_baseid(titleid)
				if titleid !=baseid:
					basename=get_dlcname(titleid,roman=rome)	
				if 'version' in dict:
					version=str(dict['version'])
					if version=='None':
						version=0
				if 'name' in dict:
					contentname=str(dict['name'])
					if contentname=='None':				
						contentname=''
					if (contentname != '' or contentname != None) and roma == True:
						converter = kakashi_conv()
						contentname=converter.do(contentname)
						contentname=contentname[0].upper()+contentname[1:]
				if 'languages' in dict:
					langue=dict['languages']
					langue=ast.literal_eval(str(langue))
					if isinstance(langue, list):
						langue=','.join(langue)		
				ismatch=False						
				for j,k in data[i].items():
					for i in range(len(include_tk)):
						token=include_tk[i];value=include_val[i]
						if j.lower()==token:
							entry=ast.literal_eval(str(k))
							if isinstance(entry, list):
								for val in entry:
									if str(val).lower()==value:
										ismatch=True
										match=','.join(entry)											
							else:
								entry=str(entry).lower()
								if value in entry:
									ismatch=True
									match=entry
					if ismatch==True:
						for i in range(len(exclude_tk)):					
							token=exclude_tk[i];value=exclude_val[i]		
							if j.lower()==token:
								entry=ast.literal_eval(str(k))
								if isinstance(entry, list):
									for val in entry:
										if str(val).lower()==value:
											ismatch=False	
					if ismatch==True:
						for i in range(len(filter_tk)):					
							token=filter_tk[i];value=filter_val[i]		
							if j.lower()==token:
								entry=ast.literal_eval(str(k))
								if isinstance(entry, list):
									for val in entry:
										if str(val).lower()!=value:
											ismatch=False	
											
				if 	not titleid in matchdict.keys() and titleid != False and ismatch==True:
					if basename==False:
						cname= "{} ({})[{}][v{}].nsp".format(contentname,langue,titleid,version)
					else:
						cname= "{} [{}]({})[{}][v{}].nsp".format(contentname,basename,langue,titleid,version)					
					matchdict[titleid]=cname

	if show==True:
		showlist=list()
		for key in matchdict.keys():
			entry=matchdict[key]
			showlist.append(entry)
		showlist.sort()	
		for entry in showlist:	
			print(entry)
	if Print!=False:
		try:
			dir=os.path.dirname(os.path.abspath(Print))
			if not os.path.exists(dir):
				os.makedirs(dir)	
			printlist=list()
			for key in matchdict.keys():
				entry=matchdict[key]
				printlist.append(entry)
			printlist.sort()	
			with open(Print,"a", encoding='utf8') as tfile: 
				for entry in printlist:	
					tfile.write(entry+'\n')	
		except BaseException as e:
			Print.error('Exception: ' + str(e))	
			pass				
	return 	matchdict
	
def get_baseid(titleid):
	if str(titleid).endswith('000'):
		baseid=titleid
	elif str(titleid).endswith('800'):	
		baseid=titleid[:-3]+'000'
	else:
		titleid=titleid.lower()
		baseid=get_dlc_baseid(titleid)
	return baseid.upper()	
		
def get_content_data(titleid,trans=True):	
	releaseDate=False;nsuId=False;category=False;ratingContent=False;
	numberOfPlayers=False;iconUrl=False;screenshots=False;bannerUrl=False
	intro=False;description=False;rating=False
	rglist=['America','Europe','Japan','Asia']
	titleid=titleid.lower()	
	if str(titleid).endswith('000'):
		baseid=titleid
	elif str(titleid).endswith('800'):	
		baseid=titleid[:-3]+'000'
	else:
		titleid=titleid.lower()
		baseid=get_dlc_baseid(titleid);baseid=baseid.lower()	
	for region in rglist:
		f='nutdb_'+region+'.json'
		regionfile=os.path.join(DATABASE_folder,f)	
		check_region_file(region)
		with open(regionfile) as json_file:	
			data = json.load(json_file)		
			for i in data:
				dict=data[i]
				if 'id' in dict:
					if str(dict['id']).lower()==baseid:
						if 'releaseDate' in dict:
							releaseDate=str(dict['releaseDate'])
							if releaseDate=='None':
								releaseDate=False
							else:
								b=releaseDate
								releaseDate=b[6:]+'/'+b[4:6]+'/'+b[:4]
						if 'nsuId' in dict:
							nsuId=str(dict['nsuId'])
							if nsuId=='None' or nsuId=='':
								nsuId=False
						if 'category' in dict:
							category=str(dict['category'])
							try:	
								x = [x.strip() for x in eval(category)]							
								category=x
							except:pass	
							if category=='None' or str((', '.join(category)))=='':
								category=False		
							elif region=='Japan' or region=='Asia':
								converter = kakashi_conv()
								romalist=list()
								for item in category:										
									item=converter.do(item)	
									item=item[0].upper()+item[1:]
									romalist.append(item)
								category=romalist	
						if 'ratingContent' in dict:
							ratingContent=str(dict['ratingContent'])							
							try:									
								x = [x.strip() for x in eval(ratingContent)]							
								ratingContent=x
							except:pass	
							if ratingContent=='None' or str((', '.join(ratingContent)))=='':
								ratingContent=False	
							elif region=='Japan' or region=='Asia':
								converter = kakashi_conv()
								romalist=list()
								for item in ratingContent:										
									item=converter.do(item)	
									item=item[0].upper()+item[1:]
									romalist.append(item)
								ratingContent=romalist									
						if 'numberOfPlayers' in dict:
							numberOfPlayers=str(dict['numberOfPlayers'])
							if numberOfPlayers=='None' or numberOfPlayers=='':
								numberOfPlayers=False	
						if 'rating' in dict:
							rating=str(dict['rating'])
							if rating=='None' or rating=='':
								rating=False									
						if 'iconUrl' in dict:
							iconUrl=str(dict['iconUrl'])	
							if iconUrl=='None' or iconUrl=='':
								iconUrl=False									
						if 'screenshots' in dict:
							screenshots=str(dict['screenshots'])	
							if screenshots=='None' or screenshots=='':
								screenshots=False								
						if 'bannerUrl' in dict:
							bannerUrl=str(dict['bannerUrl'])
							if bannerUrl=='None' or bannerUrl=='':
								bannerUrl=False								
						if 'intro' in dict:
							intro=str(dict['intro'])
							if intro=='None' or intro=='':
								intro=False			
							elif region=='Japan' or region=='Asia':			
								if trans==False:
									intro=False	
								else:
									try:
										# converter = kakashi_conv()							
										# intro=converter.do(intro)	
										# intro=intro[0].upper()+intro[1:]												
										translator = Translator()
										if region=='Asia':
											translation=translator.translate(intro,dest='en')	
										if region=='Japan':
											translation=translator.translate(intro,src='ja',dest='en')	
										intro=translation.text								
									except: pass																		
						if 'description' in dict:
							description=str(dict['description'])	
							if description=='None' or description=='':
								description=False		
							elif region=='Japan' or region=='Asia':		
								if trans==False:
									description=False	
								else:
									try:
										# converter = kakashi_conv()						
										# description=converter.do(description)	
										# description=description[0].upper()+description[1:]												
										translator = Translator()
										if region=='Asia':
											translation=translator.translate(description,dest='en')	
										if region=='Japan':
											translation=translator.translate(description,src='ja',dest='en')												
										description=translation.text								
									except: pass														
						break
		if nsuId != False or releaseDate != False or category != False:
			break
		if 	nsuId == False and releaseDate == False and category == False:
			region=False
	return nsuId,releaseDate,category,ratingContent,numberOfPlayers,intro,description,iconUrl,screenshots,bannerUrl,region,rating
			
def get_dlcnsuId(titleid):
	nsuId=False
	rglist=['America','Europe','Japan','Asia']
	titleid=titleid.lower()	
	for region in rglist:	
		f='nutdb_'+region+'.json'
		regionfile=os.path.join(DATABASE_folder,f)	
		check_region_file(region)
		with open(regionfile) as json_file:	
			data = json.load(json_file)		
			for i in data:
				dict=data[i]
				if 'id' in dict:
					if str(dict['id']).lower()==titleid:
						if 'releaseDate' in dict:
							releaseDate=str(dict['releaseDate'])
						if 'nsuId' in dict:
							nsuId=str(dict['nsuId'])
							if nsuId=='None':
								nsuId=False	
						break
		if nsuId != False:
			break						
	return 	nsuId

def convertlangue(langue,region):
	SupLg=list()
	x = [x.strip() for x in eval(langue)]
	langue=x
	for i in langue:
		if i=='en' and region=='America':
			SupLg.append("US (eng)")
		if i=='en' and region=='Europe':
			SupLg.append("UK (eng)")				
		if i=='ja':
			SupLg.append("JP")				
		if i=='fr':
			SupLg.append("FR")				
		if i=='de':
			SupLg.append("DE")						
		if i=='es':
			SupLg.append("SPA")				
		if i=='it':
			SupLg.append("IT")						
		if i=='nl':
			SupLg.append("DU")									
		if i=='pt':
			SupLg.append("POR")						
		if i=='ru':
			SupLg.append("RU")						
		if i=='ko':
			SupLg.append("KOR")				
		if i=='zh':
			SupLg.append("CH")	
	return SupLg


def get_dlc_baseid(titleid):
	baseid=str(titleid)
	token=int(hx(bytes.fromhex('0'+baseid[-4:-3])),16)-int('1',16)
	token=str(hex(token))[-1]
	token=token.upper()
	baseid=baseid[:-4]+token+'000'	
	return baseid


def get_content_cheats(titleid,version=False,buildId=False):	
	cheatID_list=list();
	titleid=titleid.lower()	
	if str(titleid).endswith('000'):
		baseid=titleid
	elif str(titleid).endswith('800'):	
		baseid=titleid[:-3]+'000'
	else:
		titleid=titleid.lower()
		baseid=get_dlc_baseid(titleid);baseid=baseid.lower()	
	f='nutdb_'+'cheats'+'.json'
	_dbfile_=os.path.join(DATABASE_folder,f)	
	check_other_file(urlconfig,'cheats')
	with open(_dbfile_) as json_file:	
		data = json.load(json_file)		
		for i in data:
			if i.lower()==baseid.lower():
				dict=data[i]
				for j in dict:
					jsonbID=j
					datalv2=dict[j]
					if 'version' in datalv2:
						titleid=str(i).upper()
						version=str(datalv2['version'])
						BuildID=str(j).upper()
						# print (titleid+' v'+version)
						# print('BuildID: '+str(j))
						cheats=list()
						for k in datalv2:
							if k!='version':
								datalv3=datalv2[k]
								if 'title' in datalv3:
									cheat_title=datalv3['title']
									# print("Title: "+datalv3['title'])
								if 'source' in datalv3:
									cheat_source=datalv3['source']
									# print(datalv3['source'])	
									if not 'title' in datalv3:
										cheat_title=''
									cheats.append([cheat_title,cheat_source])
						cheatID_list.append([titleid,version,BuildID,cheats])			
				break
	return cheatID_list
	
def BaseID_tree(titleid,printinfo=True):	
	feed=''
	titleid=titleid.lower()	
	if str(titleid).endswith('000'):
		baseid=titleid
	elif str(titleid).endswith('800'):	
		baseid=titleid[:-3]+'000'
	else:
		titleid=titleid.lower()
		baseid=get_dlc_baseid(titleid);baseid=baseid.lower()		
	f='nutdb_'+'versions'+'.txt'
	_dbfile_=os.path.join(DATABASE_folder,f)	
	check_other_file(urlconfig,'versions_txt')
	baselist=list();updlist=list();dlclist=list()
	with open(_dbfile_,'rt',encoding='utf8') as csvfile:
		readCSV = csv.reader(csvfile, delimiter='|')	
		i=0	
		for row in readCSV:
			if i==0:
				csvheader=row
				i=1
				if 'id' and 'version' in csvheader:
					id=csvheader.index('id')
					ver=csvheader.index('version')	
				else:break	
			else:	
				tid=str(row[id]).lower() 
				if str(tid).endswith('000'):
					bid=tid
				elif str(tid).endswith('800'):	
					bid=tid[:-3]+'000'
				else:
					tid=tid.lower()
					bid=get_dlc_baseid(tid);bid=bid.lower()				
				if baseid==bid:
					v_=str(row[ver])
					if v_=='':
						v_='0'
					if tid.endswith('000'):
						baselist.append([tid,v_])
						if printinfo==True:
							message=('Base:   '+tid.upper()+' v'+str(v_));print(message);feed+=message+'\n'
					elif tid.endswith('800'):
						updlist.append([tid,v_])
						if printinfo==True:
							message=('Update: '+tid.upper()+' v'+str(v_));print(message);feed+=message+'\n'		
					else:
						dlclist.append([tid,v_])
						if printinfo==True:
							message=('DLC:    '+tid.upper()+' v'+str(v_));print(message);feed+=message+'\n'
				else:pass
	return feed,baselist,updlist,dlclist			

def latest_upd(titleid):	
	titleid=titleid.lower()	
	if str(titleid).endswith('000'):
		baseid=titleid[:-3]+'000'
	elif str(titleid).endswith('800'):	
		baseid=titleid[:-3]+'000'
	else:
		titleid=titleid.lower()
		baseid=get_dlc_baseid(titleid);baseid=baseid.lower()
	updid=baseid[:-3]+'800'
	f='nutdb_'+'versions'+'.txt'
	_dbfile_=os.path.join(DATABASE_folder,f)	
	check_other_file(urlconfig,'versions_txt')
	feed=list()
	with open(_dbfile_,'rt',encoding='utf8') as csvfile:
		readCSV = csv.reader(csvfile, delimiter='|')	
		i=0	
		for row in readCSV:
			if i==0:
				csvheader=row
				i=1
				if 'id' and 'version' in csvheader:
					id=csvheader.index('id')
					ver=csvheader.index('version')	
				else:break	
			else:	
				tid=str(row[id]).lower() 		
				if updid==tid:
					v_=str(row[ver])				
					return ('v'+str(v_))

def latest_ver(titleid):	
	titleid=titleid.lower()	
	f='nutdb_'+'versions'+'.txt'
	_dbfile_=os.path.join(DATABASE_folder,f)	
	check_other_file(urlconfig,'versions_txt')
	feed=list()
	with open(_dbfile_,'rt',encoding='utf8') as csvfile:
		readCSV = csv.reader(csvfile, delimiter='|')	
		i=0	
		for row in readCSV:
			if i==0:
				csvheader=row
				i=1
				if 'id' and 'version' in csvheader:
					id=csvheader.index('id')
					ver=csvheader.index('version')	
				else:break	
			else:	
				tid=str(row[id]).lower() 		
				if titleid==tid:
					v_=str(row[ver])				
					return ('v'+str(v_))					

def set_roma_uppercases(input):
	if '(' in str(input):
		input = input.replace("( ", "(");input = input.replace(" )", ")")	
		tid1=list()
		tid2=list()
		tid1=[pos for pos, char in enumerate(input) if char == '(']
		tid2=[pos for pos, char in enumerate(input) if char == ')']
		if len(tid1)>=len(tid2):
			lentlist=len(tid1)					
		elif len(tid1)<len(tid2):
			lentlist=len(tid2)				
		for i in range(lentlist):	
			try:
				i1=tid1[i]
				i2=tid2[i]+1					
				t=input[i1:i2]
				t=t[0]+t[1].upper()+t[2:]
				input=input[:i1]+t+input[i2:]
			except:pass		
	elif '[' in str(input):
		input = input.replace("[", "(");input = input.replace("]", ")")
		tid1=list()
		tid2=list()
		tid1=[pos for pos, char in enumerate(input) if char == '(']
		tid2=[pos for pos, char in enumerate(input) if char == ')']
		if len(tid1)>=len(tid2):
			lentlist=len(tid1)					
		elif len(tid1)<len(tid2):
			lentlist=len(tid2)				
		for i in range(lentlist):	
			try:
				i1=tid1[i]
				i2=tid2[i]+1					
				t=input[i1:i2]
				t=t[0]+t[1].upper()+t[2:]
				input=input[:i1]+t+input[i2:]
			except:pass		
	else:
		pass
	return 	input

def kakashi_conv():
	kakasi = pykakasi.kakasi()
	kakasi.setMode("H", "a")
	kakasi.setMode("K", "a")
	kakasi.setMode("J", "a")
	kakasi.setMode("s", True)
	kakasi.setMode("E", "a")
	kakasi.setMode("a", None)
	kakasi.setMode("C", False)
	converter = kakasi.getConverter()	
	return converter
		
		