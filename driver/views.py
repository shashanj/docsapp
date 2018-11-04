from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse
from dashboard.models import RideDriver, Ride
from driver.models import Driver
from datetime import datetime
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

class Rides(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            ride_id = Ride.objects.get(id=data['ride_id'])
            driver_id = Driver.objects.get(id=data['driver_id'])

            ride_driver = RideDriver()
            ride_driver.ride_id = ride_id
            ride_driver.createts = datetime.now()
            ride_driver.last_updatets = datetime.now()
            ride_driver.driver_id = driver_id
            ride_driver.status = 1
            ride_driver.save()

            return JsonResponse({'code': '200', 'message': 'ok'}, status=200)

        except ObjectDoesNotExist as e:
            return JsonResponse({'code': '400', 'message': 'Ride Or Driver Does Not Exist'}, status=400)
        except IntegrityError as e:
            return JsonResponse({'code': '400', 'message': 'This ride is already taken.'}, status=400)
        except KeyError as e:
            return JsonResponse({'code': '400', 'message': 'Bad Request'}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'code': '500', 'message': 'Internal Server Error'}, status=500)

    def get(self, request, *args, **kwargs):
        try:
            driver_id = Driver.objects.get(id=request.GET['id'])
        except KeyError as e:
            return JsonResponse({'code': '400', 'message': 'Bad Request'}, status=400)
        except ObjectDoesNotExist as e:
            return JsonResponse({'code': '400', 'message': 'Driver Does Not Exist'}, status=400)

        rides = RideDriver.objects.all().values_list('ride_id', flat=True)
        waiting = Ride.objects.exclude(id__in=rides)
        finished = RideDriver.objects.filter(status=2, driver_id=driver_id)
        ongoing = RideDriver.objects.filter(status=1, driver_id=driver_id)

        wait_rides = []
        ongoing_rides = []
        finished_rides = []
        for ride in waiting:
            wait_rides.append({
                'id' : ride.id,
                'customer' : ride.customer.id,
                'createts' : ride.createts
            })

        for ride in ongoing:
            ongoing_rides.append({
                'id': ride.ride_id.id,
                'customer': ride.ride_id.customer.id,
                'createts': ride.ride_id.createts
            })

        for ride in finished:
            finished_rides.append({
                'id': ride.ride_id.id,
                'customer': ride.ride_id.customer.id,
                'createts': ride.ride_id.createts
            })

        resp = {
            'waiting_rides' : wait_rides,
            'ongoing_rides' : ongoing_rides,
            'finished_rides' : finished_rides
        }

        return JsonResponse({'code': '200', 'message': 'ok', 'data': resp}, status=200)

    def put(self, request, *args, **kwargs):
        data = request.data
        try:
            ride_id = Ride.objects.get(id=data['ride_id'])

            ride_driver = RideDriver.objects.get(ride_id = ride_id, status=1)
            ride_driver.ride_id = ride_id
            ride_driver.last_updatets = datetime.now()
            ride_driver.status = 2
            ride_driver.save()

            return JsonResponse({'code': '200', 'message': 'ok'}, status=200)

        except ObjectDoesNotExist as e:
            return JsonResponse({'code': '400', 'message': 'Ride Or Driver Does Not Exist'}, status=400)
        except IntegrityError as e:
            return JsonResponse({'code': '400', 'message': 'This ride is already taken.'}, status=400)
        except KeyError as e:
            return JsonResponse({'code': '400', 'message': 'Bad Request'}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'code': '500', 'message': 'Internal Server Error'}, status=500)


    def delete(self, request, *args, **kwargs):
        return JsonResponse({'code': '405', 'message': 'Method Not Allowed'}, status=405)
