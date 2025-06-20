



import sqlite3
from random import randrange

# Connect to SQLite database (or create it)
conn = sqlite3.connect("atm_system.db")
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    pin INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    balance REAL DEFAULT 0.0,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    account_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    amount REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(account_id) REFERENCES accounts(account_id)
)
''')


conn.commit()        

def log_in():
    # -----
    user_id = input("Enter your user_id: ").capitalize()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    res = cursor.fetchone()
    if res is None:
        print(f"{user_id} doesnt have a bank account")
        ans = input("Do you want to create new bank account (yes/no): ")
        ans = ans.lower()
        if ans == "yes":
            new_user(user_id)
            print("Bank account opened successfully!")
        elif ans == "no":
            pass
        else:
            print("Invalid Input")
    else:
        atmpts = 3
        while atmpts > 0:
            try:
                pin = int(input("Enter your 4-digit Pin: "))
                if len(str(pin)) != 4:
                    print("Pin must be of exactly 4-digits.")
                    continue
                cursor.execute('select * from users where pin = ?',(pin,))
                if cursor.fetchone():
                    print("Login successful!")
                    acc_log_in(user_id,pin)
                    break
                else:
                    atmpts -= 1
                    print(f"Incorrect PIN. {atmpts} attempts left")
                    if atmpts == 0:
                        print("Too many incorrect attempts. Exiting...")
            except ValueError:
                print("Invalid input. Please enter a numeric PIN.")
            except Exception as e:
                print(e)
                atmpts -= 1
                print(f"Incorrect PIN. {atmpts} attempts left")
        if atmpts == 0:
            print("Too many incorrect attempts. Exiting...")
# -----
def banking_services(user_id,balance, ac_id,pin):
    print(""" ==== Banking services Menu ====
Check balance             ---> 1
Deposit                   ---> 2        
Withdraw                  ---> 3
Send Money                ---> 4
Go to Account Management  ---> 5
Exit banking services     ---> 6""")
    Exit = False
    while not Exit:
        try:
            menu = int(input("\nEnter the desired operation number from menu or 6 to exit: "))
            if menu == 1:
                check_balance(balance)
            elif menu == 2:
                balance = deposit(user_id,ac_id, balance)
                check_balance(balance)
            elif menu == 3:
                wd_amt = int(input("Enter the withdrawing amount:"))
                if wd_amt <= balance:
                    balance = withdraw(user_id,ac_id, balance,wd_amt)
                    check_balance(balance)
                else:
                    check_balance(balance)
                    print("Withdrawing amount is more than available balance")
            elif menu == 4:
                transfer(user_id,ac_id, balance)
            elif menu == 5:
                acc_mgmt(user_id,balance,ac_id,pin)
            elif menu == 6:
                Exit = True
                print("Banking services exited!")
            else:
                pass
        except ValueError:
            print("Invalid input ! please enter a numeric value. ")
        except Exception as e:
            print(e)
# -----
def check_balance(balance):
    print(f"Available Balance: ${balance}")
    return balance
# -----
def deposit(user_id,ac_id, balance):
    try:
        amt = int(input("Enter depositing amount:"))
        balance += amt
        cursor.execute('update accounts set balance = ? where account_id = ?',(balance,ac_id))
        conn.commit()
        cursor.execute('INSERT INTO transactions (user_id, account_id, type, amount) VALUES (?, ?, ?, ?)', (user_id, ac_id, "Deposited", amt))
        conn.commit()
    except ValueError:
        print("Invalid input. please enter a numeric value")
    except Exception as e:
            print(e)
    return balance
def withdraw(user_id,ac_id, balance, wd_amt):
    balance -= wd_amt   
    cursor.execute('update accounts set balance = ? where account_id = ?',(balance,ac_id))
    conn.commit()
    cursor.execute('INSERT INTO transactions (user_id, account_id, type, amount) VALUES (?, ?, ?, ?)', (user_id, ac_id, "Withdrawn", wd_amt))
    conn.commit()
    return balance
# -----
def new_user(user_id):
    name = input("Enter your name: ")
    uid = name[0].capitalize()+str(randrange(1000,10000))
    print(f"Your user ID is {uid}")
    while True:
        try:
            pin = int(input("Enter a 4 digit pin: "))
            if len(str(pin)) == 4:
                break
            print("Pin should be of only 4 digits")          
        except ValueError:
            print("Invalid input. Please enter a numeric PIN.")
        except Exception as e:
            print(e)
    cursor.execute('insert into users(user_id,full_name,pin) values(?,?,?)',(uid,name,pin))
    while True:
        try:
            money = float(input("Enter first deposit amount:"))
            if money > 0:
                cursor.execute('INSERT INTO accounts(user_id, balance) VALUES (?, ?)', (uid, money))
                conn.commit()
                print("Account created with initial deposit!")
                break
            else:
                print("Balance cannot be less than or equal to zero!")
        except ValueError:
            print("Invalid input. Please enter a numeric PIN.")
        except Exception as e:
            print(e)
# -----
types = ["Deposited", "Withdrawn", "Transferred","Received"]
# -----
def fetch(tr_type, user_id, ac_id=None):
    if ac_id is not None:
        cursor.execute('SELECT * FROM transactions WHERE account_id = ? AND type = ?', (ac_id, tr_type))
    else:
        cursor.execute('SELECT * FROM transactions WHERE user_id = ? AND type = ?', (user_id, tr_type))
    rows = cursor.fetchall()
    return rows

def fet_type(n, user_id, ac_id=None):
    rows = fetch(types[n], user_id, ac_id)
    if rows:
        print(f"{'TR ID':<5} | {'User ID':<6} | {'Account ID':<10} | {'Type':<13}| {'Amount':<9} | {'Timestamp'}           |")
        print("-" * 79)
        for row in rows:
            print(f"{row[0]:<5} | {row[1]:<7} | {row[2]:<10} | {row[3]:<12} | ${row[4]:<8.2f} | {row[5]} |")
        print()
    else:
        if ac_id is not None:
            print(f"There are no entries of type {types[n]} for account {ac_id}")
        else:
            print(f"There are no entries of type {types[n]} for this user")

def hist(user_id, ac_id=None):
    if ac_id is not None:
        cursor.execute("SELECT * FROM transactions WHERE account_id = ?", (ac_id,))
    else:
        cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    if rows:
        print(f"{'TR ID':<5} | {'User ID':<6} | {'Account ID':<10} | {'Type':<13}| {'Amount':<9} | {'Timestamp'}           |")
        print("-" * 79)
        for row in rows:
            print(f"{row[0]:<5} | {row[1]:<7} | {row[2]:<10} | {row[3]:<12} | ${row[4]:<8.2f} | {row[5]} |")
    else:
        if ac_id is not None:
            print(f"There are no transactions for account {ac_id}")
        else:
            print("There are no transactions for this user")

def cat(user_id, ac_id=None):
    print("""
== Enter the category no. ==
1. Deposited
2. Withdraws
3. Transfers
4. Received
5. All
6. Exit to main menu
""")
    while True:
        try:
            choice = int(input("Enter the category number or 6 to exit: "))
            print()
            if choice == 1:
                fet_type(0, user_id, ac_id)
            elif choice == 2:
                fet_type(1, user_id, ac_id)
            elif choice == 3:
                fet_type(2, user_id, ac_id)
            elif choice == 4:
                fet_type(3, user_id, ac_id)
            elif choice == 5:
                hist(user_id, ac_id)
            elif choice == 6:
                print("Exited to account management menu")
                break
            else:
                print("Invalid Input!")
        except ValueError:
            print("Please enter a valid integer!")

def transactions(user_id):
    cursor.execute('SELECT 1 FROM transactions WHERE user_id = ? LIMIT 1', (user_id,))
    res = cursor.fetchone()
    if res:
        choice = input("Do you want to see transactions for a specific account or all accounts? (specific/all): ").lower()
        if choice == "specific":
            ac_id = int(input("Enter the account ID: "))
            cursor.execute('SELECT account_id FROM accounts WHERE account_id = ? AND user_id = ?', (ac_id, user_id))
            result = cursor.fetchone()
            if result:
                print("Account found")
                ans = input("Do you want to see your transaction history (yes/no): ").lower()
                if ans == "yes":
                    cat(user_id, ac_id)
                elif ans == "no":
                    print("Bye!")
                else:
                    print("Invalid Input!")
            else:
                print("Account not found or does not belong to you")
        elif choice == "all":
            cat(user_id)
        else:
            print("Invalid choice! Please enter 'specific' or 'all'")
    else:
        print("There are no entries found in transaction history")
# -----
def new_account(user_id):
    while True:
        try:
            money = float(input("Enter first deposit amount:"))
            if money > 0:
                cursor.execute('INSERT INTO accounts(user_id, balance) VALUES (?, ?)', (user_id, money))
                conn.commit()
                print("Account created with initial deposit!")
                # print("Amount Deposited successfully!")
                break
            else:
                print("Balance cannot be less than or equal to zero!")
        except ValueError:
            print("Invalid input. Please enter a numeric amount.")
        except Exception as e:
            print(e)

def acc_log_in(user_id,pin):
    try:
        ac_log = int(input('Enter the account id you want to log in: '))
        cursor.execute('SELECT balance FROM accounts WHERE account_id = ? AND user_id = ?', (ac_log, user_id))
        result = cursor.fetchone()
        if result:
            balance = result[0]
            main_menu(user_id, balance, ac_log, pin)
        else:
            print("Account not found or does not belong to you")
            if input("Do you want to create another account (yes/no): ").lower() == "yes":
                new_account(user_id)
                print("Bank account opened successfully!")
            else:
                print("Returning to login...")
    except ValueError:
        print("Invalid input. Please enter a numeric account ID.")

def acc_mgmt(user_id,balance,ac_id,pin):
    print("""\n ==== Account Management Menu ====
Create new account      ---> 1
Switch Account          ---> 2     
Transactions            ---> 3        
Go to banking services  ---> 4        
Exit Account Management ---> 5\n""")
    while True:



        try:
            choice = int(input("\nEnter the operation number from account management menu or 5 to exit : "))
            if choice == 1:
                new_account(user_id)            
            elif choice == 2:
                acc_log_in(user_id,pin)           
            elif choice == 3:
                transactions(user_id)
            elif choice == 4:
                banking_services(user_id, balance, ac_id,pin)            
            elif choice == 5:
                print("Account Management Exited!")
                break
        except ValueError:
            print("Invalid input. Please enter a numeric value")

def main_menu(user_id,balance, ac_id, pin):
    print("""\n ==== Main Menu ====
Account Management  ---> 1
Banking Services    ---> 2        
Exit system         ---> 3\n""")
    Exit = False
    while not Exit:
        choice = int(input("\nEnter the operation no from main menu or 3 to exit : "))
        if choice == 1:
            acc_mgmt(user_id,balance,ac_id,pin)
        elif choice ==  2:
            banking_services(user_id, balance, ac_id,pin)
        elif choice == 3:
            Exit = True
            print("system exited Successfully")
            print("👋 Goodbye!")
        pass

def transfer(user_id,ac_id, balance):
    try:
        sd_amt = float(input("Enter the transferring amount:"))
        command = cursor.execute('select * from accounts where user_id = ? AND account_id = ?',(user_id,ac_id))
        res = command.fetchone()
        if res:
            if sd_amt <= 0:
                print("Sending amount must be greater than zero")
            elif sd_amt <= balance:
                balance = send(user_id, ac_id,balance, sd_amt)
                check_balance(balance)
            else:
                check_balance(balance)
                print("Transferring amount is more than available balance")
        else:
            print("Invalid user or account ID")
    except ValueError:
        print("Invalid input! please neter a numeric value")
    return balance

def send(user_id, ac_id, balance, sd_amt):
    balance -= sd_amt
    cursor.execute('UPDATE accounts SET balance = ? WHERE account_id = ?', (balance, ac_id))
    conn.commit()
    tr_user_id = input("Enter the user id you want to send money to: ")
    cursor.execute('SELECT * FROM users WHERE user_id = ? LIMIT 1', (tr_user_id,))
    res = cursor.fetchone()
    if res:
        tr_ac_id = int(input("Enter the account id you want to send money to: "))
        cursor.execute('SELECT balance FROM accounts WHERE account_id = ? AND user_id = ? LIMIT 1', (tr_ac_id, tr_user_id))
        res = cursor.fetchone()
        if res:
            recipient_balance = res[0]  # Get recipient's current balance
            recipient_balance += sd_amt  # Add the amount
            cursor.execute('UPDATE accounts SET balance = ? WHERE account_id = ?', (recipient_balance, tr_ac_id))
        else:
            print("Recipient account not found.")
    cursor.execute(
        'INSERT INTO transactions (user_id, account_id, type, amount) VALUES (?, ?, ?, ?)',(user_id, ac_id, "Transferred", sd_amt))
    conn.commit()
    cursor.execute(
        'INSERT INTO transactions (user_id, account_id, type, amount) VALUES (?, ?, ?, ?)',(tr_user_id,tr_ac_id, "Received", sd_amt))
    conn.commit()
    return balance

log_in()

conn.close()

