from django.db import models


class TechNote(models.Model):
    patient_name = models.CharField(max_length=30)
    exam_date = models.DateField()
    tech_initials = models.CharField(max_length=10)
    patient_age = models.CharField(max_length=4)
    accession = models.CharField(max_length=10)
    comments = models.TextField()
    modality = models.ForeignKey('Modality', on_delete=models.CASCADE)


class Modality(models.Model):
    modality_name = models.CharField(max_length=20)

    def __str__(self):
        return self.modality_name
