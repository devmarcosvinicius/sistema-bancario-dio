# Press the green button in the gutter to run the script.
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def saque(self, valor):
        saldo = self._saldo
        excedeu_saldo = valor > saldo

        if valor <= 0:
            print("Operação invalida. Valor menor ou igual a zero.")
            return False

        elif excedeu_saldo:
            print("Operação invalida. Valor informado é maior que seu saldo.")
            return False

        saldo -= valor
        print("Saque realizado com sucesso!")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Operação invalida. Valor menor ou igual a zero.")
            return False

        self._saldo += valor
        print("Deposito realizado com sucesso!")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes
                             if transacao["tipo"] == Saque.__name__])
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_saques:
            print("Limite de saque diario atingido. Tente amanha.")
            return
        elif excedeu_limite:
            print("Operação invalida. Saque indisponivel para saques acima de R$500")
            return
        else:
            return super().saque(valor)

    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_trasacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self): pass

    @abstractclassmethod
    def registrar(cls, conta): pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_trasacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_trasacao(self)


def menu():
    return int(input("""
    1. Depositar
    2. Sacar
    3. Extrato
    4. Novo usuário
    5. Nova conta
    6. Listar contas
    0. Sair
    """))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    valor = float(input("Digite o valor do deposito: "))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n=-=-=-=-=-=-=-= Extrato =-=-=-=-=-=-=-=")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo: \n\tR${conta.saldo:.2f}")
    print("=-=-=-=-=-=-=-==-=-=-=-=-=-=-==-=-=-=-=-=-=-=")


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")

    return cliente.contas[0]


def criar_cliente(clientes):
    cpf = input("Informe o CPF (Somente digitos): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Já existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, numero - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("Usuario cadastrado com sucesso!")


def criar_conta_corrente(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nConta criada com sucesso!")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(str(conta))


def main():
    clientes = []
    contas = []

    while True:
        option = menu()

        if option == 1:
            depositar(clientes)

        elif option == 2:
            sacar(clientes)

        elif option == 3:
            exibir_extrato(clientes)

        elif option == 4:
            criar_cliente(clientes)

        elif option == 5:
            numero_conta = len(contas) + 1
            criar_conta_corrente(numero_conta, clientes, contas)

        elif option == 6:
            listar_contas(contas)

        elif option == 0:
            print("Saindo...")
            break
        else:
            print("Opção invalida.")


main()
