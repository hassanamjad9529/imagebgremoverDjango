from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class RemoveBackgroundAPIView(APIView):
    def post(self, request):
        return Response({"message": "API is working!"}, status=status.HTTP_200_OK)