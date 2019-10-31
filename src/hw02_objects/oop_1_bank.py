"""
Exercise 1: (5 points)

a) Using the slides & the script, put together a file
    containing the complete Account class.
    Each method must have a documentation string at the
    beginning which describes what the method is doing.
    (1 point)

b) Create a main application where you create a number of accounts.
    Play around with depositing / withdrawing money.
    Change the account holder of an account using a setter method.
    (1 point)

c) Change the withdraw function such that the minimum balance
    allowed is -1000.
    (1 point)

d) Write a function apply_interest(self) which applies an interest
    rate of 1.5% to the current balance and call it on your objects.
    (1 point)

e) Draw a UML diagram representing your Account class. (1 point)
"""


class Account:
    """ Here has to be a documentation string that describes
    which data objects this class is designed for.
    You have to remove the pass statement and then write some
    code for the class. """
    interest_rate = 0.15
    num_of_accounts = 0
    # CONSTRUCTOR
    def __init__(self, num: object, person: object) -> object:
      self.balance = 0
      self.number = num
      self.holder = person
      self.minBalance = -1000
      Account.num_of_accounts += 1
    # METHODS
    # the method upgrade a balance of an account
    def deposit(self, amount):
      self.balance += amount

    # withdrawing money without negative balance
    def withdraw(self, amount):
      if amount > self.balance - self.minBalance:
        amount = self.balance
      self.balance -= amount
      return amount

    # the method sets a new holder to an account
    # validates a new value or raises an exception
    def set_holder(self, person):
       if (not type(person) == str):
           raise TypeError
       if not (re.match("\w+( \w+)*", person.strip())):
           raise ValueError
       self.holder = person
    # String representation of an object:
    # the method resturs string that describes an account
    def __str__(self):
      res = "*** Account Info ***\n"
      res += "Account ID:" + str(self.number) + "\n"
      res += "Holder:" + self.holder + "\n"
      res += "Balance: " + str(self.balance) + "\n"
      return res

    # Static method that prints the info about number of excisting accounts
    @ staticmethod
    def accounts_info():
      print(Account.num_of_accounts, "accounts have been created.")
  

    # applies interesr rate to the balance of the saving account
    def apply_interest(self):
     self.balance *= (1 + Account.interest_rate)



if __name__ == "__main__":
    print("Welcome to the Python Bank!")
    juliasAccount = Account(1,"Julia")
    eliassAccount = Account(2, "Elias")

    juliasAccount.deposit(200)
    juliasAccount.withdraw(100)
    print(juliasAccount)
    juliasAccount.set_holder("David")
    juliasAccount.apply_interest()
    print(juliasAccount)



    eliassAccount.deposit(500)
    eliassAccount.withdraw(2000)
    print(eliassAccount)

    Account.accounts_info()