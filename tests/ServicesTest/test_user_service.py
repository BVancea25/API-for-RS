from src.Services.UserService import add_user_service,delete_user_service
from unittest.mock import patch
from src.Services.UserService import User


def test_add_user_service():
    mock_req={"id":1,"name":"Bogdan"}
    
    with patch('src.Services.UserService.User') as mock_user:
        result=add_user_service(mock_req)
        
        mock_user.assert_called_once_with(name=mock_req['name'],client_id=mock_req['id'],favorite_description=[],profile=[])
    
    assert result=="Save successful"
    
def test_delete_user_service():
    mock_req={"id":1}

    with patch('src.Services.UserService.User') as mock_user:
        mock_user_instance=User(name='Test',client_id=mock_req['id'],favorite_description=[],profile=[],element_id_property=mock_req['id'])
        
        mock_user.nodes.get.return_value=mock_user_instance
        
        result=delete_user_service(mock_req)
        
       
    assert result=="Successful deletion!"
