# tudo isso é implementação de histórico

class MedicacaoHistorico(models.Model):
    """
    Armazena o histórico de alterações feitas em uma instância de Medicacao.

    Cada entrada registra:
    - Qual campo foi alterado
    - O valor antigo e o novo
    - Qual usuário fez a alteração
    - Quando a alteração ocorreu
    """

    medicacao = models.ForeignKey(
        Medicacao, 
        on_delete=models.CASCADE, 
        related_name='historico'
    )
    usuario = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True
    )
    campo = models.CharField(max_length=100)
    valor_antigo = models.TextField(null=True, blank=True)
    valor_novo = models.TextField(null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Retorna uma representação legível do registro de histórico."""
        return f"{self.medicacao.nome} — {self.campo} alterado"


# =====================================================================
# EXEMPLO DE REGISTRO DE ALTERAÇÃO (código demonstrativo)
# =====================================================================

# Obtém a medicação que será alterada
m = Medicacao.objects.get(id=id)

# Exemplo manual de detecção de mudança — comparação antes da edição
# Aqui só registramos uma alteração se o valor realmente mudou.
if m.nome != request.POST['nome']:
    MedicacaoHistorico.objects.create(
        medicacao=m,
        usuario=request.user,
        campo='nome',
        valor_antigo=m.nome,
        valor_novo=request.POST['nome']
    )

# Atualiza o objeto após registrar o histórico
m.nome = request.POST['nome']
m.save()

# Obtém o histórico ordenado por data mais recente
historico = m.historico.order_by('-data')


# =====================================================================
# EXEMPLO DE USO NO TEMPLATE (HTML)
# =====================================================================
#
# {% for h in historico %}
#     <p>
#         <strong>{{ h.data }} – {{ h.usuario.username }}</strong><br>
#         {{ h.campo }}: "{{ h.valor_antigo }}" → "{{ h.valor_novo }}"
#     </p>
# {% endfor %}
#
# =====================================================================
