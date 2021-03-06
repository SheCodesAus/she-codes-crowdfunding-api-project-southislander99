from django.http import Http404
from django.db.models import Max, Count

from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .models import Project, Pledge, Category, Comment
from .permissions import IsOwnerOrReadOnly
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer, CategorySerializer, CommentSerializer, ProjectCommentSerializer


class ProjectList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        projects = Project.objects.all()

        #filter for open projects only
        is_open = request.query_params.get('is_open', None)
        if is_open:
            projects = projects.filter(is_open=is_open)

        #order by date created
        order_by = request.query_params.get('order_by', None)
        if order_by == 'date_created':
            projects = projects.order_by(order_by)

        #order by the most recent pledges
        if order_by == 'recent_pledges':
            projects = Project.objects.annotate(
                pledge_date=Max('pledges_date_created')
            ).order_by(
                '-pledge_date'
            )

        #order by the number of pledges
        if order_by == 'num_pledges':
            projects = Project.objects.annotate(
                pledge_count=Count('pledges')
            ).order_by(
                '-pledge_count'
            )

        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(projects, request)

        serializer = ProjectSerializer(result_page, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CategoryDetail(APIView):
    
    def get_object(self, **kwargs):
        try:
            if "slug" in kwargs:
                return Category.objects.get(slug=kwargs["slug"])
            return Category.objects.get(pk=kwargs["pk"])
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, **kwargs):
        category = self.get_object(**kwargs)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


class ProjectDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
        ]

    def get_objects(self, pk):
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_objects(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_objects(pk)
        data = request.data
        serializer = ProjectDetailSerializer(
            instance = project,
            data = data,
            partial = True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.errors, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = self.get_objects(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PledgeList(APIView):
    
    def get(self, request):
        pledges = Pledge.objects.all()
        order_by = request.query_params.get('order_by', None)
        if order_by:
            pledges = pledges.order_by(order_by)
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(supporter=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class CommentList(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Comment.objects.filter(visible=True)
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    queryset = Comment.objects.filter(visible=True)
    serializer_class = CommentSerializer


class ProjectCommentList(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    serializer_class = ProjectCommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, project_id=self.kwargs.get("pk"))

    def get_queryset(self):
        return Comment.objects.filter(project_id=self.kwargs.get("pk"))
