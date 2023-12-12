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
        expense = createOCexpense(slug, amount, description)

        # Approve the expense
        approved = approveExpense(expense)

        # Pay the expense
        paid = payExpense(expense)

        print ("The expense was created, approved and paid successfully, with amount: "+str(amount)+", at project with slug: "+slug)
        #length of an id from open collective is 35 characters, that is being returned
        return expense

#test = createAndProcessExpense("granslandet", "10000000", "reduce funds")
#print(test)