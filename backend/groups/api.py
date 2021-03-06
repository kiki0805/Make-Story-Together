from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from .models import Group, GroupMember
from .serializers import GroupSerializer, GroupDetailSerializer
from .permissions import GroupPermission
from disciplines.models import Discipline
# Create your views here.

class GroupViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    serializer_class = GroupSerializer
    permission_classes = [GroupPermission, ]

    def get_serializer_class(self):
        if self.action != 'retrieve' or self.request.method == 'post':
            return GroupSerializer
        
        return GroupDetailSerializer

    def get_queryset(self):
        params = self.request.query_params
        if 'order' in params:
            if params['order'] == 'number':
                return Group.objects.annotate(member_count=Count('members')).order_by('-member_count').order_by('-created_at')
        return Group.objects.all().order_by('-created_at')

    @action(detail=False, permission_classes=[IsAuthenticated, ])
    def my(self, request):
        groups = Group.objects.filter(owner__screen_name=request.user.account.screen_name)
        if not groups.exists:
            return Response([], status.HTTP_200_OK)
        serializer = self.get_serializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, permission_classes=[IsAuthenticated, ])
    def joined(self, request):
        groups = Group.objects.filter(members__screen_name__icontains=request.user.account.screen_name)
        if not groups.exists:
            return Response([], status.HTTP_200_OK)
        serializer = self.get_serializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, permission_classes=[IsAuthenticated, ], methods=['POST', ])
    def join(self, request, pk=None):
        group = self.get_object()
        if not group.members.filter(id=self.request.user.account.id).exists():
            GroupMember.objects.create(member=self.request.user.account, group=group)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, permission_classes=[IsAuthenticated, ], methods=['POST', ])
    def quit(self, request, pk=None):
        group = self.get_object()
        if GroupMember.objects.filter(member=self.request.user.account, group=group).exists():
            instance = GroupMember.objects.get(member=self.request.user.account, group=group)
            instance.delete()
        return Response(status=status.HTTP_200_OK)

        
    @action(detail=True, permission_classes=[IsAuthenticated, GroupPermission], methods=['POST', ])
    def remove_members(self, request, pk=None):
        group = self.get_object()
        if 'usernames' not in request.data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        member_usernames = request.data['usernames']
        for username in member_usernames:
            instance = GroupMember.objects.get(member__user__username=username, group=group)
            instance.delete()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, permission_classes=[IsAuthenticated, GroupPermission], methods=['POST', ])
    def remove_discipline(self, request, pk=None):
        group = self.get_object()
        if 'discipline_id' not in request.data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        discipline_id = request.data['discipline_id']
        instance = Discipline.objects.get(id=discipline_id)
        group.rule.remove(instance)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, permission_classes=[IsAuthenticated, GroupPermission], methods=['POST', ])
    def apply_discipline(self, request, pk=None):
        group = self.get_object()
        if 'discipline_id' not in request.data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        discipline_id = request.data['discipline_id']
        instance = Discipline.objects.get(id=discipline_id)
        group.rule.add(instance)
        return Response(status=status.HTTP_200_OK)
