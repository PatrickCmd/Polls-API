from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PollViewSet, ChoiceList, CreateVote, UserCreate, LoginView #PollList, PollDetail,

router = DefaultRouter()
router.register('polls', PollViewSet, base_name='polls')

urlpatterns = [
    # path("polls/", PollList.as_view(), name="poll_list"),
    # path("polls/<int:pk>/", PollDetail.as_view(), name="poll_detail"),
    path("users/", UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
    path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choice_list"),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),
]

urlpatterns += router.urls
