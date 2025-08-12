from app.calcs import add, subtract, multiply, divide, BankAccount
import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)



@pytest.mark.parametrize("num1, num2, result", [
    (3, 2, 5),
    (7,1,8),
    (12,4,16)
])
def test_add(num1, num2, result):
    assert add(num1,num2) == result

def test_subtract():
    assert subtract(9,4) == 5

def test_multiply():
    assert multiply(2, 3) == 6

def test_divide():
    assert divide(10,2) == 5

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_balance(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 40

def test_deposit(bank_account):
    bank_account.deposit(10)
    assert bank_account.balance == 60

def test_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

def test_bank_transaction(zero_bank_account):
    zero_bank_account.deposit(200)
    zero_bank_account.withdraw(150)
    assert zero_bank_account.balance == 50