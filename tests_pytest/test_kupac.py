import pytest


def test_get_kupac_for_given_id(client, user_session_admin):
    r = client.get(
        "/kupac/1",
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200


def test_add_kupac(client, add_kupac_data, user_session_admin):
    r = client.post(
        "/kupac",
        json=add_kupac_data,
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200


def test_update_existing_kupac(client, user_session_admin):
    edit_obj = {
        "first_name": "tesssssss"
    }
    r = client.patch(
        "/kupac/1",
        json=edit_obj,
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200


def test_delete_user(client, user_session_admin):
    r = client.delete(
        "/kupac/10",
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200


def test_filter_and_sort_kupac(client, user_session_admin):
    r = client.get(
        "/kupci?page=1&per_page=10&sort_by=id&sort_desc=false&first_name=test1",
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200
    assert len(r.json) > 0


def test_search_data(client, user_session_admin):
    r = client.get(
        "/kupci?page=1&per_page=10&sort_by=id&sort_desc=false&search_string=tes",
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200
    assert len(r.json) > 0
