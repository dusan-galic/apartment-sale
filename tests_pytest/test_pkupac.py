import pytest


def test_get_pkupac_for_given_id(client, user_session_admin):
    r = client.get(
        "/pkupac/4",
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200


def test_add_pkupac(client, add_pkupac_data, user_session_admin):
    r = client.post(
        "/pkupac",
        json=add_pkupac_data,
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200


def test_update_existing_pkupac(client, user_session_admin):
    edit_obj = {
        "broj_ugovora": "sdgsdgsd"
    }
    r = client.patch(
        "/pkupac/21",
        json=edit_obj,
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200


def test_delete_pkupac(client, user_session_admin):
    r = client.delete(
        "/pkupac/21",
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200


def test_update_validate_pkupac_false(client, user_session_admin):
    edit_obj = {
        "is_validated": True
    }
    r = client.patch(
        "/pkupac/validation/21",
        json=edit_obj,
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 403


def test_update_validate_pkupac_access(client, user_session_finansije):
    edit_obj = {
        "is_validated": True
    }
    r = client.patch(
        "/pkupac/validation/21",
        json=edit_obj,
        headers={
            'session_id': user_session_finansije
        }
    )

    assert r.status_code == 200


def test_get_pkupac_for_given_stan_id(client, user_session_admin):
    r = client.get(
        "/pkupac/stan/6",
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200
