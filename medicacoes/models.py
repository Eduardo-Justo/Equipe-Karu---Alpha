from django.db import models
from django.utils import timezone


class Medicacao(models.Model):
    VIA_ADMINISTRACAO = [
        ("ORAL", "Oral"),
        ("IM", "Intramuscular"),
    ]

    nome = models.CharField(max_length=150)
    dosagem = models.CharField(max_length=100)              # Ex: "1 mL", "2 gotas", "10 mg"
    frequencia = models.CharField(max_length=100)           # Ex: "1x ao dia", "mensal"
    via = models.CharField(max_length=10, choices=VIA_ADMINISTRACAO)
    duracao_dias = models.IntegerField()
    data_inicio = models.DateField(default=timezone.now)
    cuidados_especiais = models.TextField(blank=True)

    # Identificador simbólico do bebê
    bebe_id = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome} ({self.bebe_id})"


class Lembrete(models.Model):
    medicacao = models.ForeignKey(Medicacao, on_delete=models.CASCADE, related_name="lembretes")
    horario = models.TimeField()                            # horário exato da dose
    canal_preferido = models.CharField(max_length=20, default="APP")  # APP, SMS, WHATSAPP
    tolerancia_minutos = models.IntegerField(default=30)

    def __str__(self):
        return f"Lembrete de {self.medicacao.nome} às {self.horario}"


class RegistroAdministracao(models.Model):
    OPCOES = [
        ("TOMEI", "Tomei/Dei a medicação"),
        ("ESQUECI", "Esqueci"),
        ("RECUSEI", "Bebê recusou"),
        ("VOMITOU", "Vomitou após tomar"),
    ]

    medicacao = models.ForeignKey(Medicacao, on_delete=models.CASCADE, related_name="registros")
    horario_registro = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=OPCOES)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.medicacao.nome} - {self.status} ({self.horario_registro.date()})"


class Estoque(models.Model):
    medicacao = models.OneToOneField(Medicacao, on_delete=models.CASCADE, related_name="estoque")
    quantidade_total_ml = models.FloatField()
    consumo_diario_estimado_ml = models.FloatField()

    # alerta automático gerado quando < 3 dias restantes
    alerta_baixo_estoque = models.BooleanField(default=False)

    def atualizar_alerta(self):
        dias_restantes = self.quantidade_total_ml / self.consumo_diario_estimado_ml
        self.alerta_baixo_estoque = dias_restantes <= 3
        self.save()

    def __str__(self):
        return f"Estoque de {self.medicacao.nome}"

