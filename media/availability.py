


import datetime
from myapp.models import Room, Booking



def check_availability(room, check_in, check_out):
    avail_list=[]
    Booking_list = Booking.objects.filter(room=room)
    for booking in Booking_list:
        # if booking.check_availability(check_in, check_out):
        #     avail_list.append(booking)
        #     return avail_list
        # else:
        #     print("ERROR: " + str(booking))
        if booking.check_in > check_out or booking.check_out < check_in:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)
        




