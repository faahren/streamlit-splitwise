import os

from splitwise import Splitwise
from splitwise.expense import Expense

class SplitwiseService:
    def __init__(self):
        self.SplitwiseManager = Splitwise(os.getenv('splitwise_key'), os.getenv('splitwise_secret'),api_key=os.getenv('splitwise_api_key'))
    
    def getUser(self):
        return self.SplitwiseManager.getCurrentUser()

    def send_to_sw(self, expense):
        exp = Expense()
        exp.setCost(expense['Debit'])
        exp.setDate(expense['Date'])
        exp.setDescription(expense['Description'] + " - " + expense['Categorie'])
        exp.setSplitEqually(True)
        exp.setGroupId(os.getenv("splitwise_group_id"))
        exp, errors = self.SplitwiseManager.createExpense(exp)
        if errors:
            print(errors.getErrors())
        return exp.getId()