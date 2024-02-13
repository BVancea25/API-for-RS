from unittest.mock import patch,Mock,MagicMock
from src.Services.DataService import calculate_product_profiles_service,calculate_user_profile_pipeline
from src.Services.DataService import Product
from flask import Request

def test_product_profiles_service():
    
    mock_data=[
        {"id":1,"color":"red","name":"NikeV5","type":"boots","brand":"addidas"},
        {"id":2,"color":"blue","name":"NikeV4","type":"sneakers","brand":"puma"},
        {"id":3,"color":"green","name":"NikeV6","type":"flip flops","brand":"nike"}
        ]
     
    with patch('src.Services.DataService.Product') as mocked_product:
        ids=[1,2,3]
        index=0
        product_instances=[
            Product(name=mock_data[0]['name'],embedding=[],profile=[],color=mock_data[0]['color'],type=mock_data[0]['type'],brand=mock_data[0]['brand'],client_id=mock_data[0]['id']),
            Product(name=mock_data[1]['name'],embedding=[],profile=[],color=mock_data[1]['color'],type=mock_data[1]['type'],brand=mock_data[1]['brand'],client_id=mock_data[1]['id']),
            Product(name=mock_data[2]['name'],embedding=[],profile=[],color=mock_data[2]['color'],type=mock_data[2]['type'],brand=mock_data[2]['brand'],client_id=mock_data[2]['id'])               
                           ]
        
        mocked_product.nodes.order_by('client_id').all.return_value=product_instances
        
        for id in ids:
            mocked_product.nodes.get(client_id=id).return_value=product_instances[index]
            index+=1
        
        result = calculate_product_profiles_service()
        
        
        
        print(result)
        # Assert the result
        assert result == "Profiles calculated!"
        
        mocked_product.nodes.order_by.return_value.all.assert_called_once()

def test_user_profile_pipeline():
    request=Request({
        'QUERY_STRING': 'user_id=2',
        'REQUEST_METHOD': 'GET'
    })
    
    
   
        
    result=calculate_user_profile_pipeline(request)
    
    print(result)
    assert result=="Calculation of user profile successful"
    
    
    
    
        
       
        
            
        
        