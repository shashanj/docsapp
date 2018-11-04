from django.shortcuts import render
from rest_framework import generics
from django.http import HttpResponse, JsonResponse
from dashboard.models import Ride, RideDriver
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class Ride(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            customer_id = data['customer_id']
            lat = data['lat']
            long = data['long']

            ride = Ride()

            ride.customer = customer_id
            ride.createts = datetime.now()
            ride.lat = lat
            ride.long = long

            ride.save()

            return JsonResponse({'code': '200', 'message': 'ok'}, status=200)

        except KeyError as e:
            return JsonResponse({'code': '405', 'message': 'Method Not Allowed'}, status=405)

        except Exception as e:
            print(e)
            return JsonResponse({'code': '500', 'message': 'Internal Server Error'}, status=500)

    def get(self, request, *args, **kwargs):
        rides = Ride.objects.all()
        resp = []

        for ride in rides:
            try:
                drive_status = RideDriver.objects.get(ride_id=ride)
                status = 'Ongoing' if drive_status.status ==1 else 'Complete'
                resp.append({
                    'id':ride.id,
                    'customer_id':ride.customer_id,
                    'time_elapsed':datetime.now()- ride.createts,
                    'status':status,
                    'driver':drive_status.driver_id.id
                })
            except ObjectDoesNotExist:
                resp.append({
                    'id':ride.id,
                    'customer_id':ride.customer_id,
                    'time_elapsed':datetime.now()- ride.createts,
                    'status':'Waiting',
                    'driver':'None'
                })

        return JsonResponse({'code': '200', 'message': 'OK', 'data':resp}, status=200)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'code': '405', 'message': 'Method Not Allowed'}, status=405)

    def delete(self, request, *args, **kwargs):

        return JsonResponse({'code': '405', 'message': 'Method Not Allowed'}, status=405)
