from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from reviewcopies import models
from reviewcopies.serializers.branches import BranchListSerializer
from reviewcopies.permissions import IsStudent

class BranchListView(ListAPIView):
    serializer_class = BranchListSerializer
    def get_queryset(self):
        session = get_object_or_404(models.Session, slug=self.kwargs["session"])
        return models.Branch.objects.filter(courses__sessions=session).distinct()


branch_list_view = BranchListView.as_view()
