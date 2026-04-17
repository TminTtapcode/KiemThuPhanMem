from eapp.test.test_base import test_app,test_client


def test_add_to_cart(test_client):
    test_client.post('/api/carts' , json={
        'id':1,
        'name': 'iPhone',
        'price':50
    })
    res = test_client.post('/api/carts',json={
        'id':1,
        'name': 'iPhone',
        'price':50
    })
    data = res.get_json()

    assert data['total_quantity'] == 2
    assert data['total_amount'] == 100

def test_add_cart_increase(test_client):
    test_client.post('/api/carts', json={
        'id': 1,
        'name': 'iPhone',
        'price': 50
    })
    test_client.post('/api/carts', json={
        'id': 1,
        'name': 'iPhone',
        'price': 50
    })
    res =test_client.post('/api/carts', json={
        'id': 2,
        'name': 'Galaxy',
        'price': 100
    })
    data = res.get_json()

    assert data['total_quantity'] == 3
    assert data['total_amount'] == 200

    with test_client.session_transaction()as sess:
        assert 'cart' in sess
        assert len(sess['cart'])==2
        assert sess['cart']['1']['quantity']== 2
        assert sess['cart']['2']['quantity']== 1

def test_existing_item(test_client):
    with test_client.session_transaction() as sess:
        sess['cart']= {
            '1': {
                'id': 1,
                'name': 'iPhone',
                'price': 125,
                'quantity':2
            }
        }
    res = test_client.post('/api/carts',json = {
        'id': 1,
        'name': 'Galaxy',
        'price': 100
    })

    data = res.get_json()
    assert  data['total_quantity']==3

    with test_client.session_transaction() as sess:
        assert sess['cart']['1']['quantity']== 3

def test_update_cart(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            '1': {
                'id': 1,
                'name': 'iPhone',
                'price': 125,
                'quantity': 2
            }
        }
    res = test_client.put('/api/carts/1' , json = {
        'quantity' : 10,
    })
    data = res.get_json()

    assert data['total_quantity']== 10
    assert data['total_amount'] == 1250

    with test_client.session_transaction() as sess:
        assert len(sess['cart'])==1

def test_delete_cart(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            '1': {
                'id': 1,
                'name': 'iPhone',
                'price': 125,
                'quantity': 1
            },
            '2': {
                'id': 2,
                'name': 'iPhone',
                'price': 120,
                'quantity': 1
            },

        }

    res = test_client.delete('/api/carts/1')
    data = res.get_json()

    assert data['total_quantity'] == 1
    assert data['total_amount'] == 120
    with test_client.session_transaction() as sess:
        assert '1' not in sess['cart']