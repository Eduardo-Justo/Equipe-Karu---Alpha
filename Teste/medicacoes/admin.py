from django.contrib import admin
from django.utils.html import format_html
from .models import Medicacao, Lembrete, RegistroAdministracao, Estoque

# ---------------------------------------------------------
# Configurações gerais da interface administrativa do Django
# ---------------------------------------------------------
admin.site.site_header = "Karu Administração"
admin.site.site_title = "Karu Admin"
admin.site.index_title = "Bem-vindo ao Gerenciamento Karu"


# ============================
# INLINES
# ============================
# Os inlines permitem editar objetos relacionados dentro de outros
class LembreteInline(admin.TabularInline):
    """Inline para exibir e editar lembretes dentro da tela da Medicação."""
    model = Lembrete
    extra = 0  # Evita adicionar linhas extras vazias por padrão


class EstoqueInline(admin.StackedInline):
    """Inline para permitir a edição do estoque diretamente na Medicação."""
    model = Estoque
    can_delete = False
    verbose_name_plural = 'Estoque Associado'


# ============================
# MEDICAÇÃO
# ============================
@admin.register(Medicacao)
class MedicacaoAdmin(admin.ModelAdmin):
    """Configurações da interface administrativa para o modelo Medicação."""

    # Colunas exibidas na tabela da lista
    list_display = ('nome', 'dosagem', 'frequencia', 'via', 'bebe_id', 'status_estoque')

    # Campos utilizáveis na busca
    search_fields = ('nome', 'bebe_id', 'cuidados_especiais')

    # Filtros na barra lateral direita
    list_filter = ('via', 'data_inicio')

    # Inclusão dos inlines configurados acima
    inlines = [LembreteInline, EstoqueInline]

    # Organização dos grupos de campos na edição
    fieldsets = (
        ('Dados Principais', {
            'fields': ('nome', 'bebe_id', 'data_inicio')
        }),
        ('Posologia', {
            'fields': ('dosagem', 'frequencia', 'via', 'duracao_dias')
        }),
        ('Outros', {
            'fields': ('cuidados_especiais',),
            'classes': ('collapse',),  # Oculta para deixar a tela mais limpa
        }),
    )

    def status_estoque(self, obj):
        """
        Exibe a situação do estoque com ícones coloridos.
        Mostra 'BAIXO' em vermelho se houver alerta,
        ou 'OK' em verde caso contrário.
        """
        if hasattr(obj, 'estoque'):
            if obj.estoque.alerta_baixo_estoque:
                return format_html('<span style="color: red; font-weight: bold;">⚠ BAIXO</span>')
            return format_html('<span style="color: green;">✔ OK</span>')
        return "-"

    status_estoque.short_description = "Situação do Estoque"


# ============================
# LEMBRETE
# ============================
@admin.register(Lembrete)
class LembreteAdmin(admin.ModelAdmin):
    """Administração do modelo Lembrete."""
    list_display = ('medicacao', 'horario', 'canal_preferido', 'tolerancia_minutos')
    list_filter = ('canal_preferido', 'horario')

    # Permite buscar lembretes pelo nome da medicação
    search_fields = ('medicacao__nome',)


# ============================
# ESTOQUE
# ============================
@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    """Painel administrativo do modelo Estoque."""
    list_display = ('medicacao', 'quantidade_total_ml', 'consumo_diario_estimado_ml', 'visual_alerta')
    list_filter = ('alerta_baixo_estoque',)

    # Ações em massa disponíveis na interface
    actions = ['recalcular_alertas']

    def visual_alerta(self, obj):
        """
        Retorna o valor booleano para exibir o ícone padrão do Django.
        True = ícone verde; False = ícone vermelho.
        """
        return obj.alerta_baixo_estoque

    visual_alerta.boolean = True
    visual_alerta.short_description = "Alerta Ativo?"

    @admin.action(description='Recalcular alertas selecionados')
    def recalcular_alertas(self, request, queryset):
        """
        Ação em massa que recalcula o alerta de baixo estoque
        para todos os itens selecionados pelo administrador.
        """
        count = 0
        for estoque in queryset:
            estoque.atualizar_alerta()
            count += 1
        self.message_user(request, f"{count} estoques atualizados.")


# ============================
# REGISTRO DE ADMINISTRAÇÃO
# ============================
@admin.register(RegistroAdministracao)
class RegistroAdministracaoAdmin(admin.ModelAdmin):
    """Administração dos registros de administração das medicações."""
    list_display = ('medicacao', 'status_colorido', 'horario_registro', 'observacoes_curtas')
    list_filter = ('status', 'horario_registro', 'medicacao')
    date_hierarchy = 'horario_registro'  # Navegação por data no topo

    def status_colorido(self, obj):
        """
        Exibe o status com cores diferentes para facilitar a visualização:
        - TOMEI: verde
        - ESQUECI: laranja
        - RECUSEI: vermelho
        - VOMITOU: roxo
        """
        cores = {
            'TOMEI': 'green',
            'ESQUECI': 'orange',
            'RECUSEI': 'red',
            'VOMITOU': 'purple',
        }
        cor = cores.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            cor,
            obj.get_status_display()
        )

    status_colorido.short_description = "Status"

    def observacoes_curtas(self, obj):
        """
        Mostra apenas os primeiros 50 caracteres da observação.
        Evita poluição visual nos registros da lista.
        """
        return obj.observacoes[:50] + "..." if obj.observacoes else "-"

    observacoes_curtas.short_description = "Obs"
