def rotate_right(nums, k):
    n = len(nums)
    k = k % n
    count=0
    
    while count<k: 
        last = nums[-1]  # store last element
        
        # shift elements to right by 1
        for i in range(n-1, 0, -1):
            nums[i] = nums[i-1]
        
        nums[0] = last  # place last at front
        count=count+1

    return nums

print(rotate_right([1, 2, 3, 4, 5], 2))
