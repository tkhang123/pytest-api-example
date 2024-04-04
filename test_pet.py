from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: FIXED: schemas.py had "integer" instead of "string" for "name.type"
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''
def test_pet_schema():
    # TODO: Should probably add a check here to make sure the id exists?
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py
    validate(instance=response.json(), schema=schemas.pet)

'''
TODO: Finish this test by...
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''
# TODO: 1) Extending the parameterization to include all available statuses
@pytest.mark.parametrize("status", [("available"), ("pending"), ("sold")])
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    response = api_helpers.get_api_data(test_endpoint, params)
    # TODO: 2) Validate the appropriate response code
    assert response.status_code == 200

    pets = response.json()
    for pet in pets:
        # TODO: 3) Validate the 'status' property in the response is equal to the expected status
        assert params["status"] == pet["status"]
        # TODO: 4) Validate the schema for each object in the response
        validate(instance=pet, schema=schemas.pet)


'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''
# TODO: 2) Parameterizing the test for any edge cases, since schema says "integer", tried -1 and marked it as xfail
@pytest.mark.parametrize("id, expected_code", [(0, 200),                                            # expected success
                                               (5, 404),                                            # expected failure
                                               pytest.param(-1, 200, marks=pytest.mark.xfail),      # expected sucess, but needs investigation
                                               pytest.param("A", 404, marks=pytest.mark.xfail)])    # expected failure, but needs investigation
def test_get_by_id_404(id, expected_code):
    # TODO: Should probably add a check here to make sure the id exists?
    test_endpoint = "/pets/" + str(id)

    response = api_helpers.get_api_data(test_endpoint)
    print(response.json())
    # TODO: 1) Validate the appropriate response code
    assert response.status_code == expected_code


# OTHER BUGS:
# 1) Was able to create duplicate pet ids with a string like "0", backend needs to validate the is input is a integer
# [
#   {
#     "id": 0,
#     "name": "snowball",
#     "type": "cat",
#     "status": "available"
#   },
#   {
#     "id": 1,
#     "name": "ranger",
#     "type": "dog",
#     "status": "pending"
#   },
#   {
#     "id": 2,
#     "name": "flippy",
#     "type": "fish",
#     "status": "available"
#   },
#   {
#     "id": 0,
#     "name": "test2",
#     "type": "cat",
#     "status": "available"
#   }
# ]
#
# 2) Was able to create pet with negative integers like "-1", backend needs to validate the positive integers only
# [
#   {
#     "id": 0,
#     "name": "snowball",
#     "type": "cat",
#     "status": "available"
#   },
#   {
#     "id": 1,
#     "name": "ranger",
#     "type": "dog",
#     "status": "pending"
#   },
#   {
#     "id": 2,
#     "name": "flippy",
#     "type": "fish",
#     "status": "available"
#   },
#   {
#     "id": -1,
#     "name": "test2",
#     "type": "cat",
#     "status": "available"
#   }
# ]
#
#3) The Order model "id" should probably be an integer.