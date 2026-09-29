from django.contrib import admin

from train.models import (
    Station,
    Route,
    Crew,
    TrainType,
    Train,
    Journey,
    Order,
    Ticket,
)


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "latitude", "longitude")
    search_fields = ("name",)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("id", "source", "destination", "distance")
    list_filter = ("source", "destination")
    search_fields = ("source__name", "destination__name")


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name")
    search_fields = ("first_name", "last_name")


@admin.register(TrainType)
class TrainTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "train_type", "cargo_num", "places_in_cargo")
    list_filter = ("train_type",)
    search_fields = ("name",)


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0


@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ("id", "route", "train", "departure_time", "arrival_time")
    list_filter = ("route", "train")
    filter_horizontal = ("crew",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    list_filter = ("user",)
    inlines = (TicketInline,)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "journey", "order", "cargo", "seat")
    list_filter = ("journey",)
