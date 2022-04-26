from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import CustomUser, Badge
from .serializers import BadgeSerializer, BadgeDetailSerializer, CustomUserSerializer, RegisterSerializer, CustomUserDetailSerializer


class CustomUserList(APIView):

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CustomUserDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserDetailSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        data = request.data
        serializer = CustomUserDetailSerializer(
            instance=user,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny,]
    queryset = CustomUser.objects.all()


class BadgeView(generics.ListCreateAPIView):
    serializer_class = BadgeSerializer
    queryset = Badge.objects.all()
    permission_classes = [permissions.IsAdminUser]


class BadgeDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Badge.objects.get(pk=pk)
        except Badge.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        badge = self.get_object(pk)
        serializer = BadgeDetailSerializer(badge)
        return Response(serializer.data)

    def put(self, request, pk):
        badge = self.get_object(pk)
        data = request.data
        serializer = BadgeDetailSerializer(
            instance=badge,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        badge = self.get_object(pk)
        badge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)