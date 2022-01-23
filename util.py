
import math
def isPerfectSquare(n):
    """
    :type n: int
    :rtype: bool
    """
    if n < 0:
        return False
    if n == 0 or n == 1:
        return True
    i = 1
    while i * i < n:
        i += 1
    return i * i == n

def calculateDimensions(imageSize, imageCount):
    if isPerfectSquare(imageCount):
        return (int(imageSize[0] * imageCount/2), int(imageSize[1] * imageCount/2))
    else:
        return (int(imageSize[0] * math.sqrt(imageCount)), int(imageSize[1] * math.sqrt(imageCount)))