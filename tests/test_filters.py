from user_display.filters.regex_filter import RegexFilter
from user_display.filters.composite_filter import CompositeFilter


def test_regex_filter_basic():
    users = [{'id':1,'name':'Alice'},{'id':2,'name':'Bob'}]
    f = RegexFilter('name','Alic')
    res = list(f.filter_many(users))
    assert len(res) == 1 and res[0]['id']==1


def test_composite_filter_and_or():
    u = [{'id':1,'name':'Alice','email':'a@x'}, {'id':2,'name':'Bob','email':'b@x'}]
    fa = RegexFilter('name','Alice')
    fb = RegexFilter('email','b@')
    comb_and = CompositeFilter([fa, fb], op='and')
    assert not list(comb_and.filter_many(u))
    comb_or = CompositeFilter([fa, fb], op='or')
    assert len(list(comb_or.filter_many(u)))==2
