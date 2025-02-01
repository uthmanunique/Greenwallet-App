# Fintech Backend

This is a FastAPI backend application for a fintech platform that includes functionalities for user management, wallet and transactions, virtual card management, and transaction history. The application uses MongoDB as the database and integrates with the Flutterwave API for payment processing.

## Features

- User Management
  - Register
  - Login
  - Fetch Profile
  - Update Profile
  - KYC Verification

- Wallet Management
  - Fetch Balance
  - Top Up
  - Transfer Money
  - Withdraw Funds
  - Convert Currency

- Transaction Management
  - Fetch All Transactions
  - Transaction Details

- Virtual Card Management
  - Create Card
  - List Cards
  - Fund Card
  - Delete Card

## Technologies Used

- FastAPI
- MongoDB
- Pydantic
- Flutterwave API

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd fintech-backend
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your MongoDB database and update the connection details in `src/utils/database.py`.

5. Run the application:
   ```
   uvicorn src.main:app --reload
   ```

## API Endpoints

Refer to the individual route files in the `src/routes` directory for detailed API endpoints and their usage.

## Usage Guidelines

- Ensure that you have a valid Flutterwave account and API keys for payment processing.
- Follow the documentation in each controller and service for implementing specific functionalities.

## License

This project is licensed under the MIT License.