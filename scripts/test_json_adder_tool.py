import json_adder_tool

def test_reset_json():
    # Wipe file
    with open('../UCSD_courses.json', 'w') as f:
        f.write('')
    with open('../UCSD_courses.json', 'r') as f:
        after = f.readlines()
        assert len(after) == 0

    # Reset file
    json_adder_tool.reset_json()
    with open('../UCSD_courses.json', 'r') as f:
        after = f.readlines()
        assert len(after) > 0
