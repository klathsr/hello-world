from P2f import BankAccount

# Create accounts
john = BankAccount("John", "saving", 500)
tim = BankAccount("Tim", "loan", -1000000)
sarah = BankAccount("Sarah", "saving")

accounts = [john, tim, sarah]

john.deposit(3000)

tim.pay_loan(500000)

sarah.deposit(50000000)

sarah_loan = BankAccount("Sarah", "loan", -100000000)
accounts.append(sarah_loan)

for acc in accounts:
    acc.print_customer()
