# Press the green button in the gutter to run the script.

def menu():
    return int(input("""
    1. Depositar
    2. Sacar
    3. Extrato
    4. Novo usúario
    5. Nova conta
    6. Listar contas
    0. Sair
    """))

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques > limite_saques

    if excedeu_saques:
        print("Limite de saque diario atingido. Tente amanha.")
        return
    elif excedeu_limite:
        print("Operação invalida. Saque indisponivel para saques acima de R$500")
        return
    elif valor <= 0:
        print("Operação invalida. Valor menor ou igual a zero.")
        return
    elif excedeu_saldo:
        print("Operação invalida. Valor informado é maior que seu saldo.")
        return

    numero_saques += 1
    saldo -= valor
    extrato += f"Saque: R${valor:.2f}\n"
    print("Saldo realizado com sucesso!")

    return saldo, extrato

def deposito(saldo, valor, extrato):
    if valor <= 0:
        print("Operação invalida. Valor menor ou igual a zero.")
        return

    saldo += valor
    extrato += f"Deposito: R${valor:.2f}\n"
    print("Operação realizada com sucesso.")

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("=-=-=-==-=-=-= Extrato =-=-=-==-=-=-=")
    print("Não foi realizado nenhuma movimentação.\n" if not extrato else extrato)
    print(f"Saldo: R${saldo:.2f}")
    print("=-=-=-==-=-=-==-=-=-==-=-=-==-=-=-=-=")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (Somente digitos): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, numero - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuario cadastrado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta_corrente(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuàrio: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("Usuario não encontrado, fluxo de criação de conta encerrado!")

def listar_contas(contas):
    for conta in contas:
        print(f"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
Agência: {conta['agencia']}
Conta: {conta['numero_conta']}
Titular: {conta['usuario']['nome']}
        """)
    else:
        print("Nenhuma conta cadastrada.")

def main():
    QTD_LIMITE_SAQUE = 3
    LIMITE_SAQUE = 500
    AGENCIA = "0001"

    saldo = 0
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:

        option = menu()

        if option == 1:
            valor = float(input("Digite o valor a ser depositado: "))
            saldo, extrato = deposito(saldo, valor, extrato)

        elif option == 2:
            valor = float(input("Digite o valor a ser sacado: "))
            saldo, extrato = saque(saldo=saldo, valor=valor, limite=LIMITE_SAQUE, numero_saques=numero_saques, limite_saques=QTD_LIMITE_SAQUE)

        elif option == 3:
            exibir_extrato(saldo, extrato=extrato)

        elif option == 4:
            criar_usuario(usuarios)

        elif option == 5:
            numero_conta = len(contas) + 1
            conta = criar_conta_corrente(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif option == 6:
            listar_contas(contas)

        elif option == 0:
            print("Saindo...")
            break
        else:
            print("Opção invalida.")

main()