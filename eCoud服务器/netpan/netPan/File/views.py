#!/usr/bin/env python
#-*-coding:utf8-*-

import os
from netPan.settings import mongoDB,opIBE
from django.utils import simplejson 
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from netPan.decorators import lrender
from django.views.decorators.csrf import csrf_exempt
from netPan.mongo import *
from models import *
from netPan.File.unoconv import output
from netPan.filetype import fileType
from netPan.Log import doc_log,shareLog,trashLog
from netPan.User.models import UserProfile
import gc
import bson
from django.core import serializers
import base64
from aes import mycrypt

def gcFile(buf):
	del buf
	gc.collect()

def profileUpload(file):
	if file:
		buf = ''
		for content in file.chunks():
			buf = buf + content
		return True,buf
	return False,buf

def encryptFile(buf,email):
	ret,getkey,getsecret = opIBE.ibeEncode(email)
	aeskey = getkey + '!@#$'
	op = mycrypt(aeskey)
	secretbuf = op.myencrypt(buf)
	return ret,getsecret,secretbuf

def getAESkey(user,id):
	try:
		op = User.objects.get(username = user)
		email = op.email
		ibe = IBEMaster.objects.get(id = 1)
		master = ibe.master
		secret = FileTable.objects.get(id = id)
		getsecret = secret.key
		ibekey = opIBE.ibeDecode(master,getsecret,email)
		aeskey = ibekey + '!@#$'
		return True,aeskey
	except:
		return False,''

def decryptFile(id,buf,user):
	try:
		ret,aeskey = getAESkey(user,id)
		if not ret:
			return False,''
		opt = mycrypt(aeskey)
		plainbuf = opt.mydecrypt(buf).rstrip()
		return True,plainbuf
	except:
		return False,''

def storageFile(filename,user,fileurl,buf,doc_size,is_edit,is_browser,typefile):
	ret,getsecret,buf = encryptFile(buf,user.email)
	if not ret:
		return False
	try:
		capacity = lastCapacity(user,doc_size)
		capacity = int(capacity)
		if capacity < 0:
			return HttpResponse(simplejson.dumps({'message':'A'}))
		path = user.username + fileurl + filename
		print path
		print mongoDB.setCollection(user.username)
		id = mongoDB.creatFile(path,buf)
		print id
		storage = FileTable(file_id = id,user_id = user.id,path = fileurl,name = filename,key = getsecret,is_edit = is_edit,is_browser = is_browser,typefile = typefile)
		storage.save()
		doc_log(fileurl,filename,'A',user.id)
		gcFile(buf)
		return True
	except:
		gcFile(buf)
		return False
def storageDocument(filename,user,fileurl,buf,key):
	try:
		mongoDB.setCollection(user)
		id = mongoDB.creatFile(fileurl,buf)
		storage = FileTable(file_id = id,path = fileurl,name = filename,key = key,is_edit = is_edit)
		storage.save()
		gcFile(buf)
		return True
	except:
		return False

def lastCapacity(user,doc_size):
	profile = UserProfile.objects.get(user__username = user)
	capacity = profile.capacity-int(doc_size)
	profile.capacity = capacity
	profile.save()
	return capacity

def convert(pid,user):
	try:
		pdf = FileTable.objects.get(id = pid,user__username = user)
	except FileTable.DoesNotExist:
		return '5',''
	path,buf,name = getFile(user,pid)
	ret,plainbuf = decryptFile(pid,buf,user)
	fileWrite(name,plainbuf)
	ret = output(name)
	if ret != 0:
		ret = output(name)
	pdfname = name.split('.')[0] + '.pdf'
	pdfbuf = fileRead(pdfname)
	ok,aeskey = getAESkey(user,pid)
	if not ok:
		return '5',''
	opt = mycrypt(aeskey)
	encbuf = opt.myencrypt(pdfbuf)
	return ret,encbuf

@login_required
@csrf_exempt
def convertFile(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	pid = request.POST.get("id")
	user = request.user.username
	ret = convert(pid,user)
	return HttpResponse(simplejson.dumps({'message':ret}))

@lrender('File/home.html')
@login_required
@csrf_exempt
def uploadifyScript(request):
	user = request.user
	if request.method == 'POST':
		file_url = request.POST.get("fileUrl")
		file_size = request.POST.get("fileSize")
		file = request.FILES.get("Filedata",None)
		result,buf = profileUpload(file)
		print result
		if not result:
			return HttpResponse(simplejson.dumps({'message':'B'}))
		file_type = fileType(buf)
		if isStorage(file.name,user,file_url,buf,file_size,file_type):
			return HttpResponse(simplejson.dumps({'message':'E'}))
		else:
			return HttpResponse(simplejson.dumps({'message':'B'}))
	return {}

def isStorage(name,user,path,buf,size,file_type):
	if isTxt(name):
		if storageFile(name,user,path,buf,size,'1','1','2'):
			return True
		else:
			return False
	elif isPdf(file_type):
		if storageFile(name,user,path,buf,size,'0','1','1'):
			return True
		else:
			return False
	elif isDocument(file_type):
		if storageFile(name,user,path,buf,size,'0','1','0'):
			return True
		else:
			return False
	elif isPicture(file_type):
		if storageFile(name,user,path,buf,size,'0','1','3'):
			return True
		else:
			return False
	else:
		if storageFile(name,user,path,buf,size,'0','0','4'):
			return True
		else:
			return False
	return False
def isPdf(file_type):
	if file_type == "pdf":
		return True
	else:
		return False

def isToPdf(file_name):
	if(output(file_name) == 0):
		return True
	else:
		return False

def isTxt(file_name):
	if file_name[-3:] == 'txt':
		return True
	else:
		return False

def isDocument(file_type):
	if file_type in ['xls.or.doc','docx.or.pptx','ppt']:
		return True
	else:
		return False

def isPicture(file_type):
	if file_type in ['jpg','png','gif','bmp']:
		return True
	else:
		return False

def fileWrite(file_name,buf):
	fp = open(file_name,'wb+')
	fp.write(buf)
	fp.close()

def fileRead(file_name):
	fp = open(file_name,'rb')
	buf = fp.read()
	fp.close()
	os.remove(file_name)
	return buf

def getFile(user,sid):
	try:
		get = FileTable.objects.get(id = sid,user__username = user)
	except FileTable.DoesNotExist:
		raise Http404
	id = bson.objectid.ObjectId(get.file_id)
	mongoDB.setCollection(user)
	path = user + get.path + get.name
	buf = mongoDB.getFileData(path,id)
	return get.path,buf,get.name

@csrf_exempt
@login_required
def downLoad(request,sid):
	user = request.user.username
	path,buf,filename = getFile(user,sid)
	filename = filename.encode('utf8')
	if buf == 'error':
		pass
	else:
		ret,buf = decryptFile(sid,buf,user)
		if ret:
			doc_log(path,filename,'G',request.user.id)
		response = HttpResponse(buf,mimetype = 'application/octet-stream')
		response['Content-Disposition'] = 'attachment;filename=%s' % filename
		return response

def funcDel(array,user):
	for i in range(len(array)):
		try:
			op = FileTable.objects.get(user__username = user.username,id = array[i])
			op.is_delete = '1'
			doc_log(op.path,op.name,'C',user.id)
			op.save()
		except:
			return False
	return True

@csrf_exempt
@login_required
def delFile(request):
	if request.method != 'POST' or not request.is_ajax():
		raise Http404
	data = request.POST.get("ids")
	req = simplejson.loads(data)
	user = request.user
	if funcDel(req,user):
		return HttpResponse(simplejson.dumps({'message':'F'}))
	else:
		return HttpResponse(simplejson.dumps({'message':'G'}))

def funcResume(user,array):
	uid = user.id
	for i in range(len(array)):
		try:
			op = FileTable.objects.get(user__username = user,id = array[i])
			op.is_delete = '0'
			op.save()
			trashLog(uid,op.name,'R')
		except:
			return False
	return True

@csrf_exempt
@login_required
def resumeFile(request):
	if request.method != 'POST' or not request.is_ajax():
		raise Http404
	data = request.POST.get("id")
	req = simplejson.loads(data)
	user = request.user
	if funcResume(user,req):
		return HttpResponse(simplejson.dumps({'message':'H'}))
	else:
		return HttpResponse(simplejson.dumps({'message':'I'}))

def delMongo(user,id):
	try:
		mongoDB.setCollection(user)
		op = FileTable.objects.get(user__username = user,id = id)
		path = user + op.path + op.name
		if op.is_folder == '1':
			result = mongoDB.deleteDir(path)
			if result == 'error':
				return False
		else:
			result = mongoDB.deleteFile(path,op.file_id)
			if result == 'error':
				return False
		return True
	except:
		return False

def funcReDel(user,array):
	uid = user.id
	for i in range(len(array)):
		if not delMongo(user.username,array[i]):
			return False
		try:
			op = FileTable.objects.filter(user__username = user,id = array[i])
			trashLog(uid,op[0].name,'D')
			op.delete()
		except:
			return False
	return True

@csrf_exempt
@login_required
def reDelFile(request):
	if request.method != 'POST' or not request.is_ajax():
		return Http404
	data = request.POST.get("id")
	req = simplejson.loads(data)
	user = request.user
	if funcReDel(user,req):
		return HttpResponse(simplejson.dumps({'message':'J'}))
	else:
		return HttpResponse(simplejson.dumps({'message':'K'}))

@lrender("File/preview.html")
@login_required
def browserFile(request,id):
	return {'mark':id}

def getType(sid):
	op = FileTable.objects.get(id = sid)
	typefile = op.typefile
	return typefile

def modifyType(sid,user):
	try:
		op = FileTable.objects.get(id = sid)
		op.typefile = '5'
		op.save()
		ret,buf = convert(sid,user)
		if ret != 0:
			return False
		mongoDB.setCollection(user)
		path = user + '$' + str(op.id)
		id = mongoDB.creatFile(path,buf)
		try:
			con = ConvertTable.objects.get(file__id = sid)
			con.fid = id
			con.save()
		except ConvertTable.DoesNotExist:
			storage = ConvertTable(file_id = sid,fid = id)
			storage.save()
		return True
	except:
		return False

def getPdfFile(sid,user):
	try:
		op = ConvertTable.objects.get(file__id = sid)
		fid = op.fid
		id = bson.objectid.ObjectId(fid)
		mongoDB.setCollection(user)
		path = user + '$' + sid
		buf = mongoDB.getFileData(path,id)
		ret,plainbuf = decryptFile(sid,buf,user)
		if not ret:
			return False,''
		return True,plainbuf
	except:
		return False,''

def getConvertFile(sid,user):
	if getType(sid) == "0":
		if not modifyType(sid,user):
			return False,''
		ret,buf = getPdfFile(sid,user)
		if ret:
			return True,buf
		else:
			return False,''
	elif getType(sid) == "5":
		ret,buf = getPdfFile(sid,user)
		if ret:
			return True,buf
		else:
			return False,''
	elif getType(sid) == "1":
		path,buf,filename = getFile(user,sid)
		ret,buf = decryptFile(sid,buf,user)
		if ret:
			return True,buf
		else:
			return False,''

@login_required
@csrf_exempt
def browserFuf(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	sid = request.POST.get("id")
	user = request.user.username
	ret,buf = getConvertFile(sid,user)
	if not ret:
		return HttpResponse(simplejson.dumps({'message':''}))
	buf = str(buf)
	if buf == 'error':
		pass
	else:
		base_buf = base64.encodestring(buf)
		response = HttpResponse('data:application/pdf;base64,'+base_buf,mimetype = 'application/pdf')
		#response['Content-Disposition'] = 'attachment;filename=%s' % filename
		return response

@lrender('File/share.html')
@login_required
def shareFile(request):
	return {}

@lrender('File/delete.html')
@login_required
def deleteFile(request):
	try:
		files = FileTable.objects.filter(user__username = request.user,is_delete = '1')
	except FileTable.DoesNotExist:	
		raise Http404
	return {'files':files}

@lrender('File/search.html')
@login_required
def searchFile(request):
	return {}

@login_required
@csrf_exempt
def Search(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	name = request.POST.get("name")
	try:
		files = ShareTable.objects.filter(name__icontains = name)
		search_files = serializers.serialize("json",files)
		return HttpResponse(simplejson.dumps({'search_files':search_files}))
	except:
		return HttpResponse(simplejson.dumps({'search_files':'X'}))
	

@lrender('File/Coordination.html')
@login_required
def coordinationFile(request):
	return {}

@lrender('File/CoordinationTo.html')
@login_required
def coordinationToFile(request):
	return {}

@lrender('File/shareIn.html')
@login_required
def shareInFile(request):
	try:
		files = ShareMeTable.objects.filter(user__username = request.user)
		return {'files':files}
	except:
		raise Http404

@lrender('File/shareOut.html')
@login_required
def shareOutFile(request):
	try:
		files = MyShareTable.objects.filter(user__username = request.user)
		return {'files':files}
	except:
		raise Http404

@csrf_exempt
@login_required
def viewFile(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	all_files = FileTable.objects.filter(user__username = request.user,is_delete = '1')
	all_files = serializers.serialize("json",all_files)
	return HttpResponse(simplejson.dumps({'all_files':all_files}))

@csrf_exempt
@login_required
def myFile(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	path = request.POST.get("path")
	myfiles = FileTable.objects.filter(user__username = request.user,path = path,is_delete = '0')
	myfiles = serializers.serialize("json",myfiles)
	return HttpResponse(simplejson.dumps({'myfiles':myfiles}))

def getUser(email):
	try:
		user = User.objects.get(email = email)
		return True,user
	except User.DoesNotExist:
		return False,user

def myShare(fileid,userid,username,edit,down):
	try:
		storage = MyShareTable(file_id = fileid,user_id = userid,share_who = username,is_edit = edit,is_download = down)
		storage.save()
		op = FileTable.objects.get(id = fileid)
		shareLog(userid,username,op.name,'M')
		return True
	except:
		return False

def shareOther(fileid,userid,user,edit,down):
	try:
		storage = ShareMeTable(file_id = fileid,user_id = userid,who_share = user,is_edit = edit,is_download = down)
		storage.save()
		op = FileTable.objects.get(id = fileid)
		shareLog(userid,user,op.name,'N')
		return True
	except:
		return False

def paramStatus(param):
	if param == '0':
		edit,down = '0','0'
	if param == '1':
		edit,down = '1','0'
	if param == '2':
		edit,down = '0','1'
	return edit,down

def getKey(user,id):
	try:
		op = FileTable.objects.get(user__username = user,id = id)
		key = op.key
		return True,key
	except FileTable.DoesNotExist:
		return False,''

def batchShare(ids,emails,params,user):
	for i in range(len(ids)):
		result,shareuser = getUser(emails[0])
		if result:
			edit,down = paramStatus(params[0])
			if myShare(ids[i],user.id,shareuser.username,edit,down) and shareOther(ids[i],shareuser.id,user.username,edit,down):
				pass
			else:
				return False
		else:
			return False
	return True

@csrf_exempt
@login_required
def Share(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	datas = request.POST.get("shareData")
	data = simplejson.loads(datas)
	ids = data['fileNameIdArray']
	emails = data['EmailAdd']
	params = data['selectNumber']
	user = request.user
	if batchShare(ids,emails,params,user):
		return HttpResponse(simplejson.dumps({'message':'M'}))
	else:
		return HttpResponse(simplejson.dumps({'message':'N'}))

def changeShareOStorage(id,edit,down):
	try:
		s = ShareMeTable.objects.get(id = id)
		s.is_edit = edit
		s.is_download = down
		s.save()
		return True
	except:
		return False

def changeMyShareStorage(id,edit,down):
	try:
		s = MyShareTable.objects.get(id = id)
		s.is_edit = edit
		s.is_download = down
		s.save()
		return True
	except:
		return False

def changeShareOther(id,edit,down):
	if changeMyShareStorage(id,edit,down) and changeShareOStorage(id,edit,down):
		return True
	else:
		return False

def changeStatus(data):
	if data[0] == '0':
		edit,down = '1','0'
	if data[0] == '1':
		edit,down = '0','1'
	return edit,down

def modifyMyShare(id):
	op = MyShareTable.objects.get(id = id)
	shareLog(op.file.user.id,op.who_share,op.file.name,'O')

@csrf_exempt
@login_required
def changeShareO(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	id = request.POST.get("id")
	datas = request.POST.get("selectChangeNumber")
	data = simplejson.loads(datas)
	edit,down = changeStatus(data)
	if changeShareOther(id,edit,down):
		modifyMyShare(id)
		return HttpResponse(simplejson.dumps({'message':'T'}))
	else:
		return HttpResponse(simplejson.dumps({'message':'U'}))

def getShareDownId(sid):
	try:
		op = ShareMeTable.objects.get(id = sid)
		fileid = op.file.id
		username = op.file.user.username
		email = op.file.user.email
		shareLog(op.user.id,op.user.username,op.file.name,'P')
		shareLog(op.file.user.id,op.user.username,op.file.name,'P')
		return username,fileid,email
	except:
		return False,False

@csrf_exempt
@login_required
def shareDownload(request,sid):
	username,fileid,email = getShareDownId(sid)
	if username:
		path,buf,filename = getFile(username,fileid)
		filename = filename.encode('utf8')
		if buf == 'error':
			pass
		else:
			ret,buf = decryptFile(fileid,buf,username)
			response = HttpResponse(buf,mimetype = 'application/octet-stream')
			response['Content-Disposition'] = 'attachment;filename=%s' % filename
			return response
	else:
		pass

def delMyShareStorage(sid):
	try:
		op = MyShareTable.objects.filter(id = sid)
		shareLog(op[0].user.id,op[0].share_who,op[0].file.name,'Q')
		op.delete()
		return True
	except:
		return False

def delShareOStorage(sid):
	try:
		op = ShareMeTable.objects.filter(id = sid)
		shareLog(op[0].file.user.id,op[0].user.id,op[0].file.name,'Q')
		op.delete()
		return True
	except:
		return False
@csrf_exempt
@login_required
def cancelShare(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	id = request.POST.get("id")
	if delMyShareStorage(id) and delShareOStorage(id):
		return HttpResponse(simplejson.dumps({'message':'V'}))
	else:
		return HttpResponse(simplejson.dumps({'message':'W'}))

@login_required
def reViewCancelShare(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	try:
		files = MyShareTable.objects.filter(user__username = request.user)
		all_files = serializers.serialize("json",files)
		return HttpResponse(simplejson.dumps({'all_files':all_files}))
	except:
		raise Http404

def storageFolder(user,path,name):
	folder_path = user.username + path + name
	mongoDB.setCollection(user.username)
	result = mongoDB.creatDir(folder_path)
	if result == 'error':
		return False
	try:
		storage = FileTable(user_id = user.id,path = path,name = name,is_folder = '1')
		storage.save()
		doc_log(path,name,'B',user.id)
		return True
	except:
		return False

@login_required
@csrf_exempt
def newFolder(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	path = request.POST.get("filePath")
	name = request.POST.get("fileName")
	user = request.user
	if storageFolder(user,path,name):
		return HttpResponse(simplejson.dumps({'message':'O'}))
	else:
		return HttpResponse(simplejson.dumps({'message':'P'}))

def getFolderPath(id):
	try:
		op = FileTable.objects.get(id = id)
		path = op.path
		return True,path + op.name + '$'
	except:
		return False,''
@login_required
@csrf_exempt
def viewFolder(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	id = request.POST.get("id")
	getok,path = getFolderPath(id)
	if getok:
		try:
			files = FileTable.objects.filter(user__username = request.user,path = path)
			all_files = serializers.serialize("json",files)
			return HttpResponse(simplejson.dumps({'path':path,'all_files':all_files,'message':'Y'}))
		except:
			return HttpResponse(simplejson.dumps({'message':'Z'}))
	else:
		return HttpResponse(simplejson.dumps({'message':'Z'}))

def isShare(sid):
	for i in range(len(sid)):
		try:
			op = ShareTable.objects.get(file_id = sid[i])
			return True,op
		except ShareTable.DoesNotExist:
			return False,''

def storagePubShare(id,down):
	for i in range(len(id)):
		try:
			sharefile = FileTable.objects.get(id = id[i])
			storage = ShareTable(file_id = id[i],is_download = down,name = sharefile.name)
			storage.save()
		except:
			return False
	return True

@csrf_exempt
@login_required
def pubShare(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	data = request.POST.get("shareData")
	req = simplejson.loads(data)
	id = req['fileNameIdArray']
	down = req['selectNumber'][0]
	is_share,op = isShare(id)
	if is_share:
		return HttpResponse(simplejson.dumps({'message':op.file.name}))
	if storagePubShare(id,down):
		return HttpResponse(simplejson.dumps({'message':'R'}))
	else:
		return HttpResponse(simplejson.dumps({'message':'S'}))

@login_required
@lrender('File/PublicShare.html')
def myPubShare(request):
	try:
		files = ShareTable.objects.filter(file__user__username = request.user)
		return {'files':files}
	except:
		raise Http404

def modifyPubShareStorage(id,down):
	try:
		op = ShareTable.objects.get(id = id)
		op.is_download = down
		return True
	except:
		return False

@login_required
@csrf_exempt
def modifyPubShare(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	id = request.POST.get("id")
	down = request.POST.get("down")
	if modifyPubShareStorage(id,down):
		return HttpResponse(simplejson.dumps({'message':'T'}))
	else:
		return HttpResponse(simplejson.dumps({'message':'U'}))

def delPubShareStorage(id):
	try:
		op = ShareTable.objects.filter(id = id)
		op.delete()
		return True
	except:
		return False

@login_required
@csrf_exempt
def cancelPubShare(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	id = request.POST.get("id")
	if delPubShareStorage(id):
		return HttpResponse(simplejson.dumps({'message':'V'}))
	else:
		return HttpResponse(simplejson.dumps({'message':'W'}))

