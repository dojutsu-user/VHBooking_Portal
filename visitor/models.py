from django.db import models
from django.conf import settings
from hostel.models import Hostel
from hostel.util import generate_choices_of_hostels
from django.db.models.signals import post_save, pre_delete, pre_save
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

ROOM_TYPES = (              # specifying the types of rooms. Eg. AC, Non-AC
    ('TYPE1', 'TYPE1'),
    ('TYPE2', 'TYPE2'),
    ('TYPE3', 'TYPE3'),
)


class Visitor(models.Model):
    """
    model for visitors.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    no_of_rooms_required = models.IntegerField(default=1)
    from_date = models.DateField(default=timezone.now().date())
    to_date = models.DateField(default=timezone.now().date())
    date_of_booking = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False, verbose_name='Confirm Booking')
    is_departed = models.BooleanField(default=False, verbose_name="Departed")
    room_preference = models.CharField(max_length=10, choices=ROOM_TYPES, default='TYPE1')

    def is_allotted(self):
        return self.status

    def rooms_required(self):
        return self.no_of_rooms_required

    def __str__(self):
        return self.user.username


class BookingInfo(models.Model):
    """
    model to specify the booking info for the visitor.
    """
    hostel_allotted = models.CharField(max_length=10, choices=generate_choices_of_hostels(), default="1")
    room_no = models.CharField(max_length=10, default='0000')
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, default='TYPE1')

    def __str__(self):
        return self.visitor.user.username

    def required_rooms(self):
        return self.visitor.rooms_required()


def create_booking_info_object(instance, created, *args, **kwargs):
    if created:
        temp = BookingInfo.objects.create(visitor=instance)
        temp.save()
        return temp


# def update_available_rooms_increase(instance, created, *args, **kwargs):
#     if instance.status and not instance.is_departed:
#         if not instance.is_departed:
#             hostel = Hostel.objects.all()
#             booking_info = BookingInfo.objects.filter(visitor=instance)
#             for info in booking_info:
#                 temp = hostel[int(info.hostel_allotted) - 1]
#                 temp.total_available_rooms -= 1
#                 temp.total_booked_rooms += 1
#                 temp.save()


# def update_available_rooms_after_delete(sender, instance, using, *args, **kwargs):
#     hostel = Hostel.objects.all()
#     if instance.status:
#         booking_info = BookingInfo.objects.filter(visitor=instance)
#         for temp in booking_info:
#             hostel_obj = temp.hostel_allotted
#             x = hostel[int(hostel_obj) - 1]
#             x.total_available_rooms += 1
#             x.total_booked_rooms -= 1
#             x.save()


# def update_is_arrived(sender, instance, *args, **kwargs):
#     try:
#         obj = sender.objects.get(pk=instance.pk)
#     except sender.DoesNotExist:
#         pass
#     else:
#         if not obj.is_arrived == instance.is_arrived:
#             if instance.is_arrived:
#                 instance.arrived_at = timezone.now()


# def update_is_departed(sender, instance, *args, **kwargs):
#     try:
#         obj = sender.objects.get(pk=instance.pk)
#     except sender.DoesNotExist:
#         pass
#     else:
#         if not obj.is_departed == instance.is_departed:
#             if instance.is_departed:
#                 instance.departed_at = timezone.now()
#                 hostel = Hostel.objects.all()
#                 booking_info = BookingInfo.objects.filter(visitor=instance)
#                 for info in booking_info:
#                     temp = hostel[int(info.hostel_allotted) - 1]
#                     temp.total_available_rooms += 1
#                     temp.total_booked_rooms -= 1
#                     temp.save()


# post_save.connect(create_booking_info_object, sender=Visitor)
# post_save.connect(update_available_rooms_increase, sender=Visitor)
# pre_delete.connect(update_available_rooms_after_delete, sender=Visitor)
# pre_save.connect(update_is_arrived, sender=Visitor)
# pre_save.connect(update_is_departed, sender=Visitor)
