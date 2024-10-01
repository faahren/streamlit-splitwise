from dotenv import load_dotenv

load_dotenv()
from services.splitwise import SplitwiseService

print(SplitwiseService().get_latest_expenses())