from services.booking_service import BookingService
from services.refund_service import RefundService
from services.support_service import SupportService
from services.db import db
import time

def verify_flow():
    print("--- Starting Flow Verification ---")
    booking_svc = BookingService()
    refund_svc = RefundService()
    support_svc = SupportService()

    # 1. Check Availability
    print("\n1. Checking Available Seats:")
    seats = booking_svc.get_available_seats()
    print(f"   Available seats: {seats}")
    if not seats:
        print("   [WARNING] No seats available to book!")
        return

    # 2. Book a Ticket
    seat_info = seats[0]
    seat_to_book = seat_info['seat_id']
    price = seat_info['price']

    # Fetch a valid user ID from DB
    user_res = db.execute_query("SELECT id FROM users LIMIT 1")
    user_id = user_res[0]['id']
    
    print(f"\n2. Booking seat {seat_to_book} (Price: {price}) for user {user_id}...")
    booking_res = booking_svc.book_ticket(user_id, seat_to_book)
    print(f"   Response: {booking_res}")
    
    if not booking_res["success"]:
        print("   [FAIL] Booking failed.")
        return
    
    booking_id = booking_res["txnid"] # txnid is the booking identifier used in other calls

    # 3. Verify Booking
    print(f"\n3. Verifying Booking Details for ID {booking_id}...")
    details = booking_svc.get_booking(booking_id)
    print(f"   Details: {details}")
    if not details["success"]:
         print("   [FAIL] Could not fetch booking.")
         return

    # 4. Cancel Booking (Refund)
    print(f"\n4. Cancelling Booking {booking_id}...")
    cancel_res = booking_svc.cancel_booking(booking_id, "changed my mind")
    print(f"   Response: {cancel_res}")
    if not cancel_res["success"]:
        print("   [FAIL] Cancellation failed.")

    # 5. Check Refund Status
    print(f"\n5. Checking Refund Status for {booking_id}...")
    refund_res = refund_svc.get_refund_status(booking_id)
    print(f"   Response: {refund_res}")
    # Status should be pending or done (depending on how logic handles it, dummydb inserted 'pending' for fresh refunds)

    # 6. Create Support Ticket
    print("\n6. Creating Support Ticket...")
    support_res = support_svc.create_ticket(user_id, "technical", "I need help with my refund")
    print(f"   Response: {support_res}")
    if not support_res["success"]:
        print("   [FAIL] Support ticket creation failed.")

    print("\n--- Flow Verification Complete ---")

if __name__ == "__main__":
    verify_flow()
