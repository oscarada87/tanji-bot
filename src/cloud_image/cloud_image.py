import os
from pathlib import Path
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api
import random
import csv
from datetime import datetime

load_dotenv()

class CloudImage():
    def __init__(self) -> None:
        cloudinary.config(
            cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
            api_key=os.getenv('CLOUDINARY_API_KEY'),
            api_secret=os.getenv('CLOUDINARY_API_SECRET')
        )
        self.auth_user_file = os.path.join(Path(__file__).parents[1], './tmp/auth_user.csv')
        self.pause_group_file = os.path.join(Path(__file__).parents[1], './tmp/pause_group.csv')

    def meow(self):
        result = cloudinary.Search().expression('tags=cat').execute()
        return random.choice(result['resources'])['secure_url']

    def wang(self):
        result = cloudinary.Search().expression('tags=dog').execute()
        return random.choice(result['resources'])['secure_url']

    def upload(self, file_path, folder='undefined_species'):
        result = cloudinary.uploader.upload(file_path, folder=folder)
        return { 'public_id': result['public_id'], 'secure_url': result['secure_url'] }

    def move(self, file_public_id, folder, tags=[]):
        cloudinary.api.update(file_public_id, asset_folder=folder, tags=','.join(tags))
        if 'cat' in tags:
            return '入住卯貓窩了🏠'
        elif 'dog' in tags:
            return '入住狗勾窩了🏠'
        else:
            return '入住未知物種窩了🏠'

    def create_auth(self, password, user_id):
        if password == os.getenv('IMAGE_UPLOAD_SECRET'):
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y/%m/%d %H:%M:%S")
            with open(self.auth_user_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([user_id, formatted_time])

            return '權限已開啟'
        else:
            return '密碼錯誤'
      
    def auth(self, user_id):
        with open(self.auth_user_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == user_id:
                    return True
        
        return False
  
    def delete(self, file_public_id):
        cloudinary.api.delete_resources([file_public_id])
        return '已忽略'
    
    def pause(self, group_id):
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y/%m/%d %H:%M:%S")
        with open(self.pause_group_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([group_id, formatted_time])

        return '此群組已暫停上傳功能'
  
    def resume(self, group_id):
        with open(self.pause_group_file, 'rb') as inp, open(self.pause_group_file, 'wb') as out:
          writer = csv.writer(out)
          for row in csv.reader(inp):
              if row[0] != group_id:
                  writer.writerow(row)

        return '此群組已開啟上傳功能'
    
    def is_paused(self, group_id):
        with open(self.pause_group_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == group_id:
                    return True
        
        return False