from src.Controllers.relationController import add_relation
from unittest.mock import patch
from src.index import app
import json
from unittest.mock import patch

def test_add_relation():
    
    
    add_rel_service_response="Relationship created !"
    
  
    with patch('src.Controllers.relationController.add_relation_service') as mock_add_rel_service:
        mock_add_rel_service.return_value = add_rel_service_response
       
        
        print("Is add_product_service patched?", mock_add_rel_service)
 
        
         
        with app.test_request_context():
            response = add_relation()
            response_data = response[0]
    
    print("Was add_product_service called?",mock_add_rel_service.called)
    
    assert response_data.status_code == 200
    assert json.loads(str(response_data.response[0],'utf-8')) == {'message': 'Relation created successfuly'}
    