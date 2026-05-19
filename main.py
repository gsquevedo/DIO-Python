from abc import ABC, abstractmethod
from datetime import datetime
import textwrap


class Client:
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)


class NaturalPerson(Client):
    def __init__(self, name, email, date_of_birth, address, cpf):
        super().__init__(name, email, address)
        self.date_of_birth = date_of_birth
        self.cpf = cpf


class History:
    def __init__(self):
        self._transaction_history = []

    @property
    def transaction_history(self):
        return self._transaction_history

    def add_transaction(self, transaction):
        self._transaction_history.append(transaction)


class Account:
    AGENCY = "0001"

    def __init__(self, account_number, client, balance=0):
        self.account_number = account_number
        self.client = client
        self._balance = balance
        self.history = History()

    @classmethod
    def create_account(cls, account_number, client):
        account = cls(account_number, client)
        client.add_account(account)
        return account

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            print("Saldo não pode ser negativo.")
            return

        self._balance = value

    @property
    def account_info(self):
        return (
            f"Agência: {self.AGENCY}\n"
            f"Conta: {self.account_number}\n"
            f"Saldo: R$ {self.balance:.2f}"
        )

    @property
    def client_info(self):
        return (
            f"Cliente: {self.client.name}\n"
            f"Email: {self.client.email}\n"
            f"Endereço: {self.client.address}"
        )

    def withdraw(self, amount):
        if amount <= 0:
            print("O valor do saque deve ser positivo.")
            return False

        if amount > self.balance:
            print("Saldo insuficiente.")
            return False

        self.balance -= amount
        print(f"Saque realizado com sucesso. Novo saldo: R$ {self.balance:.2f}")
        return True

    def deposit(self, amount):
        if amount <= 0:
            print("O valor do depósito deve ser positivo.")
            return False

        self.balance += amount
        print(f"Depósito realizado com sucesso. Novo saldo: R$ {self.balance:.2f}")
        return True


class CurrentAccount(Account):
    def __init__(
        self,
        account_number,
        client,
        balance=0,
        limit=500,
        withdrawal_limit=3,
    ):
        super().__init__(account_number, client, balance)
        self.limit = limit
        self.withdrawal_limit = withdrawal_limit
        self.withdrawals_made = 0

    def withdraw(self, amount):
        if amount <= 0:
            print("O valor do saque deve ser positivo.")
            return False

        if amount > self.limit:
            print(f"O saque excede o limite de R$ {self.limit:.2f}.")
            return False

        if self.withdrawals_made >= self.withdrawal_limit:
            print("Limite diário de saques atingido.")
            return False

        if amount > self.balance:
            print("Saldo insuficiente.")
            return False

        self.balance -= amount
        self.withdrawals_made += 1

        print(
            f"Saque realizado com sucesso.\n"
            f"Saldo atual: R$ {self.balance:.2f}\n"
            f"Saques restantes: "
            f"{self.withdrawal_limit - self.withdrawals_made}"
        )

        return True

    def __str__(self):
        return (
            f"Agência:\t{self.AGENCY}\n"
            f"C/C:\t\t{self.account_number}\n"
            f"Titular:\t{self.client.name}"
        )


class Transaction(ABC):
    def __init__(self, amount, description=""):
        self.amount = amount
        self.date = datetime.now()
        self.description = description

    def __str__(self):
        return (
            f"{self.date.strftime('%d/%m/%Y %H:%M:%S')} - "
            f"{self.description}: R$ {self.amount:.2f}"
        )

    @property
    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def register(self, account):
        pass


class Deposit(Transaction):
    def __init__(self, amount):
        super().__init__(amount, "Depósito")

    @property
    def value(self):
        return self.amount

    def register(self, account):
        success = account.deposit(self.amount)

        if success:
            account.history.add_transaction(str(self))


class Withdrawal(Transaction):
    def __init__(self, amount):
        super().__init__(amount, "Saque")

    @property
    def value(self):
        return -self.amount

    def register(self, account):
        success = account.withdraw(self.amount)

        if success:
            account.history.add_transaction(str(self))


def menu():
    menu_text = """
    ================ MENU ================
    [1] Criar cliente
    [2] Criar conta
    [3] Depositar
    [4] Sacar
    [5] Ver informações da conta
    [6] Ver histórico de transações
    [7] Extrato
    [8] Listar clientes
    [9] Sair
    ======================================
    """

    print(textwrap.dedent(menu_text))

    return input("Escolha uma opção: ")


def filter_client(name, clients):
    for client in clients:
        if client.name.lower() == name.lower():
            return client

    return None


def recover_customer_account(client):
    if client.accounts:
        return client.accounts[0]

    return None


def create_client(clients):
    print("\n=== CRIAR CLIENTE ===")

    cpf = input("CPF: ")

    for client in clients:
        if isinstance(client, NaturalPerson) and client.cpf == cpf:
            print("Já existe um cliente com este CPF.")
            return

    name = input("Nome: ")
    email = input("Email: ")
    address = input("Endereço: ")
    date_of_birth = input("Data de nascimento (YYYY-MM-DD): ")

    client = NaturalPerson(
        name=name,
        email=email,
        date_of_birth=date_of_birth,
        address=address,
        cpf=cpf,
    )

    clients.append(client)

    print("Cliente criado com sucesso.")


def create_account(clients, accounts):
    print("\n=== CRIAR CONTA ===")

    name = input("Nome do cliente: ")

    client = filter_client(name, clients)

    if not client:
        print("Cliente não encontrado.")
        return

    account_number = len(accounts) + 1

    account = CurrentAccount.create_account(account_number, client)

    accounts.append(account)

    print("Conta criada com sucesso.")
    print(account)


def deposit(clients):
    print("\n=== DEPÓSITO ===")

    name = input("Nome do cliente: ")

    client = filter_client(name, clients)

    if not client:
        print("Cliente não encontrado.")
        return

    account = recover_customer_account(client)

    if not account:
        print("Conta não encontrada.")
        return

    try:
        amount = float(input("Valor do depósito: R$ "))
    except ValueError:
        print("Valor inválido.")
        return

    transaction = Deposit(amount)
    transaction.register(account)


def withdraw(clients):
    print("\n=== SAQUE ===")

    name = input("Nome do cliente: ")

    client = filter_client(name, clients)

    if not client:
        print("Cliente não encontrado.")
        return

    account = recover_customer_account(client)

    if not account:
        print("Conta não encontrada.")
        return

    try:
        amount = float(input("Valor do saque: R$ "))
    except ValueError:
        print("Valor inválido.")
        return

    transaction = Withdrawal(amount)
    transaction.register(account)


def show_account_info(clients):
    print("\n=== INFORMAÇÕES DA CONTA ===")

    name = input("Nome do cliente: ")

    client = filter_client(name, clients)

    if not client:
        print("Cliente não encontrado.")
        return

    account = recover_customer_account(client)

    if not account:
        print("Conta não encontrada.")
        return

    print("\n--- DADOS DA CONTA ---")
    print(account.account_info)

    print("\n--- DADOS DO CLIENTE ---")
    print(account.client_info)


def show_transaction_history(clients):
    print("\n=== HISTÓRICO DE TRANSAÇÕES ===")

    name = input("Nome do cliente: ")

    client = filter_client(name, clients)

    if not client:
        print("Cliente não encontrado.")
        return

    account = recover_customer_account(client)

    if not account:
        print("Conta não encontrada.")
        return

    history = account.history.transaction_history

    if not history:
        print("Nenhuma transação encontrada.")
        return

    for transaction in history:
        print(transaction)


def display_statement(clients):
    print("\n=== EXTRATO ===")

    name = input("Nome do cliente: ")

    client = filter_client(name, clients)

    if not client:
        print("Cliente não encontrado.")
        return

    account = recover_customer_account(client)

    if not account:
        print("Conta não encontrada.")
        return

    print("\n========== EXTRATO ==========")

    history = account.history.transaction_history

    if not history:
        print("Não foram realizadas movimentações.")
    else:
        for transaction in history:
            print(transaction)

    print(f"\nSaldo atual: R$ {account.balance:.2f}")
    print("================================")


def list_clients(clients):
    print("\n=== LISTA DE CLIENTES ===")

    if not clients:
        print("Nenhum cliente cadastrado.")
        return

    for client in clients:
        print(
            f"""
            Nome: {client.name}
            CPF: {client.cpf}
            Email: {client.email}
            Endereço: {client.address}
            """
        )


def main():
    clients = []
    accounts = []

    while True:
        option = menu()

        if option == "1":
            create_client(clients)

        elif option == "2":
            create_account(clients, accounts)

        elif option == "3":
            deposit(clients)

        elif option == "4":
            withdraw(clients)

        elif option == "5":
            show_account_info(clients)

        elif option == "6":
            show_transaction_history(clients)

        elif option == "7":
            display_statement(clients)

        elif option == "8":
            list_clients(clients)

        elif option == "9":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()