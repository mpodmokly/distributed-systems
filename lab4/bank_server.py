import Ice
import Bank
import sys


class BankServiceI(Bank.BankService):
    def __init__(self):
        self.accounts = [
            Bank.Account("Mateusz", 100000)
        ]
    
    def addAccount(self, owner, current=None):
        for acc in self.accounts:
            if acc.owner == owner:
                print(f"Account {owner} already exists")
                raise Bank.AccountAlreadyExists(owner)
        
        self.accounts.append(Bank.Account(owner, 0))
        print(f"Account {owner} created")
    
    def deleteAccount(self, owner, current=None):
        for i in range(len(self.accounts)):
            if self.accounts[i].owner == owner:
                self.accounts.pop(i)
                print(f"Account {owner} deleted")
                return
        
        print(f"Account {owner} does not exist")
        raise Bank.AccountNotFound(owner)

    def deposit(self, owner, amount, current=None):
        if amount <= 0:
            raise Bank.InvalidAmount(amount)

        for acc in self.accounts:
            if acc.owner == owner:
                acc.balance += amount
                print(f"Amount {amount} deposited on {owner}")
                return
        
        print(f"Account {owner} does not exist")
        raise Bank.AccountNotFound(owner)
    
    def withdraw(self, owner, amount, current=None):
        if amount <= 0:
            raise Bank.InvalidAmount(amount)
        
        for acc in self.accounts:
            if acc.owner == owner:
                if acc.balance >= amount:
                    acc.balance -= amount
                    print(f"Amount {amount / 100} withdrawn from {owner}")
                    return
                
                print(f"Account {owner} does not have amount of {amount / 100}")
                raise Bank.InsufficientFunds(owner, amount, acc.balance)
        
        print(f"Account {owner} does not exist")
        raise Bank.AccountNotFound(owner)
    
    def getBalance(self, owner, current=None):
        for acc in self.accounts:
            if acc.owner == owner:
                print(f"{owner} balance: {acc.balance / 100}")
                return acc.balance
        
        print(f"Account {owner} does not exist")
        raise Bank.AccountNotFound(owner)

    def listAccounts(self, current=None):
        print("Sent accounts list")
        return self.accounts


def serve():
    communicator = Ice.initialize(sys.argv)
    adapter = communicator.createObjectAdapterWithEndpoints(
        "ServiceAdapter",
        "default -p 10000"
    )
    servant = BankServiceI()
    adapter.add(servant, communicator.stringToIdentity("service"))
    adapter.activate()
    print("Server running on port 10000...")

    try:
        communicator.waitForShutdown()
    except KeyboardInterrupt:
        print("Server closed")
    finally:
        if communicator:
            communicator.destroy()


if __name__ == "__main__":
    serve()
