import clasificadorVIH

def test0():
    text = clasificadorVIH.get_text_from_file('datasets', 0)
    assert clasificadorVIH.detect_sida(text) == False
    
def test1():
    text = clasificadorVIH.get_text_from_file('datasets', 1)
    assert clasificadorVIH.detect_sida(text) == False
        
def test2():
    text = clasificadorVIH.get_text_from_file('datasets', 2)
    assert clasificadorVIH.detect_sida(text) == False
    
    
def test3():
    text = clasificadorVIH.get_text_from_file('datasets', 3)
    assert clasificadorVIH.detect_sida(text) == False
    
    
def test4():
    text = clasificadorVIH.get_text_from_file('datasets', 4)
    assert clasificadorVIH.detect_sida(text) == False
    
def test5():
    text = clasificadorVIH.get_text_from_file('datasets', 5)
    assert clasificadorVIH.detect_sida(text) == True
        
def test6():
    text = clasificadorVIH.get_text_from_file('datasets', 6)
    assert clasificadorVIH.detect_sida(text) == True       

def test7():
    text = clasificadorVIH.get_text_from_file('datasets', 7)
    assert clasificadorVIH.detect_sida(text) == True      

def test8():
    text = clasificadorVIH.get_text_from_file('datasets', 8)
    assert clasificadorVIH.detect_sida(text) == True      

def test9():
    text = clasificadorVIH.get_text_from_file('datasets', 9)
    assert clasificadorVIH.detect_sida(text) == True      