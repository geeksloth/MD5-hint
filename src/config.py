conf_multiprocessing = True #recommend for multi-core processor
conf_letterCasePerm = True  #recommend
conf_replaceSpecial = True  #recommend
conf_permutation = False #shuffle all possible positions, suitable for numeric, also work with alphabet but might takes too long time.
conf_bruteforce_number = False
conf_add_prefix = 0
conf_add_suffix = 0
find_x = ["a", "A", "s", "S", "o", "O", "1", "l"]
replace_x = ["@", "@", "$", "$", "0", "0", "!", "1"]
specialChars = "!@#$%^&*!@#$%^&*"
from multiprocessing import cpu_count
totalWorkers = cpu_count() - 3