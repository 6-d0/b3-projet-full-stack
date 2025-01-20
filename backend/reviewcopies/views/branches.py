from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from reviewcopies import models
from reviewcopies.serializers.branches import BranchListSerializer, BranchSerializer
from reviewcopies.permissions import IsStudent, IsAdmin
from rest_framework.response import Response
from rest_framework import status

class BranchListView(ListAPIView):
    serializer_class = BranchListSerializer
    def get_queryset(self):
        session = get_object_or_404(models.Session, slug=self.kwargs["session"])
        return models.Branch.objects.filter(courses__sessions=session).distinct()

class CreateBranchView(APIView):
    permission_classes = [IsAdmin]
    def post(self, request, *args, **kwargs):
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class BranchView(APIView):
    def get(self, request):
        branches = models.Branch.objects.all()
        serializer = BranchListSerializer(branches, many=True)
        return Response(serializer.data)

branch_list_view = BranchListView.as_view()
create_branch_view = CreateBranchView.as_view()
branch_view = BranchView.as_view()
