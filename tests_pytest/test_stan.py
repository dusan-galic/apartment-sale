import pytest


def test_get_stan_for_given_id(client, user_session_admin):
    r = client.get(
        "/stan/4",
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200


def test_add_stan(client, add_stan_data, user_session_admin):
    r = client.post(
        "/stan",
        json=add_stan_data,
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200


def test_update_existing_stan(client, user_session_admin):
    edit_obj = {
        "kvadratura": "100"
    }
    r = client.patch(
        "/stan/4",
        json=edit_obj,
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200


def test_delete_stan(client, user_session_admin):
    r = client.delete(
        "/stan/9",
        headers={
            'session_id': user_session_admin
        }
    )

    assert r.status_code == 200


def test_filter_and_sort_stan(client, user_session_prodavac):
    r = client.get(
        "/stanovi?page=1&per_page=10&sort_by=id&sort_desc=false&kvadratura=100",
        headers={
            'session_id': user_session_prodavac
        }
    )

    assert r.status_code == 200
    assert len(r.json) > 0
