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

    print("Begin test add_schedule")
    add_schedule_result = repository.add_schedule(id, test_constants.NAME, test_constants.TYPE, test_constants.JSON)

    if add_schedule_result:
        print("Test add_schedule: Passed")

        print("Begin test get_schedule_by_user")
        get_schedule_by_user_result = repository.get_schedules_by_user(id)

        if len(get_schedule_by_user_result) > 0:
            print("Test get_schedule_by_user: Passed")
            
            for sched in get_schedule_by_user_result:
                sched_id = sched['id']
                
                print("Begin test get_schedule_by_id")
                get_schedule_by_id_result = repository.get_schdule_by_id(id, sched_id)

                if get_schedule_by_id_result:
                    print(get_schedule_by_id_result)
                    print("Test get_schedule_by_id: Passed")
                else:
                    print("Test get_schedule_by_id: Failed")
        else:
            print("Test get_schedule_by_user: Failed")

    else:
        print("Test add_schedule: Failed")

    print("Begin test delete_user")
    delete_result = repository.delete_user(id)

    if delete_result == False:
        print("Test delete_user: Failed")
    else:
        print("Test delete_user: Passed")
else:
    print("Test insert_user: Failed")