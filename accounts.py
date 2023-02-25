

from random import randint
from datetime import date
issued_CardNo=[] #List that stores the whole info of all card Number issued by bank(used inorder to prevent card number duplicates )
account_series = [0] 
class BasicAccount:
    #Basic Account consists of account name,account number,balance,issued card number with card expiry dates
    #Initialiser giving the account name and opening balance.
    def __init__(self,acName,openingBalance):
        self.name=acName
        self.balance=openingBalance
        self.acNum=1 + account_series[-1] #assign serial values to account number
        account_series.append(self.acNum)
        
        
    def __str__(self):
        return "This account belong to {self.name}, and has available balance of {self.balance}".format(self=self)
    
    #Deposits the stated amount into the account, and adjusts the balance appropriately.
    def deposit(self,amount):
        if (amount<0):
            print("Please deposit a positive value")
            return
        self.balance +=amount
        if (self.balance>=0 and type(self) == PremiumAccount):
            self.setOverdraftLimit(self.oldlimit) #resets the overdraftlimit once user has cleared his dues
            self.overdraft=False# Overdraft boolen variable set to false denoting user has not overdraft
        elif (self.balance<0 and type(self) == PremiumAccount):
             self.setOverdraftLimit(self.overdraftLimit+amount)#updates overdraftlimit once user has deposited some amount,but has not cleared all his dues
             
    #Withdraws the stated amount from the account
    def withdraw(self,amount):
     if(type(self)==BasicAccount):
        if (amount>self.balance):
            print("Can not withdraw £",amount)
        else:
            self.balance-=amount
            
            print("{} has withdrawn £{}.Newbalance is £{}".format(self.name,amount,self.balance))
     elif(type(self)==PremiumAccount):
        if (amount>self.getAvailableBalance()):
            print("Can not withdraw £",amount)
            
        else:
            self.balance-=amount
            if(self.balance<0):
              self.overdraftLimit +=self.balance #updates overdraft limit after withdrawal
              self.overdraft=True # sets overdraft as true,denoting user has taken overdraft
            print("{} has withdrawn £{}.Newbalance is £{}".format(self.name,amount,self.balance))
    
    #Returns the total balance that is available in the account as a float. 
    def getAvailableBalance(self):
          return(self.getBalance())

   #Returns the balance of the account as a float.
    def getBalance(self):
         return(self.balance)

    #Prints in a sensible way the balance of the account.
    def printBalance(self):
        print("Account Balance is: {self.balance}".format(self=self))

    #Returns the name of the account holder as a string.    
    def getName(self):
        return self.name
    
    #Returns the account number as a string.
    def getAcNum(self):
        return str(self.acNum)
    
    #Creates a new card number, with the expiry date being 3 years to the month from now
    def issueNewCard(self):
        while True:
            x= str(randint((10**15),(10**16)-1))
            if x not in issued_CardNo:
                self.cardNum = x
                issued_CardNo.append(x)
                break
            else:
                continue
        today = date.today()
        expyear = (today.year +3) % 100
        self.cardExp = (today.month,expyear)

    #Returns any balance to the customer (via the withdraw method) and returns True.
    def closeAccount(self):
        self.withdraw(self.getBalance())
        print("Account has been closed successfully")
        return True

class PremiumAccount(BasicAccount):
    #Premium Account is child class of Basic Account and inherits all its properties and also has additional info such as overdraftlimit
    def __init__(self,acName,openingBalance,initialOverdraft):
        super().__init__(acName,openingBalance)
        self.oldlimit = initialOverdraft
        self.overdraftLimit = initialOverdraft
        self.overdraft = False
    
    def __str__(self):
        return "This account belong to {self.name}, and has available balance of {self.balance} and overdraftlimit of {self.overdraftLimit}".format(self=self)
        
    #Sets the overdraft limit to the stated amount
    def setOverdraftLimit(self,newLimit):
        self.overdraftLimit = newLimit
    
    #Returns the total balance that is available in the account as a float. It takes into account any overdraft that is available.
    def getAvailableBalance(self):
        if self.overdraft: #If user has overdraft displays the remaining overdraftlimit
         return(self.overdraftLimit)
        else: #Else display the total balance along with overdraftlimit
         return(self.getBalance()+self.overdraftLimit)
    
    #Prints in a sensible way the balance of the account. If an overdraft is available, then it is also printed and shows how much overdraft is remaining.
    def printBalance(self):
        print("Account Balance is: {self.balance}".format(self=self))
        print("Remaining Overdraft limit is : {self.overdraftLimit}".format(self=self))
    
    #Returns any balance to the customer (via the withdraw method) and returns True.
    #Returns False if the customer is in debt to the bank, and prints message “Can not close account due to customer being overdrawn by £<amount>”.
    def closeAccount(self):
        if self.overdraft:
            print("Can not close account due to customer being overdrawn by £",-self.getBalance())
            return False
        else:
         self.withdraw(self.getBalance())
         print("Account has been closed successfully")
         return True





