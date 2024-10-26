from django.db import models

class Candidato(models.Model):

    STATUS_CHOICES = (
        ("pendente", "Pendente"),
        ("encontrado", "Encontrado"),
    )

    name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pendente",)
    approval_date = models.DateField(null=True, blank=True)
    ocorrencias = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
