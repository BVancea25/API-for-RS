

from src.Controllers.productController import add_product,delete_product

from unittest.mock import patch
from src.index import app
import json
from unittest.mock import patch



def test_add_product():
    mock_data={"id":10,"name":"NikeTest","color":"blue","type":"flipflops","description":"Testing controller","brand":"nike"}
    
    add_product_service_response="Saved product!"
    
  # Mocking the add_product_service function
    with patch('src.Controllers.productController.add_product_service') as mock_add_product_service:
        mock_add_product_service.return_value = add_product_service_response
       
        
        print("Is the service patched?", mock_add_product_service)
 
        
         
        with app.test_request_context(json=mock_data):
            response = add_product()
            response_data = response[0]
    
    print("Was add_product_service called?", mock_add_product_service.called)
    
    assert response_data.status_code == 200
    assert json.loads(str(response_data.response[0],'utf-8')) == {'message': 'Save successful'}
    
def test_delete_product():
    
    mock_data={"id":5}
    
    with patch('src.Controllers.productController.delete_product_service') as mock_delete_product_service:
        mock_delete_product_service.return_value="Product deletion successful!"
        
        with app.test_request_context(json=mock_data):
            response=delete_product()
            response_data = response[0]
    
    
    print(response)
    print(str(response_data.response[0],'utf-8'))
    assert response_data.status_code == 200
    assert json.loads(str(response_data.response[0],'utf-8')) == {'message': 'Deletion successful'}
        
    