from revChatGPT.V1 import Chatbot
import os
from dotenv import load_dotenv

load_dotenv()

class ChatGpt():
  def __init__(self) -> None:
    self.chatbot = Chatbot(config={
      "session_token": os.getenv('CHATGPT_SESSION_TOKEN')}
    )

  def ask(self, prompt: str) -> str:
    response = ''
    for data in self.chatbot.ask(prompt):
      response = data['message']
    # print(response)
    return response


if __name__ == '__main__':
  a = ChatGpt()
  z = a.ask('說一句台灣名言')
  print(z)
  # print('測試非同步')