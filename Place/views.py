from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from rest_framework.viewsets import ModelViewSet #mrs
from django.db.models import Avg
class PlaceViewSet(ModelViewSet):#mrs
    # queryset = Place.objects.prefetch_related("placeimage_set").select_related("city_id").all()   *********************
    # queryset = Place.objects.all()
    queryset = Place.objects.annotate(avg_rate=Avg('rates__rate')).all()

    serializer_class = PlaceSerializer
    ordering_fields = ['-rate']

class PlaceImageViewSet(ModelViewSet):#mrs
    queryset = PlaceImage.objects.all()
    serializer_class = PlaceImageSerializer

class RateViewSet(ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    ordering_fields = ['-rate']


class LikeViewSet(GenericAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]   
    
    def post(self, request, id, *args, **kwargs):
        user = request.user
        place = Place.objects.get(pk=id)
        serializer = LikeSerializer(data=request.data, context = {'place': experience, 'user': request.user})
        if serializer.is_valid():
            user_likes = Like.objects.filter(user=user, place=Place)
            if user_likes.exists():
                return Response("You have liked before", status=status.HTTP_400_BAD_REQUEST)
            else:
                place.like_number += 1
                plece.save()
                serializer.save(user=user, place=Place)
                return Response(serializer.data, status=status.HTTP_200_OK)

        
class UnLikeViewSet(GenericAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    # permission_classes = [IsAuthenticated]   
    
    def post(self, request, id, *args, **kwargs):
        user = request.user
        place = place.objects.get(pk=id)
        serializer = LikeSerializer(data=request.data, context = {'place': Place, 'user': request.user})
        if serializer.is_valid():
            user_likes = Like.objects.filter(user=user, place=Place)
            if user_likes.exists():
                Place.like_number -= 1
                Place.save()
                user_likes.delete()
                return Response("Like deleted", status=status.HTTP_200_OK)
            else:
                return Response("You haven't liked this experience before", status=status.HTTP_400_BAD_REQUEST)
                

class CommentViewSet(ModelViewSet):
	queryset = Comment.objects.select_related('place').all()
	serializer_class = CommentSerializer
	# permission_classes = [IsAuthenticatedOrReadOnly]

	def get_queryset(self):
		return Comment.objects.filter(
			experience_id=self.kwargs.get('place_pk'), parent=None)\
			.order_by('-created_date')
	
	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['place'] = self.kwargs.get('place_pk')
		return context


	def create(self, request, *args, **kwargs):
		get_object_or_404(Experience.objects, pk=self.kwargs.get('place_pk'))
		return super().create(request, *args, **kwargs)

	def update(self, request, *args, **kwargs):
		return self.perform_change(request, 'update', *args, **kwargs)

	def destroy(self, request, *args, **kwargs):
		return self.perform_change(request, 'destroy', *args, **kwargs)

	def perform_change(self, request, action, *args, **kwargs):
		user = request.user
		comment = self.get_object()
		place = comment.place
		if not comment.is_owner(user):
			return Response('you do not have permission to change this comment.',
							 status=status.HTTP_403_FORBIDDEN)
		if action == 'update':
			return super().update(request, *args, **kwargs)
		response = super().destroy(request, *args, **kwargs)
		place.update_comment_no()
		return response

class ReplytViewSet(CommentViewSet):
	queryset = Comment.objects.select_related('parent').all()
	serializer_class = ReplySerializer
	http_method_names = ['post', 'put', 'delete']

	def get_queryset(self):
		return Comment.objects.filter(
			Q(experience_id=self.kwargs.get('place_pk'))&~Q(parent=None))\
			.order_by('-created_date')
	
	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['parent'] = self.kwargs.get('parent_pk')
		return context

	def create(self, request, *args, **kwargs):
		get_object_or_404(Experience.objects, pk=self.kwargs.get('place_pk'))
		get_object_or_404(Comment.objects, pk=self.kwargs.get('parent_pk'))
		return super().create(request, *args, **kwargs)
