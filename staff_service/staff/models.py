from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Staff(models.Model):
    gender = models.CharField(max_length=10)
    tel = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    birthday = models.DateField()
    hire_date = models.DateField()
    role = models.ForeignKey(Role, related_name='staffs', on_delete=models.CASCADE)

    def __str__(self):
        return f"Staff {self.id} - {self.email}"
