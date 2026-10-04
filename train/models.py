from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="routes_as_source"
    )
    destination = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="routes_as_destination"
    )
    distance = models.IntegerField()

    class Meta:
        unique_together = ("source", "destination")
        ordering = ["source", "destination"]

    def clean(self):
        if self.source_id and self.destination_id and self.source_id == self.destination_id:
            raise ValidationError("Source and destination stations must be different.")

    def __str__(self):
        return f"{self.source} -> {self.destination}"


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name_plural = "crew"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class TrainType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=255)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(
        TrainType, on_delete=models.CASCADE, related_name="trains"
    )

    class Meta:
        ordering = ["name"]

    @property
    def capacity(self):
        return self.cargo_num * self.places_in_cargo

    def __str__(self):
        return self.name


class Journey(models.Model):
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="journeys"
    )
    train = models.ForeignKey(
        Train, on_delete=models.CASCADE, related_name="journeys"
    )
    crew = models.ManyToManyField(Crew, related_name="journeys", blank=True)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        ordering = ["-departure_time"]

    def clean(self):
        if (
            self.departure_time
            and self.arrival_time
            and self.arrival_time <= self.departure_time
        ):
            raise ValidationError("Arrival time must be after departure time.")

    def __str__(self):
        return f"{self.route} ({self.departure_time:%Y-%m-%d %H:%M})"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} ({self.created_at:%Y-%m-%d %H:%M})"


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = models.ForeignKey(
        Journey, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        unique_together = ("journey", "cargo", "seat")
        ordering = ["cargo", "seat"]

    @staticmethod
    def validate_ticket(cargo, seat, train, error_to_raise):
        for ticket_attr_value, ticket_attr_name, train_attr_name in [
            (cargo, "cargo", "cargo_num"),
            (seat, "seat", "places_in_cargo"),
        ]:
            count_attrs = getattr(train, train_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: (
                            f"{ticket_attr_name} must be in range "
                            f"[1, {count_attrs}], not {ticket_attr_value}"
                        )
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.cargo, self.seat, self.journey.train, ValidationError
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.journey} - cargo {self.cargo}, seat {self.seat}"
