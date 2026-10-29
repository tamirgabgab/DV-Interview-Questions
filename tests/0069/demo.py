# Overtakes in a stream of responses: how many overtook each request, how many it
# overtook, the total, and the live report as the responses arrive
from solution import *  # noqa: F401,F403

done = [5, 2, 6, 1]
print("passed:", passed(done))  # [2, 1, 1, 0]
print("by merge sort:", passed_merge(done))  # [2, 1, 1, 0]
print("overtook:", overtook(done))  # [0, 1, 0, 3]
print("inversions:", inversions(done))  # 4
print("disorder:", round(disorder(done), 3))  # 0.667
print("arrival order:", arrival_order(done))  # [3, 1, 0, 2]
print("live:", live_overtakes(arrival_order(done), 4))  # [0, 1, 2, 1]
print("ties:", passed([4, 4, 4]), overtook([4, 4, 4]))  # [0, 0, 0] [0, 0, 0]
