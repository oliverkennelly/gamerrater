from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Game, Category, GameCategory
from django.db.models import Q


class GameView(ViewSet):
    """Game view set"""


    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        categories_ids = request.data.get('categories', [])
        categories = Category.objects.filter(id__in=categories_ids)

        game = Game()
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.year_released = request.data["year_released"]
        game.number_of_players = request.data["number_of_players"]
        game.estimated_time = request.data["estimated_time"]
        game.age_rec = request.data["age_rec"]

        try:
            game.save()
            for category in categories:
                GameCategory.objects.create(game=game, category=category)
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.title = request.data["title"]
            game.description = request.data["description"]
            game.designer = request.data["designer"]
            game.year_released = request.data["year_released"]
            game.number_of_players = request.data["number_of_players"]
            game.estimated_time = request.data["estimated_time"]
            game.age_rec = request.data["age_rec"]
            game.average_score = request.data["average_score"]
            game.save()
            serializer = GameSerializer(game)
        except game.DoesNotExist:
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
            game = Game.objects.get(pk=pk)
            game.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        search_text = self.request.query_params.get('q', None)
        try:
            if search_text is not None:
                games = Game.objects.filter(
                    Q(title__contains=search_text) |
                    Q(description__contains=search_text) |
                    Q(designer__contains=search_text)
                )
            else:
                games = Game.objects.all()
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer"""
    categories = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ( 'id', 'title', 'designer', 'description', 'year_released', 'number_of_players', 'estimated_time', 'age_rec', 'categories', 'average_score')