from airondatarepository.datarepository import DataRepository
import test_constants

repository = DataRepository()
result = repository.delete_user(test_constants.EMAIL)

if result == False:
    print("Failed to delete")
else:
    print("Delete user succeeded")