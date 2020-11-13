import modules.tools as Tools

def test_calc_hash():
    assert Tools.calc_hash('111') == 'f6e0a1e2ac41945a9aa7ff8a8aaa0cebc12a3bcc981a929ad5cf810a090e11ae'

def test_get_token():
    assert Tools.check_auth(Tools.get_token('testing')) == True
