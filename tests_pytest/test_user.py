import pytest


def test_get_user_for_given_id(client, user_session_admin):
    r = client.get(
        "/user/1",
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200


def test_add_user(client, add_user_data, user_session_admin):
    r = client.post(
        "/user/register",
        json=add_user_data,
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200


def test_get_users(client, user_session_admin):
    """Start with a blank database."""
    r = client.get(
        "/users?page=1&per_page=10&sort_by=id&sort_desc=false",
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200


def test_update_existing_user(client, user_session_admin):
    edit_obj = {
        "first_name": "tesssssss"
    }
    r = client.patch(
        "/user/1",
        json=edit_obj,
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200


def test_delete_user(client, user_session_admin):
    r = client.delete(
        "/user/9",
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200


def test_get_bad_users(client, user_session_prodavac):
    """Start with a blank database."""
    r = client.get(
        "/users?page=1&per_page=10&sort_by=id&sort_desc=false",
        headers={
            'session_id': user_session_prodavac
        }
    )

    assert r.status_code == 403
    assert len(r.json) > 0


def test_filter_and_sort_user(client, user_session_admin):
    r = client.get(
        "/users?page=1&per_page=10&sort_by=id&sort_desc=false&first_name=test",
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200
    assert len(r.json) > 0


def test_search_data(client, user_session_admin):
    r = client.get(
        "/users?page=1&per_page=10&sort_by=id&sort_desc=false&search_string=tes",
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200
    assert len(r.json) > 0
