module Bank {
    struct Account {
        string owner;
        long balance;
    };

    sequence<Account> Accounts;

    exception AccountNotFound {
        string owner;   
    };
    exception AccountAlreadyExists {
        string owner;
    };
    exception InvalidAmount {
        long amount;
    };
    exception InsufficientFunds {
        string owner;
        long amount;
        long available;
    };

    interface BankService {
        void addAccount(string owner) throws AccountAlreadyExists;
        void deleteAccount(string owner) throws AccountNotFound;
        void deposit(string owner, long amount)
            throws AccountNotFound, InvalidAmount;
        void withdraw(string owner, long amount)
            throws AccountNotFound, InvalidAmount, InsufficientFunds;
        long getBalance(string owner) throws AccountNotFound;
        Accounts listAccounts();
    };
};
