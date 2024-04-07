arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
mse = 0
msf = 0
for i in range(len(arr)):
    mse += arr[i]
    mse = max(mse, arr[i])
    msf = max(msf, mse)