from datetime import datetime
import json


class Tracker:
    data = {}

    def __init__(self, name):
        self.name = name
        if name not in Tracker.data:
            Tracker.data[name] = {"transactions": []}
        self.transactions = Tracker.data[name]["transactions"]

    def add_transaction(self, amount, category, date, description, trans_type):
        self.transactions.append(
            {
                "id": len(self.transactions) + 1,
                "amount": amount,
                "category": category,
                "date": date,
                "description": description,
                "trans_type": trans_type,
            }
        )

    @classmethod
    def save(cls):
        with open("exptra.json", "w") as f:
            json.dump(cls.data, f, indent=4)

    @classmethod
    def load(cls):
        try:
            with open("exptra.json", "r") as f:
                cls.data = json.load(f)
        except FileNotFoundError:
            cls.data = {}

    def view_transactions(self):
        return self.transactions

    def del_transaction(self, id):
        for trans in self.transactions:
            if trans["id"] == id:
                self.transactions.remove(trans)
        for i, trans in enumerate(self.transactions, start=1):
            trans["id"] = i

    def edit_transaction(self, id, amount, categrory, date, description, trans_type):
        for trans in self.transactions:
            if trans["id"] == id:
                trans.update(
                    {
                        "amount": amount,
                        "category": categrory,
                        "date": date,
                        "description": description,
                        "trans_type": trans_type,
                    }
                )

    @property
    def balance(self):
        income = 0
        expense = 0
        for trans in self.transactions:
            if trans["trans_type"]:
                income += trans["amount"]
            else:
                expense += trans["amount"]
        balance = income - expense
        return balance

    @staticmethod
    def account_transfer(trans_from, trans_to, amount, date, description):

        if amount <= 0:
            return "Error: invalid amount"
        if trans_from.balance < amount:
            return "Error: insufficient funds"
        try:
            trans_from.add_transaction(
                amount, "Account Transfer", date, description, False
            )
            trans_to.add_transaction(
                amount, "Account Transfer", date, description, True
            )
        except:
            return "Error"

    def sort(self, sorting):
        categories = {
            "food/groceries": [],
            "rent/housing": [],
            "utilities": [],
            "transportation": [],
            "entertainment": [],
            "healthcare": [],
            "shopping": [],
            "education": [],
            "salary/income": [],
            "savings": [],
            "misc/other": [],
        }
        date_sorted = sorted(
            self.transactions, key=lambda d: datetime.strptime(d["date"], "%d-%m-%Y")
        )
        for trans in self.transactions:
            if trans["category"] in categories:
                categories[trans.get("category")].append(trans)
        if sorting == "category":
            return categories
        elif sorting == "date":
            return date_sorted

    def budget(self, cat, amount):
        if "budget" not in Tracker.data[self.name]:
            Tracker.data[self.name]["budget"] = {}
        Tracker.data[self.name]["budget"][cat] = amount

    def fetch_budget(self):
        if "budget" not in Tracker.data[self.name]:
            return "Budget not set yet!"
        else:
            return Tracker.data[self.name]["budget"]

    @staticmethod
    def print_main_menu():
        print("=== Expense Tracker ===")
        print("1) View accounts / balances")
        print("2) Select an account")
        print("3) Create new account")
        print("4) Transfer between accounts")
        print("5) View all transactions")
        print("6) Save & Exit")

    def print_account_menu(self):
        print(f"=== Account: {self.name} | Balance: ${self.balance:.2f} ===")
        print("1) View transactions")
        print("2) Add transaction")
        print("3) Edit transaction")
        print("4) Delete transaction")
        print("5) View by category")
        print("6) Set/update budget")
        print("7) View budget")
        print("8) Back to main menu")


Tracker.load()
accounts = {}
for name in Tracker.data.keys():
    accounts[name] = Tracker(name)


def print_trans(list):
    for t in list:
        print(f"{t["id"]})")
        print(f"Date: {t["date"]}.")
        print(f"Amount: ${"" if t["trans_type"] else "-"}{t["amount"]}.")
        print(f"Description: {t["description"]}.")
        print(f"Category: {t["category"]}. \n")


def print_categories():
    print(
        "\n1)Food/groceries.   2)Rent/housing.   3)Utilities.   4)Transportation.   5)Entertainment"
    )
    print(
        "6)Healthcare.   7)Shopping   8)Education.   9)Salary/income   10)Savings   11)Misc/other"
    )



while True:
    Tracker.print_main_menu()
    action = int(input("What is your preffered action?: "))
    if action == 6:
        break
    elif action == 1:
        print("Your accounts")
        for i, ac in enumerate(Tracker.data, start=1):
            print(f"{i}) {ac.title()}:  ${accounts[ac].balance}")
            print()
    elif action == 2:
        categories = {
            "food/groceries": 1,
            "rent/housing": 2,
            "utilities": 3,
            "transportation": 4,
            "entertainment": 5,
            "healthcare": 6,
            "shopping": 7,
            "education": 8,
            "salary/income": 9,
            "savings": 10,
            "misc/other": 11,
        }

        print("Select an account")
        if len(Tracker.data) == 0:
            print("No accounts found")
            print()
            continue
        for i, ac in enumerate(Tracker.data, start=1):
            print(f"{i}) {ac.title()}")
            print()
        selection = input("Enter account name: ").lower()
        while True:
            accounts[selection].print_account_menu()
            act = int(input("Your preffered action: "))
            if act == 1:
                trans = accounts[selection].view_transactions()
                print("Transactions: \n")
                print_trans(trans)
            elif act == 2:

                print("Add transaction:")
                try:
                    date = input("Date of transaction(dd-mm-yyy): ").strip()
                    datetime.strptime(date, "%d-%m-%Y")
                except:
                    print("Invalid date format")
                    continue
                amount = float(input("Amount transferred($): ").strip())
                description = input("Description: ")
                x = input("Is this income or expense (i/e): ").strip().lower()
                typeof = True if x == "i" else False
                print_categories()
                y = int(input("Transaction type: "))
                category = ""
                for cat_name, cat_num in categories.items():
                    if y == cat_num:
                        category = cat_name
                accounts[selection].add_transaction(
                    amount, category, date, description, typeof
                )
            elif act == 3:
                trans = accounts[selection].view_transactions()
                print("Transactions: \n")
                print_trans(trans)
                id = int(
                    input(
                        "Enter the serial no of the transaction you would like to edit:"
                    )
                )
                try:
                    date = input("Date of transaction(dd-mm-yyy): ").strip()
                    datetime.strptime(date, "%d-%m-%Y")
                except:
                    print("Invalid date format")
                    continue
                amount = float(input("Enter the edited amount: "))
                description = input("Enter the edited description: ")
                x = input("Income or expense (i/e): ").strip().lower()
                typeof = True if x == "i" else False
                print_categories()
                y = int(input("Transaction type: "))
                category = ""
                for cat_name, cat_num in categories.items():
                    if y == cat_num:
                        category = cat_name
                accounts[selection].edit_transaction(
                    id, amount, category, date, description, typeof
                )
            elif act == 4:
                trans = accounts[selection].view_transactions()
                print_trans(trans)
                id = int(
                    input(
                        "Enter the serial no of the transaction you would like to delete:"
                    )
                )
                conformation = input(
                    "Would you like to delete this transaction?(y/n): "
                )
                if conformation == "y":
                    accounts[selection].del_transaction(id)
                else:
                    print("Error!")
            elif act == 5:
                q = input("Sort by category or date (c/d)?: ").lower().strip()
                sorting = ""
                if q == "c":
                    sorting = "category"
                    sorted_trans = accounts[selection].sort(sorting)
                    for keys, values in sorted_trans.items():
                        if len(values) > 0:
                            print(keys.title())
                            print()
                            print_trans(values)
                elif q == "d":
                    sorting = "date"
                    sorted_trans = accounts[selection].sort(sorting)
                    print_trans(sorted_trans)
                else:
                    print("Invalid input.")
                    continue

            elif act == 6:
                print_categories()
                while True:
                    category = ""
                    cat = int(
                        input(
                            "Serial numeber of the category you would like to budget (Enter 0 to cancel): "
                        )
                    )
                    if cat == 0:
                        break
                    budget = float(input("Your budget($): "))
                    for key, value in categories.items():
                        if cat == value:
                            category = key
                    accounts[selection].budget(category, budget)
                    print("Budget set!")
            elif act == 7:
                bud = accounts[selection].fetch_budget()
                if isinstance(bud, str):
                    print(bud)
                else:
                    print("Your budget:")
                    for i, (keys, values) in enumerate(bud.items(), start=1):
                        print(f"{i}) {keys.title()}: {values}")
            elif act == 8:
                break
    elif action == 3:
        print("Create new account: ")
        name = input("Name: ")
        confirmation = input(
            f"Are you sure that you would like to create an account named {name}?(y/n):"
        )
        if confirmation == "n":
            continue
        elif confirmation == "y":
            name = Tracker(name)
            print("Account created succesfully.")
            Tracker.save()
            Tracker.load()
            for name in Tracker.data.keys():
             accounts[name] = Tracker(name)

    elif action == 4:
        if len(accounts) <= 1:
            print("More than one account needed to transfer between accounts.")
            continue
        else:
            for i, ac in enumerate(Tracker.data, start=1):
                print(f"{i}) {ac.title()}")
                print()
            acc1 = input("Transfer from (enter account name): ").lower().strip()
            acc2 = input("Transfer to (enter account name): ").lower().strip()
            try:
                date = input("Date of transaction(dd-mm-yyy): ").strip()
                datetime.strptime(date, "%d-%m-%Y")
            except:
                print("Invalid date format")
                continue
            amount = float(input("Enter the edited amount: "))
            description = input("Enter the edited description: ")
            try:
                Tracker.account_transfer(
                    accounts[acc1], accounts[acc2], amount, date, description
                )
            except:
                print("Transfer failed.")
    elif action == 5:
        print()
        data = Tracker.data
        transacs = []
        for keys, values in data.items():
            print(keys.title())
            print()
            for v in values["transactions"]:
                transacs.append(v)
            print_trans(transacs)

    else:
        print("Error! Invalid serial number!")


Tracker.save()
