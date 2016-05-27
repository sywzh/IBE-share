
from django.utils import simplejson
import json
from netPan.decorators import lrender
from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.shortcuts import render_to_response


#@lrender('test.html')
@csrf_exempt
def multiply(request):
	print request.method
	print request.is_ajax()
	#t = get_template('test.html')
	content_type = 'application/json;charset=utf-8'
	a = request.POST.get("a")
	b = request.POST.get("b")
	print a,b
	return render_to_response('test.html')
	#return HttpResponse(json.dumps({'message':'haha'}),mimetype='application/javascript')
	#return {json.dumps({'message':'haha'})}
	#response.write('success')
	#return response

