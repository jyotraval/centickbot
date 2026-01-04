from services.db import db

class BookingService:
    
    def get_available_seats(self):
        """Get list of all available (vacant) seats with prices"""
        # getting all vacent seats along with price tag
        # somehing like select * from tickets where status is vacant
        query = """
            SELECT seatid, amount 
            FROM tickets 
            WHERE status = 'vacant'
            ORDER BY seatid
        """
        results = db.execute_query(query)
        # return formated list with price
        return [{"seat_id": row['seatid'], "price": row['amount']} for row in results]
    
    def book_ticket(self, userid: int, seatid: str):
        """
        Book a ticket for a user. Price is taken from the DB.
        Returns: dict with booking details including txnid
        """
        # Cheking if seat is availble or not
        check_query = """
            SELECT id, amount FROM tickets 
            WHERE seatid = %s AND status = 'vacant'
            LIMIT 1
        """
        existing = db.execute_query(check_query, (seatid,))
        
        # if not esxit then return error
        if not existing:
            return {
                "success": False,
                "error": f"Seat {seatid} is already booked or does not exist"
            }
        
        ticket_id = existing[0]['id']
        amount = existing[0]['amount']

        # check if user is valid
        user_query = "SELECT id FROM users WHERE id = %s"
        user = db.execute_query(user_query, (userid,))
        if not user:
            return {
                "success": False,
                "error": f"User {userid} does not exist"
            }
        
        # Update ticket status to booked
        # keeping original amount intact
        update_query = """
            UPDATE tickets 
            SET userid = %s, status = 'booked', booked_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        db.execute_update(update_query, (userid, ticket_id))
        
        # Create transaction record
        # inserting into transaction table
        txn_query = """
            INSERT INTO transactions (ticket_id, userid, amount, refund)
            VALUES (%s, %s, %s, FALSE)
            RETURNING id
        """
        txn_id = db.execute_update(txn_query, (ticket_id, userid, amount))
        
        return {
            "success": True,
            "txnid": txn_id,
            "ticket_id": ticket_id,
            "seatid": seatid,
            "amount": amount,
            "message": f"Ticket booked successfully! Price: {amount}. Your transaction ID is {txn_id}"
        }
    

    ###################
    def get_booking(self, booking_id: str):
        """
        Get booking details by transaction ID
        booking_id is the txnid
        """
        query = """
            SELECT  
                t.id as txnid, t.amount, t.refund, t.txntime, 
                tk.id as ticket_id, tk.seatid, tk.status, tk.booked_at,
                u.name, u.email
            FROM transactions t
            JOIN tickets tk ON t.ticket_id = tk.id
            JOIN users u ON t.userid = u.id
            WHERE t.id = %s
        """
        results = db.execute_query(query, (booking_id,))
        
        if not results:
            return {
                "success": False,
                "error": f"Booking with transaction ID {booking_id} not found"
            }
        # print(results)
        row = results[0]
        return {
            "success": True,
            "booking": dict(row)
        }
    
    def list_user_bookings(self, user_id: str):
        """List all bookings for a user"""
        query = """
            SELECT 
                t.id as txnid, t.amount, t.refund, t.txntime,
                tk.seatid,tk.status, tk.booked_at
            FROM transactions t
            JOIN tickets tk ON t.ticket_id = tk.id
            WHERE t.userid = %s
            ORDER BY t.txntime DESC
        """
        results = db.execute_query(query, (user_id,))
        # print(results, len(results))
        if not results:
            return {
                "success": False,
                "error": f"No bookings found for user {user_id}"
            }
        return {
            "success": True,
            "bookings": [dict(row) for row in results]
        }
    
    def cancel_booking(self, booking_id: str, reason: str = "user_request"):
        """
        Cancel a booking and initiate refund
        booking_id is the txnid
        """
        # Get booking details
        booking_result = self.get_booking(booking_id)
        
        if not booking_result["success"]: # if false then return not booking
            return booking_result
        
        booking = booking_result["booking"]
        
        # if vacant then return already cannot refund if in processing cannot do anyhting user must wait untill state changes.
        if booking["status"] in ("vacant" , 'processing'): 
            return {
                "success": False,
                "error": "Seat is already vacant. Cannot refund on seat which is not booked. False claim"
            }
        
        # If seat no vanct and in txn then chekc if refund dont then refund cannot happen twice
        if booking["refund"]:
            return {
                "success": False,
                "error": "Booking is already refunded"
            }
        
        # everthing is rightn procced to refund policy .previous approch api call with vector db check if reson comply with policy then proceed to refund else no refund.

        # previce appcoh api call

        # policy is right, applicable to refund then -->

        ticket_id = booking["ticket_id"]
        amount = booking["amount"]
        
        # update ticket ->  vacant
        update_ticket = """
            UPDATE tickets 
            SET status = 'vacant'
            WHERE id = %s
        """
        db.execute_update(update_ticket, (ticket_id,))
        
        # Update original txn data to mark as refunded
        update_txn = """
            UPDATE transactions
            SET refund = TRUE
            WHERE id = %s
        """
        db.execute_update(update_txn, (booking_id,))

        refund_query = """
            INSERT INTO refunds (txn_id, state)
            VALUES (%s, 'pending')
            RETURNING id
        """
        refund_id = db.execute_update(refund_query, (booking_id,))
        
        return {
            "success": True,
            "message": f"Booking cancelled and refund processed",
            "refund_id": refund_id,
            "refund_amount": amount,
            "refund_status": "pending",
            "reason": reason
        }

        