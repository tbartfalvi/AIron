from airondatarepository.datarepository import DataRepository
from airondatarepository import encrypt
import test_constants

repository = DataRepository()
repository.test_json()

id = repository.insert_user(test_constants.FULL_NAME, test_constants.EMAIL, encrypt.encrypt_password(test_constants.PASSWORD))
print(id)

if id is not None:
    print("Test Passed")
else:
    print("Test Failed")