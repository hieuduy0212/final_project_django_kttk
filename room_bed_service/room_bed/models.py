from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Room(models.Model):
    room_number = models.CharField(max_length=255)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return f"Room {self.room_number} ({self.type.name})"


class Bed(models.Model):
    bed_number = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    patient_id = models.IntegerField(null=True, blank=True)
    room = models.ForeignKey(Room, related_name='beds', on_delete=models.CASCADE)

    def __str__(self):
        return f"Bed in Room {self.room.room_number} - Status: {self.status}"
