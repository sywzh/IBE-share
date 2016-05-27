 #!/usr/bin/env python
#-*-coding:utf8-*-

from decorators import lrender
from netPan.User.models import UserProfile,AddressList
from django.contrib.auth.decorators import login_required
from netPan.File.models import *
from django.contrib.sites.models import Site

@login_required
@lrender('File/home.html')
@login_required
def IndexHd(request):
	user = request.user.username
	profile = UserProfile.objects.get(user_id = request.user.id)
	capacity = str(profile.capacity/1024/1024) + 'M'
	site = Site.objects.get_current()
	domain = site.domain
	files = FileTable.objects.filter(user__username = user,path = '$',is_delete = '0')
	if len(files) == 0:
		return {'capacity':capacity,'files':files,'domain':domain,'path':'$','userlist':[]}
	try:
		userlist = AddressList.objects.filter(user__username = user)
	except:
		userlist = None
	return {'capacity':capacity,'files':files,'domain':domain,'path':'$','userlist':userlist}