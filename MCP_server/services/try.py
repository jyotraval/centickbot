from heapq import heappush as hpush, heappop as hpop
from typing import List
class Solution:
    def maximumScore(self, nums: List[int], s: str) -> int:
        one_pos = []
        n = len(nums)
        for i in range(n):
            if s[i] == '1':
                one_pos.append(i)
        if not one_pos:
            return 0
        res =0
        lastpicked = -1
        heaps = [] # max heap [(-nums[i],i)...]
        for oneidx in one_pos:
            for i in range(lastpicked+1,oneidx+1):
                hpush(heaps, (-nums[i], i))
            while heaps and heaps[0][1]<= lastpicked:
                hpop(heaps)
            if heaps and heaps[0][1]<=one_pos:
                val , idx = hpop(heaps)
                res+= -val
                lastpicked = idx
            else:
                res+= nums[oneidx]
                lastpicked = oneidx
        return res
