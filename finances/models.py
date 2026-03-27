from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categorias')
    keywords = models.TextField(
        blank=True,
        default='',
        help_text='Palavras-chave separadas por vírgula para auto-categorização',
    )

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        unique_together = ['nome', 'usuario']

    def __str__(self):
        return f'{self.nome} ({self.get_tipo_display()})'

    def get_keywords_list(self):
        """Retorna lista de keywords em lowercase para comparação."""
        if not self.keywords:
            return []
        return [k.strip().lower() for k in self.keywords.split(',') if k.strip()]


class Account(models.Model):
    TIPO_CHOICES = [
        ('conta_corrente', 'Conta Corrente'),
        ('carteira', 'Carteira'),
        ('cartao_credito', 'Cartão de Crédito'),
    ]
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='conta_corrente')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contas')

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        unique_together = ['nome', 'usuario']

    def __str__(self):
        return f'{self.nome} ({self.get_tipo_display()})'


class Transaction(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    valor = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    data = models.DateField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    descricao = models.CharField(max_length=255)
    categoria = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transacoes',
    )
    conta = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transacoes',
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transacoes')

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-data', '-id']
        constraints = [
            models.CheckConstraint(
                check=models.Q(valor__gt=0),
                name='transaction_valor_positivo',
            )
        ]

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.descricao} - R${self.valor}'


class Goal(models.Model):
    titulo = models.CharField(max_length=200)
    valor_alvo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    valor_atual = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    prazo = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metas')
    categoria = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='metas',
    )

    class Meta:
        verbose_name = 'Meta'
        verbose_name_plural = 'Metas'
        ordering = ['prazo', 'titulo']

    def __str__(self):
        return f'{self.titulo} ({self.percentual_concluido}%)'

    @property
    def percentual_concluido(self) -> int:
        valor_alvo = Decimal(str(self.valor_alvo))
        if valor_alvo <= 0:
            return 0
        pct = int((Decimal(str(self.valor_atual)) / valor_alvo) * 100)
        return min(pct, 100)

    @property
    def saldo_restante(self) -> Decimal:
        return max(Decimal(str(self.valor_alvo)) - Decimal(str(self.valor_atual)), Decimal('0.00'))
