from services.db import db

class RefundService:
    
    def get_refund_status(self, booking_id: str):
        """
        Get refund status for a booking
        booking_id is the txnid
        """
        query = """
            SELECT 
                t.id as txnid, t.amount, t.refund, t.txntime,
                tk.seatid, tk.status,
                u.name, u.email,
                r.id as refund_id, r.state as refund_state, r.created_at as refund_requested_at, r.updated_at as refund_updated_at
            FROM transactions t
            JOIN tickets tk ON t.ticket_id = tk.id
            JOIN users u ON t.userid = u.id
            LEFT JOIN refunds r ON r.txn_id = t.id
            WHERE t.id = %s
        """
        results = db.execute_query(query, (booking_id,))
        
        if not results:
            return {
                "success": False,
                "error": f"Transaction ID {booking_id} not found."
            }
        # print(results)
        row = dict(results[0])
        
        # Check if refund exists
        if row["refund_id"]:
            state = row["refund_state"]
            
            # if state is done that means money is back
            if state == "done":
                return {
                    "success": True,
                    "refund_status": "completed",
                    "message": "Refund has been processed successfully",
                    "refund_details": {
                        "refund_id": row["refund_id"],
                        "state": state,
                        "amount": row["amount"],
                        "requested_at": row["refund_requested_at"],
                        "completed_at": row["refund_updated_at"]
                    },
                    "booking": row
                }
            
            # if still pending then we tell user to wait
            elif state == "pending":
                return {
                    "success": True,
                    "refund_status": "pending",
                    "message": "Your refund request is under review. Our team will contact you shortly.",
                    "refund_details": {
                        "refund_id": row["refund_id"],
                        "state": state,
                        "amount": row["amount"],
                        "requested_at": row["refund_requested_at"]
                    },
                    "booking": row
                }
            
            # if rejected then we tell user to contact support
            elif state == "rejected":
                return {
                    "success": True,
                    "refund_status": "rejected",
                    "message": "Your refund request has been rejected. Please contact support for details.",
                    "refund_details": {
                        "refund_id": row["refund_id"],
                        "state": state,
                        "amount": row["amount"],
                        "requested_at": row["refund_requested_at"],
                        "rejected_at": row["refund_updated_at"]
                    },
                    "booking": row
                }
        
        # No refund initiated till now
        return {
            "success": True,
            "refund_status": "not_initiated",
            "booking": row,
            "message": "No refund has been requested for this booking"
        }
    
