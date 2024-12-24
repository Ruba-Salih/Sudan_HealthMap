from rest_framework.views import APIView
from rest_framework.response import Response
from .models import State
from .serializers import StateSerializer

class StateListAPIView(APIView):
    """
    API View to list all states.
    """
    def get(self, request):
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data)
