from django.db.models import Count
from django.db.models.functions import Length
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from .permissions import StoryPermission, ChapterPermission, PlotPermission, CharacterPermission
from .serializers import (
    CharacterSerializer,
    ChapterSerializer, 
    PlotSerializer,
    StoryDetailSerializer, 
    StoryMoreDetailSerializer, 
    StorySerializer, 
    TagSerializer, 
)
from groups.models import Group
from disciplines.models import Discipline
from .models import Story, Tag, Character, Chapter, Plot
from .constants import PUBLIC
# Create your views here.

class StoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    serializer_class = StorySerializer
    permission_classes = [StoryPermission, ]

    def get_serializer_class(self):
        if self.action != 'retrieve' or self.request.method == 'POST':
            return StorySerializer

        # if self.request.user.is_anonymous:
        #     return StoryDetailSerializer
        # story = self.get_object()
        # if self.request.user.account in story.participators.all() or self.request.user.account == story.creator:
        return StoryMoreDetailSerializer
        # return StoryDetailSerializer

    def get_queryset(self):
        params = self.request.query_params
        qs = Story.objects.annotate(member_count=Count('participators')).filter(public=PUBLIC)

        if not self.request.user.is_anonymous:
            qs |= Story.objects.filter(participators__screen_name__icontains=self.request.user.account.screen_name)
        if 'order' in params:
            if params['order'] == 'number':
                qs = qs.order_by('-member_count')
        if 'group' in params and params['group'] != '':
            group = Group.objects.get(id=int(params['group']))
            qs = qs.filter(maintainer=group)
        qs = qs.order_by('-created_at')
        if 'title' not in self.request.query_params:
            return qs
        search_content = self.request.query_params['title']
        if len(search_content) < 3:
            return qs
        return qs.filter(title__contains=search_content)

    @action(detail=False, permission_classes=[IsAuthenticated, ])
    def my(self, request):
        stories = Story.objects.filter(creator__screen_name=request.user.account.screen_name)
        if not stories.exists:
            return Response([], status.HTTP_200_OK)
        serializer = self.get_serializer(stories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, permission_classes=[IsAuthenticated, ])
    def joined(self, request):
        stories = Story.objects.filter(participators__screen_name__icontains=request.user.account.screen_name)
        if not stories.exists:
            return Response([], status.HTTP_200_OK)
        serializer = self.get_serializer(stories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(detail=True, permission_classes=[IsAuthenticated, ], methods=['POST', ])
    # def join(self, request, pk=None):
    #     story = self.get_object()
    #     GroupMember.objects.create(member=self.request.user.account, group=group)
    #     return Response(status=status.HTTP_200_OK)
    @action(detail=True, permission_classes=[IsAuthenticated, StoryPermission], methods=['POST', ])
    def remove_members(self, request, pk=None):
        story = self.get_object()
        if 'usernames' not in request.data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        member_usernames = request.data['usernames']
        for username in member_usernames:
            instance = Character.objects.get(player__user__username=username, story=story)
            instance.player = None
            instance.save()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, permission_classes=[IsAuthenticated, StoryPermission], methods=['POST', ])
    def remove_discipline(self, request, pk=None):
        story = self.get_object()
        if 'discipline_id' not in request.data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        discipline_id = request.data['discipline_id']
        instance = Discipline.objects.get(id=discipline_id)
        story.rule.remove(instance)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, permission_classes=[IsAuthenticated, StoryPermission], methods=['POST', ])
    def apply_discipline(self, request, pk=None):
        story = self.get_object()
        if 'discipline_id' not in request.data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        discipline_id = request.data['discipline_id']
        instance = Discipline.objects.get(id=discipline_id)
        story.rule.add(instance)
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, permission_classes=[IsAuthenticated, StoryPermission], methods=['POST', ])
    def remove_tag(self, request, pk=None):
        story = self.get_object()
        if 'tag_id' not in request.data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        tag_id = request.data['tag_id']
        instance = Tag.objects.get(id=tag_id)
        story.category.remove(instance)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, permission_classes=[IsAuthenticated, StoryPermission], methods=['POST', ])
    def apply_tag(self, request, pk=None):
        story = self.get_object()
        if 'tag_id' not in request.data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        tag_id = request.data['tag_id']
        if type(tag_id) == list:
            for _id in tag_id:
                instance = Tag.objects.get(id=_id)
                story.category.add(instance)
        else:
            instance = Tag.objects.get(id=tag_id)
            story.category.add(instance)
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, permission_classes=[AllowAny, ])
    def plots(self, request, pk=None):
        story = self.get_object()
        if 'chapter_id' not in request.query_params:
            return Response(status=status.HTTP_404_NOT_FOUND)
        chapter_id = request.query_params['chapter_id']
        if not story.chapters.filter(id=chapter_id).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        chapter = story.chapters.get(id=chapter_id)
        plots = PlotSerializer(chapter.plots.order_by('created_at'), many=True)
        return Response(plots.data, status=status.HTTP_200_OK)
    
    @action(detail=True, permission_classes=[AllowAny, ])
    def chapters(self, request, pk=None):
        story = self.get_object()
        chapters = ChapterSerializer(story.chapters.order_by('created_at'), many=True)
        return Response(chapters.data, status=status.HTTP_200_OK)

    @action(detail=True, permission_classes=[IsAuthenticated, ], methods=['POST', ])
    def new_chapter(self, request, pk=None):
        story = self.get_object()
        title = request.data['title']
        if Chapter.objects.filter(story=story, title=title).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        chapter = Chapter.objects.create(story=story, title=title)
        return Response(ChapterSerializer(chapter).data, status=status.HTTP_200_OK)

    @action(detail=True, permission_classes=[IsAuthenticated, ], methods=['POST', ])
    def new_plot(self, request, pk=None):
        story = self.get_object()
        content = request.data['content']
        chapter_id = request.data['chapter_id']
        character_id = request.data['character_id']
        if character_id:
            character = Character.objects.get(player=request.user.account, story=story, id=character_id)
        else:
            character = None
        chapter = Chapter.objects.get(id=chapter_id)
        plot = Plot.objects.create(
            written_by=request.user.account, 
            chapter=chapter, 
            content=content
        )
        if not character:
            if Character.objects.filter(player=request.user.account, story=story, default=True).exists():
                character = Character.objects.get(player=request.user.account, story=story, default=True)
                character.updated = plot
                character.save()
            else:
                character = Character.objects.create(player=request.user.account, story=story, appear_at=plot, updated=plot, default=True)
        elif not character.appear_at:
            character.appear_at = plot
            character.updated = plot
            character.save()
        else:
            character.updated = plot
            character.save()
        plot.written_as = character
        plot.save()
        return Response(PlotSerializer(plot).data, status=status.HTTP_200_OK)

    @action(detail=True, permission_classes=[IsAuthenticated, StoryPermission], methods=['POST', ])
    def clear_empty_content(self, request, pk=None):
        story = self.get_object()
        Plot.objects.filter(chapter__story=story).annotate(empty_content=Length('content')).filter(empty_content=0).delete()
        Chapter.objects.filter(story=story).annotate(plot_count=Count('plots')).filter(plot_count=0).delete()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, permission_classes=[IsAuthenticated, StoryPermission], methods=['POST', ])
    def remove_invalid_plots(self, request, pk=None):
        story = self.get_object()
        Plot.objects.filter(chapter__story=story, valid=False).delete()
        return Response(status=status.HTTP_200_OK)
    
    # all characters of the story
    # to fetch the characters of user (in some story), see CharacterViewSet
    @action(detail=True, permission_classes=[AllowAny, ], methods=['GET', ])
    def get_characters(self, request, pk=None):
        story = self.get_object()
        chacaters = CharacterSerializer(Character.objects.filter(story=story), many=True)
        return Response(chacaters.data, status=status.HTTP_200_OK)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        if 'name' not in self.request.query_params:
            return Tag.objects.all()
        search_content = self.request.query_params['name']
        # if len(search_content) < 3:
        #     return Tag.objects.all()
        return Tag.objects.filter(name__contains=search_content)


class ChapterViewSet(viewsets.ModelViewSet):
    serializer_class = ChapterSerializer
    permission_classes = [ChapterPermission, ]

    def get_queryset(self):
        return Chapter.objects.all()

class PlotViewSet(viewsets.ModelViewSet):
    serializer_class = PlotSerializer
    permission_classes = [PlotPermission, ]

    def get_queryset(self):
        return Plot.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        if 'content' in data:
            data['valid'] = False
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CharacterViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    permission_classes = [CharacterPermission, ]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return []
        qs = Character.objects.filter(player=self.request.user.account)
        params = self.request.query_params
        if 'story_id' in params and params['story_id'] != '':
            story_id = int(params['story_id'])
            qs = qs.filter(story__id=story_id)
        return qs
