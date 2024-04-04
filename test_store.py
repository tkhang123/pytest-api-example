from jsonschema import validate
import random
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''
# TODO: 2) *Optional* Consider using @pytest.fixture to create unique test data for each run
# Function to create a new pet with a random pet_id
@pytest.fixture
def create_new_pet():
    endpoint = "/pets/"
    rand_id = random.randrange(10000, 20000)
    payload = {
        "id": str(rand_id),
        "name": "test_" + str(rand_id),
        "type": "cat",
        "status": "available"
    }

    post_response = api_helpers.post_api_data(endpoint, data=payload)
    return post_response.json()["id"]

# Function to create an order using the new_pet_id and return the uuid
def get_order_id(new_pet_id):
    # time.sleep(5)
    post_order_endpoint = "/store/order"
    post_order_payload = {
        "pet_id": str(new_pet_id)
    }

    post_response = api_helpers.post_api_data(post_order_endpoint, data=post_order_payload)
    return post_response.json()["id"]

# PATCH the "status" of an order.  Had to create a new pet to get a unique pet_id and order_id since there is no api
# to get the order_id.  Using parametrized varibles to test multiple iterations of status and expected status_code. 
@pytest.mark.parametrize("status, expected_code", [("available", 200), 
                                                   ("pending", 200), 
                                                   ("sold", 200), 
                                                   ("invalid status", 400), 
                                                   ("invalid order", 404) ])
def test_patch_order_by_id(create_new_pet, status, expected_code):
    if (status == "available" or status == "sold" or status == "pending"):
        id = get_order_id(create_new_pet)
        stat = status
        expected_message = "Order and pet status updated successfully"
    elif status == "invalid status":
        id = get_order_id(create_new_pet)
        stat = "invalid status"
        expected_message = "Invalid status 'invalid status'. Valid statuses are available, sold, pending"
    else:
        id = "invalid"
        stat = status
        expected_message = 'Order not found. You have requested this URI [/store/order/invalid] but did you mean /store/order/<string:order_id> or /store/order ?'
    # Create an unique order_id and it's endpoint
    test_endpoint = "/store/order/" + id
    payload = {
        "status": stat
    }

    # Send PATCH request with payload
    response = api_helpers.patch_api_data(test_endpoint, data=payload)

    # TODO: 3) Validate the response codes and values
    assert response.status_code == expected_code
    # TODO: 4) Validate the response message "Order and pet status updated successfully"
    print(response.json())
    assert response.json()["message"] == expected_message
