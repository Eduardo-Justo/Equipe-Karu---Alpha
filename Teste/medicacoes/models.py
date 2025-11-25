from django.db import models
from django.utils import timezone


class Medicacao(models.Model):
    """
    Representa uma medicação administrada a um bebê.

    Campos principais:
    - nome: Nome da medicação.
    - dosagem: Quantidade administrada (ex.: "5 ml", "1 comprimido").
    - frequencia: Intervalo entre doses (ex.: "8/8h").
    - via: Forma de administração (oral, intramuscular...).
    - duracao_dias: Quantidade de dias de tratamento.
    - data_inicio: Quando o tratamento começou.
    - cuidados_especiais: Observações extras relevantes.
    - bebe_id: Identificador do bebê (string simples).

    Relações:
    - Estoque (OneToOne)
    - Lembrete (OneToMany via related_name="lembretes")
    - RegistroAdministracao (OneToMany via related_name="registros")
    """

    VIA_ADMINISTRACAO = [
        ("ORAL", "Oral"),
        ("IM", "Intramuscular"),
    ]

    nome = models.CharField(max_length=150)
    dosagem = models.CharField(max_length=100)
    frequencia = models.CharField(max_length=100)
    via = models.CharField(max_length=10, choices=VIA_ADMINISTRACAO)
    duracao_dias = models.IntegerField()
    data_inicio = models.DateField(default=timezone.now)
    cuidados_especiais = models.TextField(blank=True)
    bebe_id = models.CharField(max_length=50)

    def __str__(self):
        """Retorna representação legível da medicação."""
        return f"{self.nome} ({self.bebe_id})"


class Lembrete(models.Model):
    """
    Lembretes associados a uma medicação.

    Cada lembrete contém:
    - Um horário específico.
    - Canal preferido (notificações futuras).
    - Tolerância de atraso para o lembrete.
    """

    medicacao = models.ForeignKey(
        Medicacao, on_delete=models.CASCADE, related_name="lembretes"
    )
    horario = models.TimeField()
    canal_preferido = models.CharField(max_length=20, default="APP")
    tolerancia_minutos = models.IntegerField(default=30)

    def __str__(self):
        return f"Lembrete de {self.medicacao.nome} às {self.horario}"


class Estoque(models.Model):
    """
    Controle de estoque para uma única medicação (OneToOne).

    Armazena:
    - Quantidade atual em ml.
    - Consumo diário estimado.
    - Alerta automático se faltar menos de 3 dias de uso.
    """

    medicacao = models.OneToOneField(
        Medicacao, on_delete=models.CASCADE, related_name="estoque"
    )
    quantidade_total_ml = models.FloatField()
    consumo_diario_estimado_ml = models.FloatField()
    alerta_baixo_estoque = models.BooleanField(default=False)

    def atualizar_alerta(self):
        """
        Atualiza o alerta de estoque com base no consumo diário.

        Regras:
        - Se faltarem 3 dias ou menos → alerta = True
        - Caso contrário → alerta = False
        """
        if self.consumo_diario_estimado_ml > 0:
            dias_restantes = (
                self.quantidade_total_ml / self.consumo_diario_estimado_ml
            )
            self.alerta_baixo_estoque = dias_restantes <= 3
        else:
            self.alerta_baixo_estoque = False

        self.save()

    def __str__(self):
        return f"Estoque de {self.medicacao.nome}"


class RegistroAdministracao(models.Model):
    """
    Registra eventos relacionados à administração da medicação.

    Tipos de status:
    - TOMEI / ESQUECI / RECUSEI / VOMITOU (ações humanas)
    - SISTEMA_ADD / SISTEMA_EDIT / ESTOQUE_UP (ações internas)

    Usado tanto para log de auditoria quanto para feedback diário dos pais.
    """

    OPCOES = [
        ("TOMEI", "Tomei/Dei a medicação"),
        ("ESQUECI", "Esqueci"),
        ("RECUSEI", "Bebê recusou"),
        ("VOMITOU", "Vomitou após tomar"),

        # Ações automáticas do sistema
        ("SISTEMA_ADD", "✨ Cadastro Novo"),
        ("SISTEMA_EDIT", "✏️ Edição de Dados"),
        ("ESTOQUE_UP", "📦 Atualização de Estoque"),
    ]

    medicacao = models.ForeignKey(
        Medicacao, on_delete=models.CASCADE, related_name="registros"
    )
    horario_registro = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=OPCOES)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        """Retorna entrada no histórico de registro."""
        return f"{self.medicacao.nome} - {self.status} ({self.horario_registro.date()})"
