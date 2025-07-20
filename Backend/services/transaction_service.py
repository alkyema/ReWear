from firebase_admin import db
from datetime import datetime
from services.firebase_config import initialize_firebase

class SwapTransactionService:
    def __init__(self):
        initialize_firebase()
        self.ref = db.reference("items")

    def swap_items(self, item_id_1: str, item_id_2: str):
        def transaction_logic(current_data):
            if not current_data:
                return None  # One of the items doesn't exist

            # Extract both items
            item1 = current_data.get(item_id_1)
            item2 = current_data.get(item_id_2)

            if not item1 or not item2:
                return None  # Abort if either item is missing

            if item1["status"] != "Available" or item2["status"] != "Available":
                return None  # Abort if either is not available

            # Mark both as swapped
            item1["status"] = "Swapped"
            item2["status"] = "Swapped"

            # Optionally, add swap info
            item1["swapped_with"] = item_id_2
            item2["swapped_with"] = item_id_1

            current_data[item_id_1] = item1
            current_data[item_id_2] = item2

            return current_data

        # Apply transaction
        result = self.ref.transaction(transaction_logic)
        if result is None:
            raise ValueError("Transaction failed due to item unavailability or missing data.")
        return True
