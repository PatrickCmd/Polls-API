# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse

# from .models import Poll

# def polls_list(request):
#     MAX_OBJECTS = 20
#     polls = Poll.objects.all()[:20]
#     data = {
#         "results": list(polls.values("question", "created_by_id", "pub_date"))
#     }
#     return JsonResponse(data)

# def poll_detail(request, pk):
#     poll = get_object_or_404(Poll, pk=pk)
#     data = {
#         "results": {
#             "question": poll.question,
#             "created_by": poll.created_by_id,
#             "pub_date": poll.pub_date
#         }
#     }
#     return JsonResponse(data)

#==============APIView==========================+#
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404

# from .models import Poll
# from .serializers import PollSerializer


# class PollList(APIView):
#     def get(self, request):
#         polls = Poll.objects.all()[:20]
#         data = PollSerializer(polls, many=True).data
#         return Response(data)


# class PollDetail(APIView):
#     def get(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         data = PollSerializer(poll).data
#         return Response(data)


#=============Generics========================#
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Poll, Choice, Vote
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer, UserSerialiser


# class PollList(ListCreateAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer


# class PollDetail(RetrieveDestroyAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer

#============using viewset for polllist and pollDetail views==========#
class UserCreate(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerialiser


class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()
    
    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({
                "error": "Wrong Credentials"
            }, status=status.HTTP_400_BAD_REQUEST)


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    # user can only delete poll he created
    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])
        if not request.user == poll.created_by:
            raise PermissionDenied("You can not delete this poll")
        return super().destroy(request, *args, **kwargs)


class ChoiceList(ListCreateAPIView):
    # queryset = Choice.objects.all()
    # serializer_class = ChoiceSerializer
    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs['pk'])
        return queryset
    serializer_class = ChoiceSerializer

    # user can only create choices for polls they have created
    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if not request.user == poll.created_by:
            raise PermissionDenied("You can not create choice for this poll.")
        return super().post(request, *args, **kwargs)


# class CreateVote(CreateAPIView):
#     serializer_class = VoteSerializer


class CreateVote(APIView):
    
    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {'choice':choice_pk, "poll": pk, "voted_by": voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
