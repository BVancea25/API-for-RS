from src.Services.RecService import get_initial_rec_service
from unittest.mock import patch, MagicMock


def test_get_initial_rec_service():
    mock_request = MagicMock(args={'user_id': 'none'})
    
    with patch('src.Services.RecService.popular_products') as mock_popular_products:
        mock_popular_products.return_value = ['Recommendation 1', 'Recommendation 2', 'Recommendation 3']
        
        result = get_initial_rec_service(mock_request)
        
        assert result == ['Recommendation 1', 'Recommendation 2', 'Recommendation 3']
    

