# dummy.py
import random
import os
from services.db import db

def create_tables():
    print("Reading schema.sql...")
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    print("Executing schema...")
    # executing strictly as per schema.sql
    # creating tables one by one
    db.execute_update(schema_sql)
    print("Tables created/verified.")

def main():
    print("Starting dummy data insertion...")
    
    # Ensure tables exist
    create_tables()

    # -----------------------
    # Insert Users
    # -----------------------
    users = [
        ("Alice Johnson", "alice@example.com"),
        ("Bob Smith", "bob@example.com"),
        ("Charlie Brown", "charlie@example.com"),
        ("Diana Prince", "diana@example.com"),
    ]

    print("Inserting users...")
    for user in users:
        # PostgreSQL specific conflict handling for seeding
        db.execute_update(
            "INSERT INTO users (name, email) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING;",
            user
        )

    # Fetch user ids
    users_data = db.execute_query("SELECT id FROM users;")
    
    if not users_data:
        print("No users found. Aborting.")
        return

    user_ids = [row['id'] for row in users_data]

    # -----------------------
    # Insert Tickets
    # -----------------------
    statuses = ["booked", "vacant", "processing"]
    tickets = []

    for i in range(1, 11):
        seatid = f"A{i}"
        userid = random.choice(user_ids)
        amount = round(random.uniform(50, 200), 2)
        status = random.choice(statuses)
        tickets.append((seatid, userid, amount, status))

    print("Inserting tickets...")
    for ticket in tickets:
        db.execute_update(
            """
            INSERT INTO tickets (seatid, userid, amount, status)
            VALUES (%s, %s, %s, %s);
            """,
            ticket
        )

    # Fetch ticket ids
    ticket_rows = db.execute_query("SELECT id, userid, amount, status FROM tickets WHERE status = 'booked';") # transactions only for booked tickets

    # -----------------------
    # Insert Transactions
    # -----------------------
    transactions = []

    for row in ticket_rows:
        is_refund = bool(random.choice([0, 1]))
        transactions.append(
            (row['id'], row['userid'], row['amount'], is_refund)
        )

    print("Inserting transactions...")
    for txn in transactions:
        db.execute_update(
            """
            INSERT INTO transactions (ticket_id, userid, amount, refund)
            VALUES (%s, %s, %s, %s);
            """,
            txn
        )

    # Fetch transaction ids
    txn_rows = db.execute_query("SELECT id, refund FROM transactions;")

    # -----------------------
    # Insert Refunds
    # -----------------------
    refund_states = ["done", "pending", "rejected"]
    refunds = []

    for row in txn_rows:
        if row['refund']:
            refunds.append(
                (row['id'], random.choice(refund_states))
            )

    print("Inserting refunds...")
    for refund in refunds:
        db.execute_update(
            """
            INSERT INTO refunds (txn_id, state)
            VALUES (%s, %s);
            """,
            refund
        )

    # -----------------------
    # Insert Support Tickets
    # -----------------------
    support_categories = ["billing", "technical", "general"]
    support_tickets = []
    
    for _ in range(5):
        uid = random.choice(user_ids)
        cat = random.choice(support_categories)
        msg = f"This is a {cat} issue."
        support_tickets.append((uid, cat, msg))

    print("Inserting support tickets...")
    for ticket in support_tickets:
         db.execute_update(
            """
            INSERT INTO support_tickets (user_id, category, message)
            VALUES (%s, %s, %s);
            """,
            ticket
        )

    print("Dummy data inserted successfully.")

if __name__ == "__main__":
    main()
