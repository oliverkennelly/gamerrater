from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import GamePicture
import uuid
import base64
from django.core.files.base import ContentFile


class GamePictureViewSet(ViewSet):
    """GamePicture view set"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        game_picture = GamePicture()
        format, imgstr = request.data["action_pic"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["game_id"]}-{uuid.uuid4()}.{ext}')
        game_picture.action_pic = data
        game_picture.game_id = request.data["game_id"]

        try:
            game_picture.save()
            serializer = GamePictureSerializer(game_picture)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            game_picture = GamePicture.objects.get(pk=pk)
            serializer = GamePictureSerializer(game_picture)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            game_picture = GamePicture.objects.get(pk=pk)
            game_picture.game_id = request.data["game_id"]
            game_picture.action_pic = request.data["action_pic"]
            game_picture.save()
        except GamePicture.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game_picture = GamePicture.objects.get(pk=pk)
            game_picture.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except GamePicture.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            game_pictures = GamePicture.objects.all()
            serializer = GamePictureSerializer(game_pictures, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class GamePictureSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = GamePicture
        fields = ('id', 'game', 'action_pic')