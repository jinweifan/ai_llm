from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
import config_data as config

import os
import json
from langchain_core.messages import BaseMessage, messages_to_dict, messages_from_dict

class FileChatMessageHistory(BaseChatMessageHistory):
    
    def __init__(self, session_id, storage_path):
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path + '.json', "r", encoding="utf-8") as f:
                messages_dict = json.load(f)
                return messages_from_dict(messages_dict)
        except FileNotFoundError:
            return []
        
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)
        messages_dict = messages_to_dict(all_messages)
        with open(self.file_path + '.json', "w", encoding="utf-8") as f:
            json.dump(messages_dict, f, ensure_ascii=False)

    def clear(self) -> None:
        self._messages = []
        with open(self.file_path + '.json', "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False)


store = {}
def get_history(session_id):
    if session_id not in store:
        store[session_id] = FileChatMessageHistory(session_id, config.chat_history_path)
    return store[session_id]


def stream_print(resp):
    for chunk in resp:
        print(chunk, end="", flush=True)
    print()
