from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend


from .serializers import PollSerializer, QuestionSerializer, VoteSerializer
from .models import Poll, Question, Vote
from .permissions import PollPermission



class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (PollPermission, )


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAdminUser, )


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(user=self.request.user)
        
        return super().perform_create(serializer)
