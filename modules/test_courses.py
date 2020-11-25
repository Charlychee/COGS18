from modules import courses

def test_remove_star():
    test_string1 = 'no_star'
    test_string2 = 'with_star*'

    assert courses.remove_star(test_string1) == 'no_star'
    assert courses.remove_star(test_string2) == 'with_star'

