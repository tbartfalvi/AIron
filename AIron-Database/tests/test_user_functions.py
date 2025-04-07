from airondatarepository.datarepository import DataRepository
import test_constants

repository = DataRepository()

print("Begin test insert_user")
id = repository.insert_user(test_constants.FULL_NAME, test_constants.EMAIL, test_constants.PASSWORD)

if id is not None:
    print(id)
    print("Test insert_user: Passed")

    print("Begin test user_exists")
    user_exists_result = repository.user_exsits(id)

    if user_exists_result == False:
        print("Test user_exists: Failed")
    else:
        print("Test user_exists: Passed")

    print("Begin test login")
    login_result = repository.login(test_constants.EMAIL, test_constants.PASSWORD)

    if login_result:
        print("Test login: Passed")
    else:
        print("Test login: Failed")

    print("Begin test get_user")
    get_user_result = repository.get_user(id)
    print(get_user_result)

    if get_user_result:
        print("Test get_user: Passed")
    else:
        print("Test get_user: Failed")

    print("Begin test delete_user")
    delete_result = repository.delete_user(id)

    if delete_result == False:
        print("Test delete_user: Failed")
    else:
        print("Test delete_user: Passed")
else:
    print("Test insert_user: Failed")