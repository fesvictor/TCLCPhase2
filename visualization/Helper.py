"""
arr : np.array

returns an array of 5 values --> 5 weeks
"""
def summarize_values_to_week(arr):
    if len(arr) <= 31: 
        return [arr[0:7].sum(), arr[7:14].sum(), arr[14:21].sum(), arr[21:28].sum(), arr[28:31].sum()]
    else:
        ret_arr = []
        counter = 0
        while counter * 7 < len(arr):
            ret_arr += [arr[counter * 7 : (counter + 1) * 7].sum()]
            counter +=1
        return ret_arr
    