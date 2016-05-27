# Create your views here.

from django.utils import simplejson 
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from netPan.decorators import lrender
from models import *
from django.core import serializers

@login_required
def fileLog(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	path = request.POST.get('path')
	try:
		logs = DocumentTable.objects.filter(user__username = request.user,path_name = path)
		all_logs = serializers.serialize("json",logs)
		return HttpResponse(simplejson.dumps({'all_logs':all_logs}))
	except:
		return HttpResponse(simplejson.dumps({'message','L'}))

'''
def shareLog(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	try:
		logs = ShareLogTable.objects.filter(user__username = request.user)
		all_logs = serializers.serialize("json",logs)
		return HttpResponse(simplejson.dumps({'all_logs':all_logs}))
	except:
		return HttpResponse(simplejson.dumps({'message':'L'}))
'''

@login_required
@lrender('Log/sharelog.html')
def shareLog(request):
	try:
		logs = ShareLogTable.objects.filter(user__username = request.user)
		return {'logs':logs}
	except:
		raise Http404

@login_required
def trashLog(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	try:
		logs = TrashLogTable.objects.filter(user__username = request.user)
		all_logs = serializers.serialize("json",logs)
		return HttpResponse(simplejson.dumps({'all_logs':all_logs}))
	except:
		return HttpResponse(simplejson.dumps({'message':'L'}))