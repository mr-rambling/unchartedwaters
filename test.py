from goods import *

test_dict = {'1': magical_tome, '2': enchanted_artifacts}

print(test_dict.values())

for item in test_dict.values():
    print(item.name)