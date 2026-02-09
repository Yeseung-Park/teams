from pydantic import BaseModel, ConfigDict


class TableResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    table_id: int
    table_number: int
    current_session_id: int | None
