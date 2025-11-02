from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Post
from .serializers import PostSerializer


@permission_classes([IsAuthenticated])
@api_view(['POST', 'GET'])
def create_and_read_all(request):
    if request.method == 'POST':
        new_post = PostSerializer(data={**request.data, 'author': request.user.pk})
        if new_post.is_valid():
            new_post.save(author=request.user)
            return Response(new_post.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_post.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        all_posts = Post.objects.filter(author=request.user.pk)
        if all_posts:
            posts_to_display = PostSerializer(all_posts, many=True)
            return Response(data=posts_to_display.data, status=status.HTTP_200_OK)
        else:
            return Response(data={'msg': 'Nothing to display'}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
def specific_post(request, pk):
    try:
        user_id = request.user.pk
        postObject = Post.objects.get(pk=pk, author=user_id)
    except Post.DoesNotExist:
        return Response(data={'msg': 'Invalid ID'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        post = PostSerializer(postObject)
        return Response(data=post.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        updated_post = PostSerializer(postObject, data=request.data, partial=True)
        if updated_post.is_valid():
            updated_post.save()
            return Response(data=updated_post.data, status=status.HTTP_200_OK)
        else:
            return Response(data={'msg': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        postObject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
