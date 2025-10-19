import pytest
from fastapi.testclient import TestClient
from redis import Redis
from main import app
from decouple import config

client = TestClient(app)

@pytest.fixture(scope="function")
def redis_client():
    """Create a real Redis connection for integration tests"""
    redis = Redis(
            host=config("redis_host", cast=str),
            port=config("redis_port", cast=int),
            username=config("redis_username", cast=str, default=None),
            password=config("redis_password", cast=str, default=None),
            decode_responses=True
        )
    
    # Test connection
    try:
        redis.ping()
    except Exception as e:
        pytest.skip(f"Redis server not available: {e}")
    
    yield redis
    
    # Cleanup: Delete all test keys
    test_keys = ["test_*", "integration_*"]
    for pattern in test_keys:
        keys = redis.keys(pattern)
        if keys:
            redis.delete(*keys)
    
    redis.close()

class TestIntegrationPing:
    def test_ping_with_real_redis(self, redis_client):
        print("bggvghhv")
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json()["status"] == "success"

class TestIntegrationStringOperations:    
    def test_create_and_get_string(self, redis_client):
        # Create
        response = client.post("/redis", json={
            "data_type": "STRING",
            "key": "integration_test_string",
            "value": "test_value"
        })
        assert response.status_code == 201
        
        # Get
        response = client.get("/redis/integration_test_string")
        assert response.status_code == 200
        assert response.json()["value"] == "test_value"
        
        # Delete
        response = client.delete("/redis/integration_test_string")
        assert response.status_code == 202

    def test_string_with_expiry(self, redis_client):
        response = client.post("/redis", json={
            "data_type": "STRING",
            "key": "integration_test_expiry",
            "value": "expires_soon",
            "expiryT": 10
        })
        assert response.status_code == 201
        
        # Verify TTL is set
        ttl = redis_client.ttl("integration_test_expiry")
        assert ttl > 0 and ttl <= 10

class TestIntegrationListOperations:
        
    def test_create_and_get_list(self, redis_client):
        test_list = ["item1", "item2", "item3"]
        
        # Create
        response = client.post("/redis", json={
            "data_type": "LIST",
            "key": "integration_test_list",
            "value": test_list
        })
        assert response.status_code == 201
        
        # Get
        response = client.get("/redis/integration_test_list")
        assert response.status_code == 200
        assert response.json()["value"] == test_list
        
        # Delete
        client.delete("/redis/integration_test_list")

class TestIntegrationSetOperations:    
    def test_create_and_get_set(self, redis_client):
        test_set = ["item1", "item2", "item3"]
        
        # Create
        response = client.post("/redis", json={
            "data_type": "SET",
            "key": "integration_test_set",
            "value": test_set
        })
        assert response.status_code == 201
        
        # Get
        response = client.get("/redis/integration_test_set")
        assert response.status_code == 200
        result_set = set(response.json()["value"])
        assert result_set == set(test_set)
        
        # Delete
        client.delete("/redis/integration_test_set")

class TestIntegrationHashOperations:
    def test_create_and_get_hash(self, redis_client):
        test_hash = {"field1": "value1", "field2": "value2"}
        
        # Create
        response = client.post("/redis", json={
            "data_type": "HASH",
            "key": "integration_test_hash",
            "value": test_hash
        })
        assert response.status_code == 201
        
        # Get all fields
        response = client.get("/redis/integration_test_hash")
        assert response.status_code == 200
        assert response.json()["value"] == test_hash
        
        # Get specific field
        response = client.get("/redis/integration_test_hash?path=field1")
        assert response.status_code == 200
        assert response.json()["value"] == "value1"
        
        # Delete
        client.delete("/redis/integration_test_hash")

class TestIntegrationJsonOperations:
    def test_create_and_get_json(self, redis_client):
        test_json = {
            "name": "John Doe",
            "age": 30,
            "address": {
                "city": "New York",
                "country": "USA"
            }
        }
        
        # Create
        response = client.post("/redis", json={
            "data_type": "JSON",
            "key": "integration_test_json",
            "value": test_json
        })
        assert response.status_code == 201
        
        # Get
        response = client.get("/redis/integration_test_json")
        assert response.status_code == 200
        assert response.json()["value"] == test_json
        
        # Delete
        client.delete("/redis/integration_test_json")

class TestIntegrationErrorHandling:
    def test_get_nonexistent_key(self, redis_client):
        response = client.get("/redis/nonexistent_key_12345")
        assert response.status_code == 404

    def test_delete_nonexistent_key(self, redis_client):
        response = client.delete("/redis/nonexistent_key_12345")
        assert response.status_code == 404

    def test_invalid_data_type_validation(self, redis_client):
        response = client.post("/redis", json={
            "data_type": "STRING",
            "key": "test_key",
            "value": ["not_a_string"]
        })
        assert response.status_code == 422

class TestIntegrationUpdateOperations:
    def test_update_existing_key(self, redis_client):
        # Create initial value
        response = client.post("/redis", json={
            "data_type": "STRING",
            "key": "integration_test_update",
            "value": "initial_value"
        })
        assert response.status_code == 201
        
        # Update value
        response = client.post("/redis", json={
            "data_type": "STRING",
            "key": "integration_test_update",
            "value": "updated_value"
        })
        assert response.status_code == 201
        
        # Verify update
        response = client.get("/redis/integration_test_update")
        assert response.status_code == 200
        assert response.json()["value"] == "updated_value"
        
        # Cleanup
        client.delete("/redis/integration_test_update")