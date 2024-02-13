from src.Controllers.userController import add_user,delete_user
from unittest.mock import patch
from src.index import app
import json
from unittest.mock import patch

def test_add_user():
    mock_data={"id":1,"name":"Bogdan"}
    
    add_user_service_response="Save successful"
    
  
    with patch('src.Controllers.userController.add_user_service') as mock_add_user_service:
        mock_add_user_service.return_value = add_user_service_response
       
        
        print("Is add_product_service patched?", mock_add_user_service)
 
        
         
        with app.test_request_context(json=mock_data):
            response = add_user()
            response_data = response[0]
    
    print("Was add_product_service called?", mock_add_user_service.called)
    
    assert response_data.status_code == 200
    assert json.loads(str(response_data.response[0],'utf-8')) == {'message': 'Save successful'}
    
def test_delete_user():
    mock_data={"id":1}
    
    delete_user_service_response="Successful deletion!"
    
  
    with patch('src.Controllers.userController.delete_user_service') as mock_delete_user_service:
        mock_delete_user_service.return_value = delete_user_service_response
       
        
        print("Is add_product_service patched?", mock_delete_user_service)
 
        
         
        with app.test_request_context(json=mock_data):
            response = delete_user()
            response_data = response[0]
    
    print("Was add_product_service called?", mock_delete_user_service.called)
    
    assert response_data.status_code == 200
    assert json.loads(str(response_data.response[0],'utf-8')) == {'message': 'Deletion successful'}
    