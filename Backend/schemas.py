
# sh
from typing import List, Optional
from pydantic import BaseModel

class SwapInfo(BaseModel):
    request_from_user_id: str  # updated to string
    requested_item_id: str
    target_item_id: str
    status: str = "pending"  # pending, accepted, rejected, completed

class ItemCreate(BaseModel):
    user_id: str                     # changed from int to str
    title: str
    description: str
    category: str
    type: str
    size: str
    condition: str
    status: str
    image_urls: List[str]
    is_approved: bool
    points: int = 0
    swap_info: Optional[SwapInfo] = None

class ItemOut(ItemCreate):
    id: str
    created_at: str
