from ccomplex.cli import main

def test_main():
    assert main([]) == 0




from ccomplex import ccomplex

def test():
    assert str(ccomplex(0.0 + 0j))   == '0'
    assert str(ccomplex(0))          == '0'
    assert str(ccomplex(12))         == '12'
    assert str(ccomplex(-32+54j))    == '-32+j54'
    assert str(ccomplex(0+4.0j))     == 'j4'
    assert str(ccomplex(-2.0+0.13j)) == '-2+j0.13'
    assert str(ccomplex(-2+32.0j))   == '-2+j32'
    assert str(ccomplex(12-23.43j))  == '12-j23.43'
    assert str(ccomplex(2.0-4.1j))   == '2-j4.1'
    assert str(ccomplex(3e-6+0j))    == '3e-06'

def test_approx():
    assert str(ccomplex(4/5))           == '0.8'
    assert str(ccomplex(1e-12+32.2j))   == 'j32.2'
    assert str(ccomplex(1e14+.22j))     == '100000000000000'
    assert str(ccomplex(.32+1e-22j))     == '0.32'
    

    
