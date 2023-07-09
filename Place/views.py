from http import HTTPStatus	
from http.client import ResponseNotReady	
from pickle import NONE	
from django.shortcuts import render	
from .models import *	
from .serializer import *	
from rest_framework.decorators import api_view	
from rest_framework.response import Response	
from rest_framework.viewsets import ModelViewSet	
from rest_framework.viewsets import ModelViewSet #mrs	
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly	
from rest_framework import permissions #mrs  #61	
from rest_framework import status	
from django.db.models import Avg	
from Place import serializer #mrs
import base64
from django.core.files.base import ContentFile
from .models import Place , PlaceImage, Rate
from .serializer import PlaceImageSerializer, PlaceSerializer, RateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ModelViewSet #mrs
from rest_framework import permissions #mrs  #61
from rest_framework import status
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
# from Profile import permissions as permi
from rest_framework import viewsets
from rest_framework.decorators import action #lesson 60

from django.db.models import Q

class PlaceViewSet(ModelViewSet):#mrs 
    # permission_classes=[permi.CrudOrganizationReadOther]
    # queryset = Place.objects.prefetch_related("placeimage_set").select_related("city_id").all()   *********************
    queryset = Place.objects.all()
    # queryset = Place.objects.annotate(avg_rate=Avg('rates__rate')).all()
    serializer_class = PlaceSerializer
    # ordering_fields = ['-rate']
    
class PlaceImageViewSet(ModelViewSet):#mrs
    queryset = PlaceImage.objects.all()
    serializer_class = PlaceImageSerializer
    @action(detail=False , methods=['POST'])#, permission_classes=[IsAuthenticated])#lesson 60 , permi... -> 61
    def imagewithplaceid(self , request):
        try:
            placeid = request.data['place_id']
        except:
            return Response("i want place_id" , status = status.HTTP_400_BAD_REQUEST)
        try:
            placeimage = PlaceImage.objects.filter(place_id = placeid)
        except:
            return Response("i can't find place image with this place id: "+str(placeid) , status = status.HTTP_400_BAD_REQUEST)
        serializer = PlaceImageSerializer(placeimage , many = True)
        # for i in placeimage:
        #     print(i)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    # def post(self, request , *args , **kwargs):
    #     img_b64 = request.post.get('image')
    #     img_data = base64.b64decode(img_b64)
    #     file_name = "my_image.png"
    #     pl_id = request.post.get('place_id')
    #     placeimage = PlaceImage.objects.create(place_id=pl_id)
    #     placeimage.image.save(filename , ContentFile(img_data))
    #     placeimage.save()
    # def get
class RateViewSet(ModelViewSet):
    # permission_classes=[IsAuthenticated]#mrs
    def get_permissions(self):#mrs #61
        if self.request.method in ['POST','PUT','DELETE' , 'PATCH']:
            return [permissions.IsAuthenticated()]
        else:
            return[permissions.AllowAny()]
    def get_queryset(self):#mrs
        rate = Rate.objects.select_related('place').filter(place = self.kwargs.get('Place_pk'))
        return rate
    def create(self, request, *args, **kwargs):        
        user = self.request.user
        user_object = Rate.objects.filter(user = user , place = self.kwargs.get('Place_pk'))
        if user_object.count() >= 1:
            return Response("you can't have duplicate rate" , status=status.HTTP_403_FORBIDDEN)
        else :
            return super().create(request, *args, **kwargs)
    def get_serializer_context(self ):
        return {'user_id':self.request.user}
    serializer_class = RateSerializer
    ordering_fields = ['-rate']

@api_view(['GET'])#mrs     #by default argument => GET  15
def get_specific_placeimage(request , place_idd):
# def retrieve(self, request, *args, **kwargs):
    # instance = self.get_object()
    # place_image = PlaceImage.objects.filter(place_id = place_idd).values("place_id" , "image")
    # serializer = PlaceImageSerializer(place_image)
    # return Response(serializer.data)
    place_image = PlaceImage.objects.filter(place_id = place_idd).values("place_id" , "image")
    # print(place_image)
    return Response(place_image)

from django.db.models import F
@api_view(['GET'])#mrs     #by default argument => GET  15
def get_specific_place(request ,place_id = None, country_name = None , city_name = None):
    place = Place.objects.select_related('city_id' , 'country_id' ).annotate(
        country =F('city_id__country_id__country_name') ,
        city = F('city_id__city_name') ,
        # image = F('placeimage__image')
    ).values("id" ,"name","country", "city","address" , "description","lan", "lon")
    if place_id == None:
        if country_name != None :        
            place =place.filter(city_id__country_id__country_name=country_name)
            if city_name == None:
                place =place.filter(city_id__country_id__country_name = country_name )
            else :
                place =place.filter(city_id__country_id__country_name = country_name , city_id__city_name=city_name )
    else:
        place=place.filter(id = place_id )
    # serializers = PlaceFrontSerializer(place , many = True)
    # return Response(serializers.data)
    return Response(place)
    # place = Place.objects.select_related('city_id' , 'country_id' ).prefetch_related('placeimage_set').annotate(
    #     country =F('city_id__country_id__country_name') ,
    #     city = F('city_id__city_name') ,
    #     image = F('placeimage__image')
    # ).values("id" ,"name","country", "city","address" , "description","lan", "lon" , "image")


# from rest_framework import generics
# class CommentViewSet(generics.ListCreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

# class ReplytViewSet(generics.CreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = ReplySerializer

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['comment_id'] = self.kwargs['comment_id']
#         return context

class CommentViewSet(ModelViewSet):	
    # queryset = Comment.objects.all()
	queryset = Comment.objects.select_related('place').all()	
	serializer_class = CommentSerializer	
	permission_classes = [IsAuthenticatedOrReadOnly]	
	def get_queryset(self):	
		return Comment.objects.filter(	
			place_id=self.kwargs.get('Place_pk'), parent=None).order_by('-created_date')	
		
	def get_serializer_context(self):	
		context = super().get_serializer_context()	
		context['place'] = self.kwargs.get('Place_pk')	
		return context	

	def create(self, request, *args, **kwargs):	
		get_object_or_404(Place.objects, pk=self.kwargs.get('Place_pk'))	
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
			Q(place_id=self.kwargs.get('place_pk'))&~Q(parent=None)).order_by('-created_date')	
		
	def get_serializer_context(self):	
		context = super().get_serializer_context()	
		context['parent'] = self.kwargs.get('parent_pk')	
		return context	
	def create(self, request, *args, **kwargs):	
		get_object_or_404(Place.objects, pk=self.kwargs.get('place_pk'))	
		get_object_or_404(Comment.objects, pk=self.kwargs.get('parent_pk'))	
		return super().create(request, *args, **kwargs)


# class CustomPlaceImage(APIView):
#     def get(self , request , ):

