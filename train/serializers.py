from django.db import transaction
from rest_framework import serializers

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


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")

    def validate(self, attrs):
        source = attrs.get("source", getattr(self.instance, "source", None))
        destination = attrs.get(
            "destination", getattr(self.instance, "destination", None)
        )
        if source and destination and source == destination:
            raise serializers.ValidationError(
                "Source and destination stations must be different."
            )
        return attrs


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(slug_field="name", read_only=True)
    destination = serializers.SlugRelatedField(slug_field="name", read_only=True)


class RouteDetailSerializer(RouteSerializer):
    source = StationSerializer(read_only=True)
    destination = StationSerializer(read_only=True)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "full_name")


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ("id", "name")


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = (
            "id",
            "name",
            "cargo_num",
            "places_in_cargo",
            "train_type",
            "capacity",
        )


class TrainListSerializer(TrainSerializer):
    train_type = serializers.SlugRelatedField(slug_field="name", read_only=True)


class TrainDetailSerializer(TrainSerializer):
    train_type = TrainTypeSerializer(read_only=True)


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = (
            "id",
            "route",
            "train",
            "crew",
            "departure_time",
            "arrival_time",
        )

    def validate(self, attrs):
        departure_time = attrs.get(
            "departure_time", getattr(self.instance, "departure_time", None)
        )
        arrival_time = attrs.get(
            "arrival_time", getattr(self.instance, "arrival_time", None)
        )
        if departure_time and arrival_time and arrival_time <= departure_time:
            raise serializers.ValidationError(
                "Arrival time must be after departure time."
            )
        return attrs


class JourneyListSerializer(JourneySerializer):
    route = serializers.StringRelatedField(read_only=True)
    train_name = serializers.CharField(source="train.name", read_only=True)
    train_capacity = serializers.IntegerField(
        source="train.capacity", read_only=True
    )
    tickets_available = serializers.SerializerMethodField()

    class Meta(JourneySerializer.Meta):
        fields = JourneySerializer.Meta.fields + (
            "train_name",
            "train_capacity",
            "tickets_available",
        )

    def get_tickets_available(self, obj):
        return obj.train.capacity - obj.tickets.count()


class JourneyDetailSerializer(JourneySerializer):
    route = RouteDetailSerializer(read_only=True)
    train = TrainDetailSerializer(read_only=True)
    crew = CrewSerializer(many=True, read_only=True)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "journey")

    def validate(self, attrs):
        journey = attrs.get("journey", getattr(self.instance, "journey", None))
        Ticket.validate_ticket(
            attrs.get("cargo", getattr(self.instance, "cargo", None)),
            attrs.get("seat", getattr(self.instance, "seat", None)),
            journey.train,
            serializers.ValidationError,
        )
        return attrs


class TicketListSerializer(TicketSerializer):
    journey = JourneyListSerializer(read_only=True)


class TicketSeatSerializer(TicketSerializer):
    class Meta(TicketSerializer.Meta):
        fields = ("cargo", "seat")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
