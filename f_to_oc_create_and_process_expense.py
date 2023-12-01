from f_to_oc_approveExpense import approveExpense
from f_to_oc_creating_transaction_on_OC import createOCexpense
from f_to_oc_update_to_paid import payExpense
from f_to_oc_check_balance import checkBalance

# Create an expense on OC
#slug = "infrastructure-2023"
#amount = 10100
#description = "test12"

def createAndProcessExpense(slug, amount, description):

    # Check to see that the project/account has sufficient funds
    balance = checkBalance(slug)

    if balance < amount:
        print("Insufficient funds")
        return "Insufficient funds"
    else:
        # Create the expense
        test = createOCexpense(slug, amount, description)

        # Approve the expense
        approved = approveExpense(test)

        # Pay the expense
        paid = payExpense(test)

        print ("The expense was created, approved and paid successfully, with id: " + test)
        return test

#test = createandprocessexpense(slug, amount, description)