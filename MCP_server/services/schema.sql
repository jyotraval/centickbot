-- users table
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE
);

-- Tickets table
DROP TABLE IF EXISTS tickets CASCADE;
CREATE TABLE tickets (
  id SERIAL PRIMARY KEY,
  seatid TEXT NOT NULL,
  userid INTEGER NOT NULL,
  amount DECIMAL(10, 2) NOT NULL, -- price of the ticket
  status TEXT NOT NULL CHECK(status IN ('booked', 'vacant', 'processing')),
  booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (userid) REFERENCES users(id)
);

-- Transactions table
DROP TABLE IF EXISTS transactions CASCADE;
CREATE TABLE transactions (
  id SERIAL PRIMARY KEY,
  ticket_id INTEGER NOT NULL,
  userid INTEGER NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  refund BOOLEAN DEFAULT FALSE,
  txntime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (ticket_id) REFERENCES tickets(id),
  FOREIGN KEY (userid) REFERENCES users(id)
);

-- Refunds table
DROP TABLE IF EXISTS refunds CASCADE;
CREATE TABLE refunds (
  id SERIAL PRIMARY KEY,
  txn_id INTEGER NOT NULL,
  state TEXT NOT NULL CHECK(state IN ('done', 'pending', 'rejected')),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (txn_id) REFERENCES transactions(id)
);

-- Support Tickets table
DROP TABLE IF EXISTS support_tickets CASCADE;
CREATE TABLE support_tickets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('open', 'closed', 'in_progress')) DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);