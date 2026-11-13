# The page's functions: the longest prefix match by a scan, a binary trie, a multibit trie and the pipeline
from solution import *  # noqa: F401,F403

table = [route("10.0.0.0/8", "A"), route("10.1.0.0/16", "B"), route("10.1.2.0/24", "C"),
         route("172.16.0.0/12", "E"), route("0.0.0.0/0", "D")]
print(ip("10.1.2.3"))                                    # 167838211
print(route("10.1.2.3/16", "B") == route("10.1.0.0/16", "B"))   # True
print(mask(0), hex(mask(8)), hex(mask(32)))              # 0 0xff000000 0xffffffff
print([lpm_naive(table, ip(a)) for a in ["10.1.2.3", "10.1.3.4", "10.200.0.1", "172.20.1.1", "8.8.8.8"]])   # ['C', 'B', 'A', 'E', 'D']

t = Trie()
for v, k, hop in table:
    t.insert(v, k, hop)
print(t.nodes, t.lookup(ip("10.1.2.3")))                 # 37 C
print(t.delete(ip("10.0.0.0"), 8), t.nodes, t.lookup(ip("10.200.0.1")))   # True 37 D

strides = []
for s in (1, 2, 4, 8):
    m = MultiTrie(32, s)
    for v, k, hop in table:
        m.insert(v, k, hop)
    strides.append((s, m.entries(), m.lookup(ip("10.1.3.4"))))
print(strides)                  # [(1, 70, 'B'), (2, 68, 'B'), (4, 128, 'B'), (8, 1024, 'B')]

small = MultiTrie(8, 2)
for v, k, hop in [(0, 0, "D"), (128, 1, "A"), (160, 3, "B"), (176, 5, "C"), (64, 2, "E")]:
    small.insert(v, k, hop)
out = pipeline(small, [185, 182, None, 64, 3])
print([st[-1] for st in out][3:])                        # [(185, 'B', False), (182, 'C', False), None, (64, 'E', False), (3, 'D', False)]
