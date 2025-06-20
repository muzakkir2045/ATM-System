# ATM System

This project is a simple ATM (Automated Teller Machine) system implemented in Python. It uses SQLite for database management and allows users to perform basic banking operations such as checking balance, depositing, withdrawing, transferring money, and managing multiple accounts.

## Features

- User authentication with a 4-digit PIN
- Multiple account management per user
- Check account balance
- Deposit money
- Withdraw money
- Transfer money between accounts
- View transaction history (filterable by type)
- Create new accounts

## Technologies Used

- Python 3.13.3
- SQLite3 (for database management)
- Python's built-in `random` module for generating user IDs

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/atm-system.git
   cd atm-system
   ```

2. **Ensure you have Python 3.x installed.** You can check this by running:
   ```bash
   python --version
   ```

3. **No additional dependencies are required** since the project uses Python's standard libraries.

4. **Run the application:**
   ```bash
   python atm_system.py
   ```

## Usage

1. **Log In:**
   - Enter your user ID (e.g., `J1234`).
   - If you don’t have an account, choose to create one by entering `yes` when prompted, then provide your name, a 4-digit PIN, and an initial deposit.
   - Enter your 4-digit PIN to log in (3 attempts allowed).

2. **Main Menu:**
   - Choose between:
     - `1` Account Management
     - `2` Banking Services
     - `3` Exit

3. **Account Management:**
   - `1` Create a new account
   - `2` Switch to another account
   - `3` View transaction history
   - `4` Go to Banking Services
   - `5` Exit Account Management

4. **Banking Services:**
   - `1` Check your balance
   - `2` Deposit money
   - `3` Withdraw money
   - `4` Transfer money to another account
   - `5` Go to Account Management
   - `6` Exit Banking Services

5. **Transaction History:**
   - View all transactions or filter by type: Deposited, Withdrawn, Transferred, Received.

6. **Exit:**
   - Select `3` from the Main Menu to exit the system.

## Database Schema

The project uses an SQLite database (`atm_system.db`) with the following tables:

- **users**
  - `user_id` (TEXT, PRIMARY KEY) - e.g., `J1234`
  - `full_name` (TEXT) - User’s full name
  - `pin` (INTEGER) - 4-digit PIN

- **accounts**
  - `account_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
  - `user_id` (TEXT, FOREIGN KEY references users(user_id))
  - `balance` (REAL, DEFAULT 0.0)

- **transactions**
  - `transaction_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
  - `user_id` (TEXT, FOREIGN KEY references users(user_id))
  - `account_id` (INTEGER, FOREIGN KEY references accounts(account_id))
  - `type` (TEXT) - e.g., Deposited, Withdrawn, Transferred, Received
  - `amount` (REAL)
  - `timestamp` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.
