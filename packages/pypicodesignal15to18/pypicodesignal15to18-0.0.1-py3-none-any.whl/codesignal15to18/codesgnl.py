# 15
def addBorder(picture):
    r =['*'*(len(picture[0])+2)]
    for i in picture:
        r.append('*' + i + '*')
    r.append(r[0])
    return r
#16
def areSimilar(A, B):
    r = []
    for i in range(len(A)):
        if A[i] != B[i]:
            r.append([A[i], B[i]])
    if len(r) == 0 or len(r) == 2 and r[0] == r[1][::-1]:
        return True
    return False
#17
def arrayChange(inputArray):
    total_count = 0

    diff_list = [x-y for x,y in zip(inputArray[1:], inputArray[:-1])]
    prev_move = 0
    curr_move = 0

    for val in diff_list:
        curr_move = max(0, prev_move - (val - 1))
        total_count = total_count + curr_move
        prev_move = curr_move

    return total_count
#18
def palindromeRearranging(inputString):
    odds=0
    myset=set(inputString)
    for i in myset:
        n=inputString.count(i)
        if n%2!=0:
            odds+=1
    return odds<=1