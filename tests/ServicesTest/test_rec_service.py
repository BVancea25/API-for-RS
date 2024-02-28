from src.Services.RecService import get_initial_rec_service
from unittest.mock import patch, MagicMock


def test_get_initial_rec_service():
    mock_request = MagicMock(args={'user_id': 'none'})
    
    with patch('src.Services.RecService.popular_products') as mock_popular_products:
        mock_popular_products.return_value = ['Recommendation 1', 'Recommendation 2', 'Recommendation 3']
        
        result = get_initial_rec_service(mock_request)
        
        assert result == ['Recommendation 1', 'Recommendation 2', 'Recommendation 3']
    

    mock_request = MagicMock(args={'user_id': 2})
    
    with patch('src.Services.RecService.db.cypher_query') as mock_cypher_query:
        # Mocking the results of the database query
        mock_results = MagicMock()
        mock_results.__getitem__.return_value = [
            # Mocking the first result where user hasn't interacted with any products
            [
                {'profile': [1, 2, 2], 'embedding': [0.1, 0.2, 0.3]},
                {'profile': [3, 8, 1], 'favorite_description': [0.4, 0.5, 0.6]}
            ],
            # Mocking the second result with product details
            [
                {'profile': [1, 2, 3], 'embedding': [0.1, 0.2, 0.3]},
                {'profile': [4, 5, 6], 'favorite_description': [0.4, 0.5, 0.6]}
            ],
            # Mocking the third result with product details
            [
                {'profile': [7, 8, 9], 'embedding': [0.7, 0.8, 0.9]},
                {'profile': [10, 11, 12], 'favorite_description': [1.0, 1.1, 1.2]}
            ]
        ]
        mock_cypher_query.return_value = mock_results
        
        # Call the get_initial_rec_service function
        result = get_initial_rec_service(mock_request)
        
        # Assert that the result matches the expected recommendations
        assert result == ['Recommendation 1', 'Recommendation 2', 'Recommendation 3']
    