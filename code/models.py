from pydantic import BaseModel


class FindChat(BaseModel):
    phone_number: str
    chat_name: str


class SendMessage(BaseModel):
    phone_number: str
    message: str
