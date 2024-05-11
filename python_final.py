class Bank:
    def __init__(self, name, address, balance):
        self.__name = name
        self.__address = address
        self.__users = []
        self.__admins = []
        self.__balance = balance
        self.__bankrupt = False
        self.__loan = True
        self.__loanAmount = 0

    @property
    def name(self):
        return self.__name
    
    @property
    def address(self):
        return self.__address
   
    @property
    def users(self):
        return self.__users
    
    @property
    def balance(self):
        return self.__balance
    
    @property
    def loan(self):
        return self.__loan


    @property
    def bankrupt(self):
        return self.__bankrupt
    
    @property
    def loanAmount(self):
        return self.__loanAmount
    
    def add_to_loan_amount(self, amount):
        self.__loanAmount += amount
   
    def add_balance(self, amount):
        self.__balance += amount

    def negate_balance(self, amount):
        self.__balance -= amount

    def turn_on_loan(self, admin):
        if isinstance(admin, Admin):
            self.__loan = True
        else:
            print("Only admin can loan turn on")

    def turn_off_loan(self, admin):
        if isinstance(admin, Admin):
            self.__loan = False
        else:
            print("Only admin can loan turn of")

    def add_user(self, user):
        self.__users.append(user)

    def add_admin(self, admin):
        if(isinstance(admin, Admin)):
            self.__admins.append(admin)
        else:
            print("Not an admin account")

    def remove_user(self, index, admin):
        if(isinstance(admin, Admin)):
            self.__users.pop(index)
        else:
            print("Not an admin account")

    def give_loan(self, amount, user):
        if not self.__loan:
            print("Loan feature is currently not available.")
            return False
       
        elif amount > self.__balance:
            print("Loan amount exceeded")
            return False
        
        self.__balance -= amount
        self.__loanAmount += amount
        print("Successfully received loan.")
        return True

class Admin:
    def __init__(self, name, email):
        self.__name = name
        self.__email = email
        self.__bank = None

    @property
    def name(self):
        return self.__name
    
    @property
    def email(self):
        return self.__email
    
    def create_admin_account(self, bank):
        self.__bank = bank
        self.__bank.add_admin(self)

    def view_user_accounts(self):
        print("Users:")
        n = 1
        for user in self.__bank.users:
            print(f"{n}. Name: {user.name} Account_No: {user.accountNumber}")
            n += 1

    def delete_user_account(self, index):
        if index > len(self.__bank.users):
            print("Index out of range.")
            return
        self.__bank.remove_user(index, self)

    def check_bank_balance(self):
        print(f"Total bank balance of {self.__bank.name} is {self.__bank.balance}")

    def turn_on_loan(self):
        self.__bank.turn_on_loan(self)
        print("Bank loan feature turned on")

    def turn_off_loan(self):
        self.__bank.turn_off_loan(self)
        print("Bank loan feature turned off")
       
    def view_total_loan(self):
        print(f"Total loan amount of {self.__bank.name} is {self.__bank.loanAmount}")

class User:
    __accountNumber = 100000

    def __init__(self, name, email, address, accounType):
        self.__name = name
        self.__email = email
        self.__address = address
        self.__accounType = accounType
        self.__accountNumber = self.account_number_generator()
        self.__balance = 0
        self.__transctionHistory = []
        self.__bank = None
        self.__loan = 0

    @property
    def name(self):
        return self.__name
    
    @property
    def email(self):
        return self.__email
    
    @property
    def address(self):
        return self.__address

    @property
    def accounType(self):
        return self.__accounType
   
    @property
    def accountNumber(self):
        return self.__accountNumber

    @property
    def balance(self):
        return self.__balance
    
    def create_user_account(self, bank):
        self.__bank = bank
        self.__bank.add_user(self)
   
    def account_number_generator(self):
        # number = User.__accountNumber
        User.__accountNumber += 101
        return User.__accountNumber

    def check_account_balance(self):
        print(f"Balance of account is {self.__balance}")

    def deposit(self, amount):
        self.__balance += amount
        self.__bank.add_balance(amount)
        self.__transctionHistory.append(f"deposited {amount} to account.")
        print(f"deposited {amount} to account.")

    def withdraw(self, amount):
        if amount > self.__balance:
            print("Withdrawal amount exceeded.")
            return
        
        if self.__bank.bankrupt:
            print(f"{self.__bank.name} is bankrupt")
            return

        self.__balance -= amount
        self.__bank.negate_balance(amount)
        self.__transctionHistory.append(f"Withdrew {amount} from account.")
        print(f"Withdrew {amount} from account.")

    def transfer(self, reciever, amount):
        if not isinstance(reciever, User):
            print("The account does not exist.")
            return

        if self.__balance < amount:
            print("Transfer amount is greater than account balance.")
            return
        self.__balance -= amount
        reciever.receive(self, amount)
        self.__transctionHistory.append(f"Transferred {amount} to Name:{reciever.name} Account_No:{reciever.accountNumber}")
        print(f"Transferred {amount} to Name:{reciever.name} Account_No:{reciever.accountNumber}")

    def receive(self, sender, amount):
        self.__balance += amount
        self.__bank.add_balance(amount)
        self.__transctionHistory.append(f"Received {amount} from Name: {sender.name} Account_No: {sender.accountNumber}")

    def view_transaction_history(self):
        print("Transactions: ")
        for transaction in self.__transctionHistory:
            print(transaction)

    def take_loan(self, amount):
        if self.__loan < 2:
            if self.__bank.give_loan(amount, self):
                self.__balance += amount
                self.__transctionHistory.append(f"Took Loan in amount {amount}")
                self.__loan += 1
        else:
            print("Two times loan already taken.")

bank = Bank("Bank Asia", "Brahmanbaria", 10000)
admin = Admin("admin","admin@gmail.com")
admin.create_admin_account(bank)

while True:
    print("1. Admin")
    print("2. User")
    print("3. Exit")

    option = int(input("Enter Option: "))

    if option == 1:
        # Name: admin
        # Email: admin@gmail.com
        name = input("Enter Name as admin: ")
        email = input("Enter Email as admin@gmail.com: ")

        if name == "admin" and email == "admin@gmail.com":
            while True:
                print("1. Add User Account")
                print("2. Delete User Account")
                print("3. View All Users")
                print("4. Check Total Available Balance")
                print("5. Check Total Loan Amount")
                print("6. Turn on Loan Features")
                print("7. Turn off Loan Features")
                print("8. Logout")

                option = int(input("Enter Option: "))

                if option == 1:
                # bank = Bank("Bank Asia", "Brahmanbaria", 828578)
                    name = input("Enter Name: ")
                    email = input("Enter Email: ")
                    address = input("Enter Address: ")
                    Types = input("Enter Type: ")
                    usr = User(name,email,address,Types)
                    usr.create_user_account(bank)

                elif option == 2:
                    admin.view_user_accounts()
                    index = int(input("Enter index of User: ")) - 1
                    admin.delete_user_account(index)

                elif option == 3:
                    admin.view_user_accounts()
                
                elif option == 4:
                    admin.check_bank_balance()
        
                elif option == 5:
                    admin.view_total_loan()

                elif option == 6:
                    admin.turn_on_loan()

                elif option == 7:
                    admin.turn_off_loan()
                
                elif option == 8:
                    break
    
    elif option == 2:
        name = input("Enter Name: ")
        email = input("Enter Email: ")
        address = input("Enter Address: ")
        Types = input("Enter Type: ")
        usr = User(name,email,address,Types)
        usr.create_user_account(bank)
        while True:
            print("1. Deposite Money")
            print("2. Withdraw Money")
            print("3. Check Available Balance")
            print("4. Check Transactions History")
            print("5. Take Loan")
            print("6. Transfer Amount")
            print("6. Logout")

            option = int(input("Enter Option: "))

            if option == 1:
                amount = int(input("Enter Deposit Amount: "))
                usr.deposit(amount)
            
            elif option == 2:
                amount = int(input("Enter Withdraw Amount: "))
                usr.withdraw(amount)

            elif option == 3:
                usr.check_account_balance()
           
            elif option == 4:
                usr.view_transaction_history()
            
            elif option == 5:
                amount = int(input("Enter Loan amount: "))
                usr.take_loan(amount)
            
            elif option == 6:
                amount = int(input("Enter transfer amount: "))
                usr.transfer(usr, amount)

            elif option == 7:
                break