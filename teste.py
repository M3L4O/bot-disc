nums = [1, 2, 3, 4, 5, 6 ,7]

num = list(filter(lambda num: num == 10, nums))

if num:
    print(list(num))
else:
    print(list(num), ':)')