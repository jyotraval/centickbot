from services.db import db

class SupportService:
    """
    Human support escalation logic.
    """

    def create_ticket(self, user_id: str, category: str, message: str):
        # Create support ticket in DB
        # just inserting basic details
        query = """
            INSERT INTO support_tickets (user_id, category, message)
            VALUES (%s, %s, %s)
            RETURNING id, status
        """
        try:
            # execute_update in db.py handles commit, but typically returns last row id for maily sqlite
            # for Postgres with RETURNING, we might need to adjust db.py or use execute_query if we want the returned row.
            # les check db.py capability. It says: 
            # "iif the query has 'RETURNING id', we fetch it." -> returns last row id.
            # bbut here we want id and status. 
            # just rely on returning ID for now to be safe with existing db.py logic which seems tailored for single return.
            # wait, db.py logic:
            # if cursor.description: res = cursor.fetchone(); lastrowid = list(res.values())[0]
            # So it returns the FIRST column of the result.
            
            # executing update now
            ticket_id = db.execute_update(query, (user_id, category, message))
            
            return {
                "success": True,
                "ticket_id": ticket_id,
                "status": "open",
                "message": "Support ticket created successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
