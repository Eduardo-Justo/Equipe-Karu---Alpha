from django import forms
from .models import Medicacao, Lembrete, Estoque, RegistroAdministracao

# NOTE QUE AQUI NÃO TEM "from .forms import ..."
# Isso é correto: este arquivo *define* os forms, não os importa.


class MedicacaoForm(forms.ModelForm):
    """
    Formulário para criação e edição de objetos do modelo Medicacao.

    Utiliza widgets personalizados para datas e textos longos.
    """
    class Meta:
        model = Medicacao
        fields = '__all__'
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),  # Exibe calendário nativo
            'cuidados_especiais': forms.Textarea(attrs={'rows': 3}),  # Área de texto reduzida
        }


class LembreteForm(forms.ModelForm):
    """
    Formulário responsável pela criação/edição de lembretes associados às medicações.

    Inclui seleção de horário com widget HTML5.
    """
    class Meta:
        model = Lembrete
        fields = ['medicacao', 'horario', 'canal_preferido', 'tolerancia_minutos']
        widgets = {
            'horario': forms.TimeInput(attrs={'type': 'time'}),  # Widget de horário
        }


class EstoqueForm(forms.ModelForm):
    """
    Formulário para gerenciar dados de Estoque de uma medicação.

    Usado para registrar quantidade total e consumo diário estimado.
    """
    class Meta:
        model = Estoque
        fields = ['medicacao', 'quantidade_total_ml', 'consumo_diario_estimado_ml']


class RegistroForm(forms.ModelForm):
    """
    Formulário utilizado para registrar administrações de medicamentos,
    incluindo status e observações curtas.
    """
    class Meta:
        model = RegistroAdministracao
        fields = ['medicacao', 'status', 'observacoes']
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 2}),  # Caixa de texto compacta
        }