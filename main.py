import os
from mongo.mongo_controller import connectToMongoAndReturnClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

def print_hi(name):
    print(f'Hi, {name}') 

if __name__ == '__main__':
    connectToMongoAndReturnClient(MONGO_URI)
    print_hi('GOT THEM')
