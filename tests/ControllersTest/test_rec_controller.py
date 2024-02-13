from src.Controllers.recController import get_initial_rec,get_rec
from unittest.mock import patch
from src.index import app
import json
from unittest.mock import patch


def test_get_initial_rec():
    mock_products=[
        {"id":1,"color":"red","name":"NikeV5","type":"boots"},
        {"id":2,"color":"blue","name":"NikeV4","type":"sneakers"},
        {"id":3,"color":"green","name":"NikeV6","type":"flip flops"}
    ]
    
    with patch('src.Controllers.recController.get_initial_rec_service') as mocked_rec_service:
        mocked_rec_service.return_value=mock_products
        
        with app.test_request_context():
            response = get_initial_rec()
            response_data,status_code=response
    print(response_data)
    print(status_code)
    print("Was add_product_service called?", mocked_rec_service.called)
    
    assert status_code==200
    assert response_data == mock_products

def test_get_rec():
    mock_products=[
        {"id":1,"color":"red","name":"NikeV5","type":"boots"},
        {"id":2,"color":"blue","name":"NikeV4","type":"sneakers"},
        {"id":3,"color":"green","name":"NikeV6","type":"flip flops"}
    ]
    
    add_rel_service_response="Relationship created !"
    
    with patch('src.Controllers.recController.get_rec_service') as mocked_rec_service:
        with patch('src.Controllers.recController.add_relation_service') as mocked_rel_service:
            mocked_rel_service.return_value=add_rel_service_response
            mocked_rec_service.return_value=mock_products
            
            with app.test_request_context():
                response = get_rec()
                response_data,status_code=response
        print(response_data)
        print(status_code)
        print("Was add_product_service called?", mocked_rec_service.called)
        
    assert status_code==200
    assert response_data == mock_products
    