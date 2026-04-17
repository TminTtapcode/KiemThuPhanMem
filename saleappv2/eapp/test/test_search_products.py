from eapp.dao import load_products
from eapp.test.test_base import test_app,test_session, sample_products


def test_all(sample_products):
    actual_products = load_products()

    assert len(actual_products) == len(sample_products)

def test_cate(sample_products):
    actual_products= load_products(cate_id=2)
    assert len(actual_products)==3;

    assert all( p.category_id==2 for p in actual_products)

def test_kw_cate( sample_products):
    actual_products= load_products(kw='iPhone',cate_id=1)
    assert len(actual_products)==1
    assert ("iPhone" in p.name and p.category_id ==1 for p in actual_products)


def test_kw(sample_products):
    actual_product=load_products(kw ='iPhone')

    assert len(actual_product) == 3
    assert all('iPhone' in p.name for p in actual_product)
def test_paging(sample_products):
    actual_products = load_products(page=1)
    assert len(actual_products) == 2
    actual_products = load_products(page=3)
    assert len(actual_products) == 1

def test_kw_paging(sample_products):
    actual_product = load_products(kw = 'Galaxy',page=1)
    assert len(actual_product) ==1
    assert all('Galaxy' in p.name for p in actual_product)

    actual_product = load_products(kw='Galaxy', page=2)
    assert len(actual_product) == 0
    assert all('Galaxy' in p.name for p in actual_product)



