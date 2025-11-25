from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Medicacao, Lembrete, Estoque, RegistroAdministracao
from .forms import MedicacaoForm, LembreteForm, EstoqueForm, RegistroForm

"""
Este módulo contém todas as views do app 'medicacoes'.

Ele inclui:
- Sistema híbrido de login (Usuários Fake para demonstração + Login real do Django/Admin)
- Área exclusiva para pais (mockup demonstrativo)
- Área administrativa real (CRUD completo para medicações, lembretes, estoque e registros)
"""


# ================================================================
# === DADOS MOCKUP (Usuários Fakes para Demonstração do Sistema) ===
# ================================================================
USUARIOS_FAKE = {
    "joao": {
        "senha": "123",
        "nome_exibicao": "João (Pai)",
        "remedios": [
            {"nome": "Dipirona", "dosagem": "15 gotas", "horario": "08:00"},
            {"nome": "Vitamina C", "dosagem": "1 comprimido", "horario": "10:00"}
        ]
    },
    "maria": {
        "senha": "abc",
        "nome_exibicao": "Maria (Mãe)",
        "remedios": [
            {"nome": "Insulina", "dosagem": "2 unidades", "horario": "12:00"},
            {"nome": "Omeprazol", "dosagem": "1 cápsula", "horario": "07:00"}
        ]
    }
}


# ==============================================
# === LOGIN HÍBRIDO (Fake + Autenticação Real) ===
# ==============================================
def login_view(request):
    """
    Autentica o usuário de duas formas:
    1. Primeiro tenta autenticação via usuário 'fake' para a área dos pais (demo).
    2. Se falhar, tenta autenticação real usando o sistema padrão do Django.
    """
    if request.method == 'POST':
        usuario_form = request.POST.get('username')
        senha_form = request.POST.get('password')

        # --- Autenticação Fake ---
        if usuario_form in USUARIOS_FAKE and senha_form == USUARIOS_FAKE[usuario_form]['senha']:
            request.session['usuario_fake'] = usuario_form
            return redirect('area_pais')

        # --- Autenticação Real (Admin) ---
        user = authenticate(request, username=usuario_form, password=senha_form)
        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, 'Usuário ou senha incorretos.')

    return render(request, 'registration/login.html')


def logout_view(request):
    """
    Realiza logout tanto do Django quanto da sessão fake.
    Limpa mensagens pendentes para evitar que elas reapareçam após logout.
    """
    storage = messages.get_messages(request)
    for _ in storage:  # limpa mensagens pendentes
        pass

    logout(request)
    request.session.flush()
    return redirect('login')


# ============================================
# === ÁREA DOS PAIS (Mockup de Demonstração) ===
# ============================================
def area_pais(request):
    """
    Exibe um painel simplificado para os pais, baseado em dados falsos.
    Só acessível enquanto houver usuário fake ativo na sessão.
    """
    usuario_key = request.session.get('usuario_fake')

    if not usuario_key or usuario_key not in USUARIOS_FAKE:
        return redirect('login')

    dados_usuario = USUARIOS_FAKE[usuario_key]

    return render(request, 'medicacoes/dashboard_pais.html', {
        'usuario': dados_usuario,
        'remedios': dados_usuario['remedios']
    })


def simular_registro_pai(request):
    """
    Simula uma ação realizada pelos pais (tomar medicamento ou editar).
    Registra no sistema real via Modelo RegistroAdministracao.
    Útil para demonstração de uso real.
    """
    usuario_key = request.session.get('usuario_fake')
    remedio_nome = request.GET.get('remedio')
    acao = request.GET.get('acao')

    if usuario_key and remedio_nome:
        med_real = Medicacao.objects.first()

        if med_real:
            if acao == 'editou':
                status_code = 'SISTEMA_EDIT'
                msg_admin = f"PAI/MÃE ({USUARIOS_FAKE[usuario_key]['nome_exibicao']}) alterou configurações de: {remedio_nome}"
                msg_pai = f"Você editou as informações de {remedio_nome} com sucesso!"
            else:
                status_code = 'TOMEI'
                msg_admin = f"PAI/MÃE ({USUARIOS_FAKE[usuario_key]['nome_exibicao']}) registrou dose tomada: {remedio_nome}"
                msg_pai = f"Dose de {remedio_nome} confirmada!"

            RegistroAdministracao.objects.create(
                medicacao=med_real,
                status=status_code,
                observacoes=msg_admin
            )

            messages.success(request, msg_pai)

    return redirect('area_pais')


# ============================================
# === ÁREA REAL DO SISTEMA (Admin Autenticado) ===
# ============================================

@login_required
def dashboard(request):
    """
    Dashboard principal do Admin com métricas gerais do sistema.
    """
    context = {
        'total_medicacoes': Medicacao.objects.count(),
        'total_lembretes': Lembrete.objects.count(),
        'baixo_estoque': Estoque.objects.filter(alerta_baixo_estoque=True).count(),
    }
    return render(request, "dashboard.html", context)


# ---------------------------
# === CRUD de Medicações ===
# ---------------------------
@login_required
def listar_medicacoes(request):
    """Lista todas as medicações cadastradas."""
    medicacoes = Medicacao.objects.all().order_by('-data_inicio')
    return render(request, "medicacoes/listar.html", {'medicacoes': medicacoes})


@login_required
def criar_medicacao(request):
    """Cria nova medicação e registra o evento no histórico."""
    if request.method == 'POST':
        form = MedicacaoForm(request.POST)
        if form.is_valid():
            medicacao = form.save()
            RegistroAdministracao.objects.create(
                medicacao=medicacao,
                status='SISTEMA_ADD',
                observacoes=f"Nova medicação cadastrada por {request.user.username}"
            )
            messages.success(request, 'Medicação criada com sucesso!')
            return redirect('listar_medicacoes')
    else:
        form = MedicacaoForm()

    return render(request, "medicacoes/form.html", {'form': form, 'titulo': 'Nova Medicação'})


@login_required
def editar_medicacao(request, id):
    """Edita uma medicação existente."""
    medicacao = get_object_or_404(Medicacao, id=id)

    if request.method == 'POST':
        form = MedicacaoForm(request.POST, instance=medicacao)
        if form.is_valid():
            form.save()
            RegistroAdministracao.objects.create(
                medicacao=medicacao,
                status='SISTEMA_EDIT',
                observacoes=f"Dados alterados por {request.user.username}"
            )
            messages.success(request, 'Medicação atualizada!')
            return redirect('listar_medicacoes')
    else:
        form = MedicacaoForm(instance=medicacao)

    return render(request, "medicacoes/form.html", {
        'form': form,
        'titulo': f'Editar {medicacao.nome}'
    })


# -------------------------
# === CRUD de Lembretes ===
# -------------------------
@login_required
def listar_lembretes(request):
    """Lista todos os lembretes cadastrados."""
    lembretes = Lembrete.objects.all().order_by('horario')
    return render(request, "lembretes/listar.html", {'lembretes': lembretes})


@login_required
def criar_lembrete(request):
    """Cria um novo lembrete vinculado a uma medicação."""
    if request.method == 'POST':
        form = LembreteForm(request.POST)
        if form.is_valid():
            lembrete = form.save()
            RegistroAdministracao.objects.create(
                medicacao=lembrete.medicacao,
                status='SISTEMA_ADD',
                observacoes=f"Novo lembrete definido para {lembrete.horario}"
            )
            messages.success(request, 'Lembrete criado!')
            return redirect('listar_lembretes')
    else:
        form = LembreteForm()

    return render(request, "medicacoes/form.html", {'form': form, 'titulo': 'Novo Lembrete'})


@login_required
def editar_lembrete(request, id):
    """Edita um lembrete existente."""
    lembrete = get_object_or_404(Lembrete, id=id)

    if request.method == 'POST':
        form = LembreteForm(request.POST, instance=lembrete)
        if form.is_valid():
            form.save()
            RegistroAdministracao.objects.create(
                medicacao=lembrete.medicacao,
                status='SISTEMA_EDIT',
                observacoes=f"Horário do lembrete alterado para {lembrete.horario}"
            )
            messages.success(request, 'Lembrete atualizado!')
            return redirect('listar_lembretes')
    else:
        form = LembreteForm(instance=lembrete)

    return render(request, "medicacoes/form.html", {'form': form, 'titulo': 'Editar Lembrete'})


# -------------------------
# === CRUD de Estoque ===
# -------------------------
@login_required
def listar_estoque(request):
    """
    Lista todos os itens de estoque.
    Atualiza automaticamente o status de alerta de cada item.
    """
    estoques = Estoque.objects.all()
    for item in estoques:
        item.atualizar_alerta()

    return render(request, "estoques/listar.html", {'estoques': estoques})


@login_required
def criar_estoque(request):
    """Cria um novo registro de estoque e ativa alerta, se necessário."""
    if request.method == 'POST':
        form = EstoqueForm(request.POST)
        if form.is_valid():
            estoque = form.save(commit=False)
            estoque.atualizar_alerta()
            estoque.save()

            RegistroAdministracao.objects.create(
                medicacao=estoque.medicacao,
                status='ESTOQUE_UP',
                observacoes=f"Estoque iniciado: {estoque.quantidade_total_ml}ml"
            )

            messages.success(request, 'Item adicionado ao estoque!')
            return redirect('listar_estoque')
    else:
        form = EstoqueForm()

    return render(request, "medicacoes/form.html", {'form': form, 'titulo': 'Novo Item de Estoque'})


@login_required
def editar_estoque(request, id):
    """Edita um item de estoque existente."""
    item = get_object_or_404(Estoque, id=id)

    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=item)
        if form.is_valid():
            estoque = form.save(commit=False)
            estoque.atualizar_alerta()
            estoque.save()

            RegistroAdministracao.objects.create(
                medicacao=estoque.medicacao,
                status='ESTOQUE_UP',
                observacoes=f"Estoque atualizado para: {estoque.quantidade_total_ml}ml"
            )

            messages.success(request, 'Estoque atualizado!')
            return redirect('listar_estoque')
    else:
        form = EstoqueForm(instance=item)

    return render(request, "medicacoes/form.html", {
        'form': form,
        'titulo': f'Editar Estoque: {item.medicacao.nome}'
    })


# -----------------------------------------
# === Registros de Administração (Histórico)
# -----------------------------------------
@login_required
def listar_registros(request):
    """Lista todos os registros realizados (sistema + pais)."""
    registros = RegistroAdministracao.objects.all().order_by('-horario_registro')
    return render(request, "registros/listar.html", {'registros': registros})
