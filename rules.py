class Politics(object):
    _unused_bigrams = ["bk", "fq", "jc", "jt", "mj", "qh", "qx", "vj", "wz", "zh",
                       "bq", "fv", "jd", "jv", "mq", "qj", "qy", "vk", "xb", "zj",
                       "bx", "fx", "jf", "jw", "mx", "qk", "qz", "vm", "xg", "zn",
                       "cb", "fz", "jg", "jx", "mz", "ql", "sx", "vn", "xj", "zq",
                       "cf", "gq", "jh", "jy", "pq", "qm", "sz", "vp", "xk", "zr",
                       "cg", "gv", "jk", "jz", "pv", "qn", "tq", "vq", "xv", "zs",
                       "cj", "gx", "jl", "kq", "px", "qo", "tx", "vt", "xz", "zx",
                       "cp", "hk", "jm", "kv", "qb", "qp", "vb", "vw", "yq", "cv",
                       "hv", "jn", "kx", "qc", "qr", "vc", "vx", "yv", "cw", "hx",
                       "jp", "kz", "qd", "qs", "vd", "vz", "yz", "cx", "hz", "jq",
                       "lq", "qe", "qt", "vf", "wq", "zb", "dx", "iy", "jr", "lx",
                       "qf", "qv", "vg", "wv", "zc", "fk", "jb", "js", "mg", "qg",
                       "qw", "vh", "wx", "zg"]

    @classmethod
    def check_bigrams(cls, sym1, sym2):
        if cls._unused_bigrams.count(sym1 + sym2) == 0:
            return True
        if cls._unused_bigrams.count(sym1 + sym2) == 1:
            return False
