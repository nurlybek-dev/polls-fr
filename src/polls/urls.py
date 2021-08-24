from rest_framework import routers, urlpatterns

from polls.views import PollViewSet, QuestionViewSet, VoteViewSet


router = routers.DefaultRouter()
router.register('polls', PollViewSet)
router.register('questions', QuestionViewSet)
router.register('votes', VoteViewSet)

urlpatterns = router.urls
