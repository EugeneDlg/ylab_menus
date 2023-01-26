from fastapi import status

### get list dishes, must be empty here, ALL LIST OF ALL

def test_get_menu_404_0(client, test_db):
    response = client.get('/api/v1/menus/1')
    assert response.json() == {'detail': 'menu not found'}
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_menu_0(client, test_db):
    response = client.post('/api/v1/menus', json={'title': 'My menu 1', 'description': 'My menu description 1'})
    assert response.json() == {
        "id": "1",
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0,
        "dishes_count": 0
    }
    assert response.status_code == status.HTTP_201_CREATED


def test_get_menu_0(client, test_db):
    response = client.get('/api/v1/menus/1')
    assert response.json() == {
        "id": "1",
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0,
        "dishes_count": 0
    }
    assert response.status_code == status.HTTP_200_OK


# def test_get_menu_list_0(client, test_db):
#     response = client.get('/api/v1/menus')
#     assert response.json() == [{
#         "id": "1",
#         "title": "My menu 1",
#         "description": "My menu description 1",
#         "submenus_count": 0,
#         "dishes_count": 0
#     }]
#
#
# def test_update_menu_0(client, test_db):
#     response = client.patch(
#         '/api/v1/menus/1', json={'title': 'My new menu 1',
#                                  'description': 'My new menu description 1'}
#     )
#     assert response.json() == {
#         "id": "1",
#         "title": "My new menu 1",
#         "description": "My new menu description 1",
#         "submenus_count": 0,
#         "dishes_count": 0
#     }
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_get_menu_after_update_0(client, test_db):
#     response = client.get('/api/v1/menus/1')
#     assert response.json() == {
#         "id": "1",
#         "title": "My new menu 1",
#         "description": "My new menu description 1",
#         "submenus_count": 0,
#         "dishes_count": 0
#     }
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_delete_menu_0(client, test_db):
#     response = client.delete('/api/v1/menus/1')
#     assert response.json() == {
#         "status": True,
#         "message": "The menu has been deleted"
#     }
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_get_menu_after_deletion_0(client, test_db):
#     response = client.get('/api/v1/menus/1')
#     assert response.json() == {'detail': 'menu not found'}
#     assert response.status_code == status.HTTP_404_NOT_FOUND
#
#
# def test_update_menu_after_deletion_0(client, test_db):
#     response = client.patch('/api/v1/menus/1',
#                             json={'title': 'My updated menu 1',
#                                   'description': 'My updated menu description 1'})
#     assert response.json() == {'detail': 'menu not found'}
#     assert response.status_code == status.HTTP_404_NOT_FOUND
#
#
# def test_delete_menu_after_deletion_0(client, test_db):
#     response = client.delete('/api/v1/menus/1')
#     assert response.json() == {"detail": "menu not found"}
#     assert response.status_code == status.HTTP_404_NOT_FOUND
#
#
# def test_create_menu_1(client, test_db):
#     response = client.post('/api/v1/menus',
#                            json={'title': 'My menu 2',
#                                  'description': 'My menu description 2'})
#     assert response.json() == {
#         "id": "2",
#         "title": "My menu 2",
#         "description": "My menu description 2",
#         "submenus_count": 0,
#         "dishes_count": 0
#     }
#     assert response.status_code == status.HTTP_201_CREATED
#
#
# def test_get_submenu_404_1(client, test_db):
#     response = client.get('/api/v1/menus/2/submenus/1')
#     assert response.json() == {'detail': 'submenu not found'}
#     assert response.status_code == status.HTTP_404_NOT_FOUND
#
#
# def test_create_submenu_1(client, test_db):
#     response = client.post('/api/v1/menus/2/submenus',
#                            json={'title': 'My submenu 1',
#                                  'description': 'My submenu description 1'})
#     assert response.json() == {
#         "id": "1",
#         "title": "My submenu 1",
#         "description": "My submenu description 1",
#         "dishes_count": 0
#     }
#     assert response.status_code == status.HTTP_201_CREATED
#
#
# def test_get_submenu_1(client, test_db):
#     response = client.get('/api/v1/menus/2/submenus/1')
#     assert response.json() == {
#         "id": "1",
#         "title": "My submenu 1",
#         "description": "My submenu description 1",
#         "dishes_count": 0
#     }
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_get_submenu_list_1(client, test_db):
#     response = client.get('/api/v1/menus/2/submenus')
#     assert response.json() == [{
#         "id": "1",
#         "title": "My submenu 1",
#         "description": "My submenu description 1",
#         "dishes_count": 0
#     }]
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_get_menu_1(client, test_db):
#     response = client.get('/api/v1/menus/2')
#     assert response.json() == {
#         "id": "2",
#         "title": "My menu 2",
#         "description": "My menu description 2",
#         "submenus_count": 1,
#         "dishes_count": 0
#     }
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_update_submenu_1(client, test_db):
#     response = client.patch('/api/v1/menus/2/submenus/1',
#                             json={'title': 'My new submenu 1',
#                                   'description': 'My new submenu description 1'})
#     assert response.json() == {
#         "id": "1",
#         "title": "My new submenu 1",
#         "description": "My new submenu description 1",
#         "dishes_count": 0
#     }
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_get_submenu_after_update_1(client, test_db):
#     response = client.get('/api/v1/menus/2/submenus/1')
#     assert response.json() == {
#         "id": "1",
#         "title": "My new submenu 1",
#         "description": "My new submenu description 1",
#         "dishes_count": 0
#     }
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_delete_submenu_1(client, test_db):
#     response = client.delete('/api/v1/menus/2/submenus/1')
#     assert response.json() == {
#         "status": True,
#         "message": "The submenu has been deleted"
#     }
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_get_submenu_after_deletion_1(client, test_db):
#     response = client.get('/api/v1/menus/2/submenus/1')
#     assert response.json() == {'detail': 'submenu not found'}
#     assert response.status_code == status.HTTP_404_NOT_FOUND
#
#
# def test_update_submenu_after_deletion_1(client, test_db):
#     response = client.patch('/api/v1/menus/2/submenus/1',
#                             json={'title': 'My updated menu 1',
#                                   'description': 'My updated menu description 1'})
#     assert response.json() == {'detail': 'submenu not found'}
#     assert response.status_code == status.HTTP_404_NOT_FOUND
#
#
# def test_create_submenu_2(client, test_db):
#     response = client.post('/api/v1/menus/2/submenus',
#                            json={'title': 'My submenu 2',
#                                  'description': 'My submenu description 2'})
#     assert response.json() == {
#         "id": "2",
#         "title": "My submenu 2",
#         "description": "My submenu description 2",
#         "dishes_count": 0
#     }
#     assert response.status_code == status.HTTP_201_CREATED
#
#
# def test_get_dishes_list_2(client, test_db):
#     response = client.get('/api/v1/menus/2/submenus/2/dishes')
#     assert response.json() == []
#
#
# def test_create_dish_2(client, test_db):
#     response = client.post('/api/v1/menus/2/submenus/2/dishes',
#                            json={"title": "My dish 1",
#                                  "description": "My dish description 1",
#                                  "price": "33.7"})
#     assert response.json() == {
#         "id": "1",
#         "title": "My dish 1",
#         "description": "My dish description 1",
#         "price": "33.70"
#     }
#     assert response.status_code == status.HTTP_201_CREATED
#
#
# def test_get_dish_2(client, test_db):
#     response = client.get('/api/v1/menus/2/submenus/2/dishes/1')
#     assert response.json() == {
#         "id": "1",
#         "title": "My dish 1",
#         "description": "My dish description 1",
#         "price": "33.70"
#     }
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_get_menu_2(client, test_db):
#     response = client.get('/api/v1/menus/2')
#     assert response.json() == {
#         "id": "2",
#         "title": "My menu 2",
#         "description": "My menu description 2",
#         "submenus_count": 1,
#         "dishes_count": 1
#     }
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_get_submenu_2(client, test_db):
#     response = client.get('/api/v1/menus/2/submenus/2')
#     assert response.json() == {
#         "id": "2",
#         "title": "My submenu 2",
#         "description": "My submenu description 2",
#         "dishes_count": 1
#     }
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_update_dish_2(client, test_db):
#     response = client.patch('/api/v1/menus/2/submenus/2/dishes/1',
#                             json={"title": "My new dish 1",
#                                   "description": "My new dish description 1",
#                                   "price": "101.99"})
#     assert response.json() == {
#         "id": "1",
#         "title": "My new dish 1",
#         "description": "My new dish description 1",
#         "price": "101.99"
#     }
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_get_dish_after_update_2(client, test_db):
#     response = client.get('/api/v1/menus/2/submenus/2/dishes/1')
#     assert response.json() == {
#         "id": "1",
#         "title": "My new dish 1",
#         "description": "My new dish description 1",
#         "price": "101.99"
#     }
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_delete_dish_2(client, test_db):
#     response = client.delete('/api/v1/menus/2/submenus/2/dishes/1')
#     assert response.json() == {
#         "status": True,
#         "message": "The dish has been deleted"
#     }
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_get_dish_after_deletion_2(client, test_db):
#     response = client.get('/api/v1/menus/2/submenus/2/dishes/1')
#     assert response.json() == {'detail': 'dish not found'}
#     assert response.status_code == status.HTTP_404_NOT_FOUND
#
#
# def test_get_menu_3(client, test_db):
#     response = client.get('/api/v1/menus/2')
#     assert response.json() == {
#         "id": "2",
#         "title": "My menu 2",
#         "description": "My menu description 2",
#         "submenus_count": 1,
#         "dishes_count": 0
#     }
#     assert response.status_code == status.HTTP_200_OK
#
#
# def test_get_submenu_3(client, test_db):
#     response = client.get('/api/v1/menus/2/submenus/2')
#     assert response.json() == {
#         "id": "2",
#         "title": "My submenu 2",
#         "description": "My submenu description 2",
#         "dishes_count": 0
#     }
#     assert response.status_code == status.HTTP_200_OK

