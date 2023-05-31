from datetime import datetime
import math

from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics

from alerts.models import Alert
from alerts.serializers import AlertSerializer

class AlertView(APIView): 
    permission_classes = (IsAuthenticated, )

    serializer_class = AlertSerializer
    queryset = Alert.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("status")
        alerts = Alert.objects.all()
        total_alerts = alerts.count()
        if search_param:
            alerts = alerts.filter(status=int(search_param))
        serializer = self.serializer_class(alerts[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_alerts,
            "page": page_num,
            "last_page": math.ceil(total_alerts / limit_num),
            "alerts": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # send_mail('Subject here', 'Here is the message.', 'abhi521993@gmail.com', [request.user.email], fail_silently=False)
            return Response({"status": "success", "data": {"alert": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AlertDetail(generics.GenericAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

    def get_alert(self, pk):
        try:
            return Alert.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        alert = self.get_alert(pk=pk)
        if alert == None:
            return Response({"status": "fail", "message": f"Alert with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(alert)
        return Response({"status": "success", "data": {"alert": serializer.data}})

    def patch(self, request, pk):
        alert = self.get_alert(pk)
        if alert == None:
            return Response({"status": "fail", "message": f"Alert with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            alert, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['updatedAt'] = datetime.now()
            serializer.save()
            return Response({"status": "success", "data": {"Alert": serializer.data}})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        alert = self.get_alert(pk)
        if alert == None:
            return Response({"status": "fail", "message": f"Alert with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        alert.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)