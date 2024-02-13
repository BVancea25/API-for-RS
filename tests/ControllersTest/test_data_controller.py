from src.Controllers.dataController import calculate_product_profiles
from unittest.mock import patch
from src.index import app
import json
from unittest.mock import patch

def test_data():
    
    data_service_response="Profiles calculated!"
    
    with patch('src.Controllers.dataController.calculate_product_profiles_service') as mock_calculate_product_profiles_service:
        mock_calculate_product_profiles_service.return_value=data_service_response
        
        print("Is the service patched?", mock_calculate_product_profiles_service)
 
        
         
        with app.test_request_context():
            response = calculate_product_profiles()
            response_data = response[0]
    
    print("Was mocked service called?", mock_calculate_product_profiles_service.called)
    
    assert response_data.status_code == 200
    assert json.loads(str(response_data.response[0],'utf-8')) == {'message': 'Profiles calculated'}