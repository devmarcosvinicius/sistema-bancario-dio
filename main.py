if __name__ == '__main__':
    LIMITE_SAQUE = 3
    saldo = 0
    extrato = ""
    qtd_saques_diario = 0
    excedeu_saques_diario = qtd_saques_diario >= LIMITE_SAQUE

    while True:

        menu = """
1. Depositar
2. Sacar
3. Extrato
4. Sair
"""
        option = int(input(menu))

        if option == 1:
            valor = float(input("Digite o valor a ser depositado: "))

            if valor <= 0:
                print("Operação invalida. Valor menor ou igual a zero.")

            saldo += valor
            extrato += f"Deposito: R${valor:.2f}\n"
            continue
        elif option == 2:
            valor = float(input("Digite o valor a ser sacado: "))
            if excedeu_saques_diario:
                print("Limite de saque diario atingido. Tente amanha.")
                continue
            if valor > 500:
                print("Operação invalida. Saque indisponivel para saques acima de R$500")
                continue
            if valor <= 0:
                print("Operação invalida. Valor menor ou igual a zero.")
                continue
            if valor > saldo:
                print("Operação invalida. Valor informado é maior que seu saldo.")

            qtd_saques_diario += 1
            saldo -= valor
            extrato += f"Saque: R${valor:.2f}\n"
            continue

        elif option == 3:
            print("=-=-=-==-=-=-= Extrato =-=-=-==-=-=-=")
            print("Não foi realizado nenhuma movimentação.\n" if not extrato else extrato)
            print(f"Saldo: R${saldo:.2f}")
            print("=-=-=-==-=-=-==-=-=-==-=-=-==-=-=-=-=")
            continue
        elif option == 4:
            print("Saindo...")
            break
        else:
            print("Opção invalida.")