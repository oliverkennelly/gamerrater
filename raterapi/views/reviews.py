from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Review, Game

class ReviewView(ViewSet):
    """Review view set"""

    def create(self, request):
        """Handle POST operations"""
        review = Review()
        review.user = request.auth.user
        review.game = Game.objects.get(pk=request.data["game_id"])
        review.score = request.data["score"]
        review.comment = request.data["comment"]

        try:
            review.save()
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            review = Review.objects.get(pk=pk)
            review.user = request.auth.user
            review.game = Game.objects.get(pk=request.data["game_id"])
            review.score = request.data["score"]
            review.comment = request.data["comment"]
            review.save()
        except Review.DoesNotExist:
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
            review = Review.objects.get(pk=pk)
            review.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        game_id = self.request.query_params.get('game')
        try:
            reviews = Review.objects.all()
            if game_id is not None:
                reviews = reviews.filter(game_id=game_id)
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for Reviews"""

    class Meta:
        model = Review
        fields = ('id', 'user', 'game', 'score', 'comment')