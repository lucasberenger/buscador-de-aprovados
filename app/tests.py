from django.test import TestCase
from .models import Candidato
from datetime import date

"""Teste Modelo Candidato"""
class CandidatoTestCase(TestCase):
    
    def setUp(self):
        """cria as intâncias para o teste"""
        Candidato.objects.create(
            name="José Eduardo Silva",
            cpf="12345678910",
            status="aprovado",
            approval_date=date(2024, 8, 8)
        )
        Candidato.objects.create(
            name="Maria Elvira Santos",
            cpf="12345612312",
            status="pendente",
            approval_date=None
        )

    def test_candidatos(self):
        candidato1 = Candidato.objects.get(name="José Eduardo Silva")
        candidato2 = Candidato.objects.get(name="Maria Elvira Santos")

        self.assertEqual(candidato1.status, 'aprovado')
        self.assertEqual(candidato2.status, 'pendente')
        
        self.assertEqual(candidato1.approval_date, date(2024, 8, 8))
        self.assertIsNone(candidato2.approval_date)
        
