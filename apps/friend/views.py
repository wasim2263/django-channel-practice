from django.shortcuts import render

# Create your views here.
from django.views import View


class FriendListView(View):
    def get(self, request):
        context = {}
        return render(request, 'friend/friend-list.html', context)
