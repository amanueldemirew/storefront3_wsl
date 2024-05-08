from store.models import Collection
from rest_framework import status
import pytest
from model_bakery import baker

@pytest.fixture
def create_colection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_return_401(self, api_client, create_colection):
        response = create_colection({'title': 'a'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    def test_if_user_is_not_admin_return_403(self,authenticate, api_client, create_colection):
        authenticate()
        response = create_colection({'title': 'a'})
        assert response.status_code == status.HTTP_403_FORBIDDEN
    def test_if_data_is_invalid_returns_400(self,authenticate, api_client, create_colection):
        authenticate(is_staff=True)
        response = create_colection({'title': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
    def test_if_data_is_valid_returns_201(self,authenticate, api_client, create_colection):
        authenticate(is_staff=True)
        response = create_colection({'title': 'a'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_return_200(self, api_client):
        collection = baker.make(Collection)
        response = api_client.get(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0
        }
      