from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import GameCategory, Game, Category

class GameCategoryView(ViewSet):
    """GameCategory view set"""

    def create(self, request):
        """Handle POST operations"""
        game_category = GameCategory()
        game_category.game = Game.objects.get(pk=request.data["game_id"])
        game_category.category = Category.objects.get(pk=request.data["category_id"])

        try:
            game_category.save()
            serializer = GameCategorySerializer(game_category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            game_category = GameCategory.objects.get(pk=pk)
            serializer = GameCategorySerializer(game_category)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            game_category = GameCategory()
            game_category.game = Game.objects.get(pk=request.data["game_id"])
            game_category.category = Category.objects.get(pk=request.data["category_id"])
            game_category.save()
        except GameCategory.DoesNotExist:
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
            game_category = GameCategory.objects.get(pk=pk)
            game_category.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except GameCategory.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            game_categories = GameCategory.objects.all()
            serializer = GameCategorySerializer(game_categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

class GameCategorySerializer(serializers.ModelSerializer):
    """JSON serializer for GameCategories"""

    class Meta:
        model = GameCategory
        fields = ('id', 'game', 'category')