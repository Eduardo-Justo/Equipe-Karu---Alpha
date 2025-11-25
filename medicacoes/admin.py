from django.contrib import admin
from django.contrib import admin
from .models import Medicacao, Lembrete, RegistroAdministracao, Estoque

admin.site.register(Medicacao)
admin.site.register(Lembrete)
admin.site.register(RegistroAdministracao)
admin.site.register(Estoque)