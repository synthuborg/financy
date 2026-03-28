from decimal import Decimal

from django import forms

from .models import Account, Category, Goal, MonthlyBudgetConfig, Transaction


INPUT_CSS = (
    'w-full bg-zinc-900/50 border border-zinc-700 text-white rounded-xl px-4 py-3 text-sm '
    'focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent '
    'placeholder-zinc-500 transition-all'
)
SELECT_CSS = (
    'w-full bg-zinc-900 border border-zinc-700 text-white rounded-xl px-4 py-3 text-sm '
    'focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent '
    'transition-all'
)


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['valor', 'data', 'tipo', 'descricao', 'categoria', 'conta']
        widgets = {
            'valor': forms.NumberInput(attrs={
                'class': INPUT_CSS,
                'placeholder': '0,00',
                'step': '0.01',
                'min': '0.01',
            }),
            'data': forms.DateInput(attrs={
                'class': INPUT_CSS,
                'type': 'date',
            }),
            'tipo': forms.Select(attrs={'class': SELECT_CSS}),
            'descricao': forms.TextInput(attrs={
                'class': INPUT_CSS,
                'placeholder': 'Ex: Salário, Aluguel, Mercado...',
            }),
            'categoria': forms.Select(attrs={'class': SELECT_CSS}),
            'conta': forms.Select(attrs={'class': SELECT_CSS}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['categoria'].queryset = Category.objects.filter(usuario=user)
            self.fields['categoria'].required = False
            self.fields['conta'].queryset = Account.objects.filter(usuario=user)
            self.fields['conta'].required = False
        self.fields['categoria'].empty_label = '— Sem categoria —'
        self.fields['conta'].empty_label = '— Sem conta —'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['nome', 'tipo', 'keywords']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': INPUT_CSS,
                'placeholder': 'Ex: Alimentação, Transporte, Salário...',
            }),
            'tipo': forms.Select(attrs={'class': SELECT_CSS}),
            'keywords': forms.TextInput(attrs={
                'class': INPUT_CSS,
                'placeholder': 'Ex: mercado, ifood, supermercado',
            }),
        }
        help_texts = {
            'keywords': 'Palavras-chave separadas por vírgula para auto-categorização de extratos.',
        }


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['nome', 'tipo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': INPUT_CSS,
                'placeholder': 'Ex: Nubank, Carteira, Bradesco...',
            }),
            'tipo': forms.Select(attrs={'class': SELECT_CSS}),
        }


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['titulo', 'valor_alvo', 'prazo', 'categoria']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': INPUT_CSS,
                'placeholder': 'Ex: Reserva de Emergência, Viagem, Notebook...',
            }),
            'valor_alvo': forms.NumberInput(attrs={
                'class': INPUT_CSS,
                'placeholder': '0,00',
                'step': '0.01',
                'min': '0.01',
            }),
            'prazo': forms.DateInput(attrs={
                'class': INPUT_CSS,
                'type': 'date',
            }),
            'categoria': forms.Select(attrs={'class': SELECT_CSS}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['categoria'].queryset = Category.objects.filter(usuario=user)
        self.fields['categoria'].required = False
        self.fields['categoria'].empty_label = '— Sem categoria —'
        self.fields['prazo'].required = False


class GoalAddProgressForm(forms.Form):
    valor = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={
            'class': INPUT_CSS,
            'placeholder': '0,00',
            'step': '0.01',
            'min': '0.01',
        }),
        label='Valor do Depósito',
    )


class MonthlyBudgetConfigForm(forms.ModelForm):
    class Meta:
        model = MonthlyBudgetConfig
        fields = ['renda_mensal', 'limite_percentual', 'alertas_ativos']
        widgets = {
            'renda_mensal': forms.NumberInput(attrs={
                'class': INPUT_CSS,
                'placeholder': 'Ex: 5000,00',
                'step': '0.01',
                'min': '0.01',
            }),
            'limite_percentual': forms.NumberInput(attrs={
                'class': INPUT_CSS,
                'placeholder': 'Ex: 80',
                'step': '0.01',
                'min': '1',
                'max': '100',
            }),
            'alertas_ativos': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 rounded border-zinc-700 bg-zinc-900 text-emerald-500 focus:ring-emerald-500',
            }),
        }
        labels = {
            'renda_mensal': 'Renda Mensal',
            'limite_percentual': 'Percentual Máximo de Gastos (%)',
            'alertas_ativos': 'Ativar alertas de orçamento no Telegram',
        }


class ReportFilterForm(forms.Form):
    data_inicio = forms.DateField(
        label='Data Início',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': INPUT_CSS,
        }),
    )
    data_fim = forms.DateField(
        label='Data Fim',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': INPUT_CSS,
        }),
    )
    formato = forms.ChoiceField(
        label='Formato',
        choices=[('pdf', 'PDF'), ('excel', 'Excel')],
        widget=forms.Select(attrs={'class': SELECT_CSS}),
    )

    def clean(self):
        cleaned = super().clean()
        data_inicio = cleaned.get('data_inicio')
        data_fim = cleaned.get('data_fim')
        if data_inicio and data_fim and data_inicio > data_fim:
            raise forms.ValidationError(
                'A data de início não pode ser maior que a data fim.'
            )
        return cleaned


ALLOWED_IMPORT_EXTENSIONS = {'csv', 'ofx', 'pdf'}


class ImportStatementForm(forms.Form):
    arquivo = forms.FileField(
        label='Arquivo',
        widget=forms.ClearableFileInput(attrs={
            'class': INPUT_CSS,
            'accept': '.csv,.ofx,.pdf',
        }),
    )
    conta = forms.ModelChoiceField(
        queryset=Account.objects.none(),
        label='Conta',
        widget=forms.Select(attrs={'class': SELECT_CSS}),
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['conta'].queryset = Account.objects.filter(usuario=user)

    def clean_arquivo(self):
        arquivo = self.cleaned_data['arquivo']
        ext = arquivo.name.rsplit('.', 1)[-1].lower() if '.' in arquivo.name else ''
        if ext not in ALLOWED_IMPORT_EXTENSIONS:
            raise forms.ValidationError(
                'Formato não suportado. Envie um arquivo .csv, .ofx ou .pdf.'
            )
        return arquivo
