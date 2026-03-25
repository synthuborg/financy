import random
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction as db_transaction

from finances.models import Account, Category, Goal, Transaction


# ---------------------------------------------------------------------------
# Dados de referência
# ---------------------------------------------------------------------------

CATEGORIAS_SAIDA = [
    {"nome": "Alimentação", "keywords": "mercado,supermercado,padaria,restaurante,ifood,delivery"},
    {"nome": "Transporte", "keywords": "uber,99,combustível,gasolina,bus,metro,estacionamento"},
    {"nome": "Moradia", "keywords": "aluguel,condomínio,iptu,água,luz,energia,gás,internet"},
    {"nome": "Saúde", "keywords": "farmácia,médico,consulta,exame,plano de saúde,academia"},
    {"nome": "Lazer", "keywords": "cinema,teatro,netflix,spotify,streaming,show,viagem"},
    {"nome": "Vestuário", "keywords": "roupa,sapato,calçado,acessório,loja"},
    {"nome": "Educação", "keywords": "curso,faculdade,escola,livro,material"},
    {"nome": "Pets", "keywords": "pet shop,ração,veterinário,banho,tosa"},
    {"nome": "Cartão de Crédito", "keywords": "fatura,cartão"},
    {"nome": "Outros Gastos", "keywords": ""},
]

CATEGORIAS_ENTRADA = [
    {"nome": "Salário", "keywords": "salário,pagamento,folha"},
    {"nome": "Freelance", "keywords": "freelance,projeto,consultoria,serviço"},
    {"nome": "Investimentos", "keywords": "rendimento,dividendo,juros,cdb,fundo,ação"},
    {"nome": "Outros Rendimentos", "keywords": ""},
]

CONTAS = [
    {"nome": "Nubank", "tipo": "conta_corrente"},
    {"nome": "Bradesco", "tipo": "conta_corrente"},
    {"nome": "Cartão Nubank", "tipo": "cartao_credito"},
    {"nome": "Cartão Inter", "tipo": "cartao_credito"},
    {"nome": "Carteira", "tipo": "carteira"},
]

TRANSACOES_SAIDA = [
    ("Mercado Semanal", "Alimentação", 120, 350),
    ("iFood – Delivery", "Alimentação", 30, 80),
    ("Aluguel", "Moradia", 900, 900),
    ("Conta de Luz", "Moradia", 80, 200),
    ("Internet Fibra", "Moradia", 99, 99),
    ("Plano de Saúde", "Saúde", 350, 350),
    ("Farmácia", "Saúde", 20, 90),
    ("Academia", "Saúde", 70, 120),
    ("Uber", "Transporte", 15, 60),
    ("Combustível", "Transporte", 80, 250),
    ("Netflix", "Lazer", 39, 39),
    ("Spotify", "Lazer", 19, 19),
    ("Cinema", "Lazer", 30, 80),
    ("Restaurante", "Alimentação", 40, 120),
    ("Padaria", "Alimentação", 10, 30),
    ("Supermercado Extra", "Alimentação", 60, 180),
    ("Roupa/Vestuário", "Vestuário", 60, 300),
    ("Curso Online", "Educação", 50, 200),
    ("Consulta Médica", "Saúde", 80, 300),
    ("Pet Shop", "Pets", 30, 100),
    ("Gasolina", "Transporte", 80, 160),
    ("Estacionamento", "Transporte", 5, 20),
    ("Bar / Happy Hour", "Lazer", 30, 80),
    ("Pastelaria", "Alimentação", 10, 25),
    ("Material Escritório", "Outros Gastos", 15, 60),
    ("Fatura Cartão Nubank", "Cartão de Crédito", 300, 900),
    ("Fatura Cartão Inter", "Cartão de Crédito", 200, 600),
]

TRANSACOES_ENTRADA = [
    ("Salário", "Salário", 3000, 7000),
    ("Freelance – Projeto Web", "Freelance", 500, 2000),
    ("Rendimento CDB", "Investimentos", 50, 300),
    ("Dividendos", "Investimentos", 30, 200),
    ("13º Salário", "Salário", 2000, 5000),
    ("Bônus", "Salário", 500, 2000),
    ("Venda de Produto", "Outros Rendimentos", 100, 500),
]

METAS = [
    {"titulo": "Reserva de Emergência", "valor_alvo": Decimal("15000.00"), "meses": 12},
    {"titulo": "Viagem de Férias", "valor_alvo": Decimal("5000.00"), "meses": 8},
    {"titulo": "Novo Notebook", "valor_alvo": Decimal("3500.00"), "meses": 6},
    {"titulo": "Curso de Especialização", "valor_alvo": Decimal("2000.00"), "meses": 4},
    {"titulo": "Reforma de Apartamento", "valor_alvo": Decimal("8000.00"), "meses": 10},
]


class Command(BaseCommand):
    help = "Popula o banco com dados demo (categorias, contas, transações, metas)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Apaga os dados do usuário alvo antes de re-popular.",
        )
        parser.add_argument(
            "--user",
            type=str,
            default=None,
            help="Username do usuário alvo. Se omitido, cria 'demo'.",
        )
        parser.add_argument(
            "--meses",
            type=int,
            default=6,
            help="Meses de histórico a gerar (default: 6).",
        )

    @db_transaction.atomic
    def handle(self, *args, **options):
        meses = max(1, min(options["meses"], 24))
        username = options["user"]

        if username:
            try:
                usuario = User.objects.get(username=username)
                self.stdout.write(f"  Usuário encontrado: {usuario.username}")
            except User.DoesNotExist:
                raise CommandError(
                    f"Usuário '{username}' não existe. "
                    "Crie o usuário ou omita --user para criar 'demo'."
                )
        else:
            usuario, criado = User.objects.get_or_create(
                username="demo",
                defaults={
                    "email": "demo@smartfinancy.com",
                    "first_name": "Demo",
                    "last_name": "SmartFinancy",
                },
            )
            if criado:
                usuario.set_password("demo1234")
                usuario.save()
                self.stdout.write(f"  Usuário criado: {usuario.username}")
            else:
                self.stdout.write(f"  Usuário existente: {usuario.username}")

        if options["flush"]:
            self._flush(usuario)
            self.stdout.write(self.style.WARNING(
                f"  Dados de '{usuario.username}' apagados."
            ))

        categorias = self._seed_categorias(usuario)
        self.stdout.write(self.style.SUCCESS(
            f"  ✓ {len(categorias)} categorias"
        ))

        contas = self._seed_contas(usuario)
        self.stdout.write(self.style.SUCCESS(
            f"  ✓ {len(contas)} contas"
        ))

        transacoes = self._seed_transacoes(
            usuario, categorias, contas, meses
        )
        self.stdout.write(self.style.SUCCESS(
            f"  ✓ {len(transacoes)} transações ({meses} meses)"
        ))

        metas = self._seed_metas(usuario, categorias)
        self.stdout.write(self.style.SUCCESS(
            f"  ✓ {len(metas)} metas"
        ))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Seed concluído!"))
        self.stdout.write(f"  Usuário: {usuario.username}")
        self.stdout.write("")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _flush(self, usuario):
        Transaction.objects.filter(usuario=usuario).delete()
        Goal.objects.filter(usuario=usuario).delete()
        Account.objects.filter(usuario=usuario).delete()
        Category.objects.filter(usuario=usuario).delete()

    def _seed_categorias(self, usuario):
        categorias = {}
        for dados in CATEGORIAS_SAIDA:
            cat, _ = Category.objects.get_or_create(
                nome=dados["nome"],
                usuario=usuario,
                defaults={
                    "tipo": "saida",
                    "keywords": dados["keywords"],
                },
            )
            categorias[dados["nome"]] = cat

        for dados in CATEGORIAS_ENTRADA:
            cat, _ = Category.objects.get_or_create(
                nome=dados["nome"],
                usuario=usuario,
                defaults={
                    "tipo": "entrada",
                    "keywords": dados["keywords"],
                },
            )
            categorias[dados["nome"]] = cat

        return categorias

    def _seed_contas(self, usuario):
        contas = {}
        for dados in CONTAS:
            conta, _ = Account.objects.get_or_create(
                nome=dados["nome"],
                usuario=usuario,
                defaults={"tipo": dados["tipo"]},
            )
            contas[dados["nome"]] = conta
        return contas

    def _seed_transacoes(self, usuario, categorias, contas, meses):
        hoje = date.today()
        contas_correntes = [
            c for c in contas.values() if c.tipo == "conta_corrente"
        ]
        contas_credito = [
            c for c in contas.values() if c.tipo == "cartao_credito"
        ]
        todas_contas = list(contas.values())
        criadas = []

        # Salário mensal garantido
        cat_salario = categorias.get("Salário")
        conta_principal = (
            contas_correntes[0] if contas_correntes else todas_contas[0]
        )

        for m in range(meses):
            ano = hoje.year
            mes = hoje.month - m
            while mes <= 0:
                mes += 12
                ano -= 1

            data_salario = date(ano, mes, 5)
            valor = Decimal(
                str(random.randint(400000, 700000))
            ) / 100

            t, criado = Transaction.objects.get_or_create(
                usuario=usuario,
                descricao="Salário",
                data=data_salario,
                defaults={
                    "tipo": "entrada",
                    "valor": valor,
                    "categoria": cat_salario,
                    "conta": conta_principal,
                },
            )
            if criado:
                criadas.append(t)

        # Saídas variadas
        for desc, nome_cat, v_min, v_max in TRANSACOES_SAIDA:
            categoria = categorias.get(nome_cat)
            eh_fixo = v_min == v_max
            vezes = meses if eh_fixo else random.randint(1, meses)
            datas_usadas = set()

            for _ in range(vezes):
                dt = self._data_aleatoria(hoje, meses, datas_usadas)
                datas_usadas.add(dt)

                valor = Decimal(
                    str(v_min if eh_fixo else random.randint(
                        v_min * 100, v_max * 100
                    ))
                ) / 100

                conta = random.choice(
                    contas_credito
                    if nome_cat == "Cartão de Crédito"
                    else todas_contas
                )

                t, criado = Transaction.objects.get_or_create(
                    usuario=usuario,
                    descricao=desc,
                    data=dt,
                    defaults={
                        "tipo": "saida",
                        "valor": valor,
                        "categoria": categoria,
                        "conta": conta,
                    },
                )
                if criado:
                    criadas.append(t)

        # Entradas extras
        for desc, nome_cat, v_min, v_max in TRANSACOES_ENTRADA:
            if desc == "Salário":
                continue
            categoria = categorias.get(nome_cat)
            vezes = random.randint(1, max(1, meses // 2))

            for _ in range(vezes):
                dt = self._data_aleatoria(hoje, meses)
                valor = Decimal(
                    str(random.randint(v_min * 100, v_max * 100))
                ) / 100
                conta = random.choice(
                    contas_correntes or todas_contas
                )

                t, criado = Transaction.objects.get_or_create(
                    usuario=usuario,
                    descricao=desc,
                    data=dt,
                    defaults={
                        "tipo": "entrada",
                        "valor": valor,
                        "categoria": categoria,
                        "conta": conta,
                    },
                )
                if criado:
                    criadas.append(t)

        return criadas

    def _seed_metas(self, usuario, categorias):
        hoje = date.today()
        criadas = []
        cat_invest = categorias.get("Investimentos")

        for dados in METAS:
            prazo = hoje + timedelta(days=30 * dados["meses"])
            pct = Decimal(str(random.randint(0, 80))) / 100
            valor_atual = (
                dados["valor_alvo"] * pct
            ).quantize(Decimal("0.01"))

            meta, criado = Goal.objects.get_or_create(
                titulo=dados["titulo"],
                usuario=usuario,
                defaults={
                    "valor_alvo": dados["valor_alvo"],
                    "valor_atual": valor_atual,
                    "prazo": prazo,
                    "categoria": cat_invest,
                },
            )
            if criado:
                criadas.append(meta)

        return criadas

    @staticmethod
    def _data_aleatoria(referencia, meses, excluir=None):
        delta_max = meses * 30
        for _ in range(20):
            dias = random.randint(0, delta_max)
            d = referencia - timedelta(days=dias)
            if excluir is None or d not in excluir:
                return d
        return referencia - timedelta(
            days=random.randint(0, delta_max)
        )
