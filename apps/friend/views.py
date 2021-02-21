from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.friend.models import Friend


class FriendListView(LoginRequiredMixin, View):
    def get(self, request):
        friends = Friend.objects.filter(
            Q(user_1__username=request.user.username) | Q(user_2__username=request.user.username)).values(
            'user_1', 'user_2')
        friend_list = []
        for friend in friends:
            friend_list.append(friend['user_1'])
            friend_list.append(friend['user_2'])
        friend_list = set(friend_list)
        users = User.objects.exclude(id__in=friend_list)
        for user in users:
            friend = Friend(user_1=request.user, user_2=user)
            friend.save()
        friend_list.remove(request.user.id)
        print(friend_list, users)

        context = {}
        return render(request, 'friend/friend-list.html', context)
