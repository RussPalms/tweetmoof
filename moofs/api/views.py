import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from ..models import Moof
from ..forms import MoofForm
from ..serializers import (
    MoofSerializer, 
    MoofActionSerializer,
    MoofCreateSerializer
)

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@api_view(['POST']) # http method the client == POST
# @authentication_classes([SessionAuthentication, MyCustomAuth])
@permission_classes([IsAuthenticated])
def moof_create_view(request, *args, **kwrgs):
    serializer = MoofCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=200)

def get_paginated_queryset_response(qs, request):
    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginated_qs = paginator.paginate_queryset(qs, request)
    username = request.GET.get('username') # ?username=russell
    serializer = MoofSerializer(paginated_qs, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data) 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def moof_feed_view(request, *args, **kwargs):
    user = request.user
    qs = Moof.objects.feed(user)
    #print(user)
    return get_paginated_queryset_response(qs, request)

@api_view(['GET'])
def moof_list_view(request, *args, **kwargs):
    qs = Moof.objects.all()
    username = request.GET.get('username') # ?username=russell
    if username != None:
        qs = qs.by_username(username)
    return get_paginated_queryset_response(qs, request)

@api_view(['GET'])
def moof_detail_view(request, moof_id, *args, **kwargs):
    qs = Moof.objects.filter(id=moof_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = MoofSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def moof_delete_view(request, moof_id, *args, **kwargs):
    qs = Moof.objects.filter(id=moof_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this moof"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Moof removed"}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def moof_action_view(request, *args, **kwargs):
    #print(request.data)
    '''
    id is required
    Action options are: like, unlike, remoof
    '''
    serializer = MoofActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        moof_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Moof.objects.filter(id=moof_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = MoofSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = MoofSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "remoof":
            new_moof = Moof.objects.create(
                user=request.user, 
                parent=obj,
                content=content
            )
            serializer = MoofSerializer(new_moof)
            #print(serializer.data)
            return Response(serializer.data, status=201)
    return Response({}, status=200)


def moof_create_view_pure_django(request, *args, **kwargs):
    '''
    REST API Create View -> DRF
    '''
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if is_ajax(request=request):
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    # error testing
    # print(abc)
    print("ajax", is_ajax(request=request))
    form = MoofForm(request.POST or None) 
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        # do other form related logic
        obj.user = user
        obj.save()
        if is_ajax(request=request):
            return JsonResponse(obj.serialize(), status=201) # 201 == created items
        if next_url != None and url_has_allowed_host_and_scheme(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = MoofForm()
    if form.errors:
        if is_ajax(request=request):
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})

def moof_list_view_pure_django(request, *args, **kwargs):
    qs = Moof.objects.all()
    moofs_list = [x.serialize() for x in qs]
    data= {
        "isUser": False,
        "response": moofs_list,
    }
    return JsonResponse(data)

def moof_detail_view_pure_django(request, moof_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript
    return json data
    """
    data = {
        "id": moof_id,
    }
    status = 200
    try:
        obj = Moof.objects.get(id=moof_id)
        data['content'] = obj.content
    except:
        data['message'] = 'Not found'
        status = 404
    return JsonResponse(data, status=status) # json.dumps content_type='application/json'
