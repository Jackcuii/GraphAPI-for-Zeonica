from zeoapi.zeotensor import *


class nodeOP: #TODO support wrap
    @classmethod
    def PipeG(cls):
        assert 0, "Function not implemented, please check your config."
    @classmethod
    def aPipeG(cls):
        assert 0, "Function not implemented, please check your config."
    @classmethod
    def setWH(cls, src:list, dst:list):
        assert 0, "Function not implemented, please check your config."
    # in PipeG, the item in src should be Dimension, and the item in dst should be ZeoTensor

class OP_addlmm_uwp(nodeOP):
    @classmethod
    def PipeG(cls):
        def anon(src:list, dst:list):
            assert len(src) == 2
            assert len(dst) == 1
            src0, src1 = *src
            dstd = dst[0]
            if not (src0.flow == Flow("EAST") and src0.flow == Flow("SOUTH")):
                return None
            assert type(dstd) == Dimension
            wrap = Dimension([])
            dirc = (src0.dirc[0][0] + src1.dirc[0][1], i)
            dst_ = ZeoTensor(deepcopy(dstd), dirc, wrap, (Flow("SOUTH") if i == 0 else Flow("EAST")))
            return [src0, src1], [dst_]
        for i in [0, 1]:
            yield anon
    @classmethod
    def aPipeG(cls):
        def anon(src: list, dst: list):
            assert len(src) == 2
            assert len(dst) == 1
            src0d, src1d = *src
            src0d = deepcopy(src0d)
            src1d = deepcopy(src1d)
            dst = dst[0]
            assert type(dst) == ZeoTensor
            if not (dst.flow == Flow("EAST") and dst.flow == Flow("SOUTH")):
                return None
            wrap0 = Dimension([])
            wrap1 = Dimension([])
            dirc0 = (dst.dirc[0][0] + x, 0)
            dirc1 = (y + dst.dirc[0][1], 1)
            flow0, flow1 = Flow("EAST"), Flow("SOUTH")
            src0 = ZeoTensor(src0d, dirc0, wrap0, flow0)
            src1 = ZeoTensor(src1d, dirc1, wrap1, flow1)
            return [src0, src1], [dst]
        for x in ["E", "W"]:
            for y in ["N", "S"]:
                yield anon
    @classmethod
    def setWH(cls, src:list, dst:list):  # W,H
        return  src[1].dim[1], src[0].dim[0]

class attachOP(nodeOP):
    @classmethod
    def PipeG(cls):
        def anon(src:list, dst:list):
            assert len(src) == 1
            assert len(dst) == 1
            src = src[0]
            dstd = dst[0]
            assert type(dstd) == Dimension
            flow = Flow(src.flow.dir)
            dirc = deepcopy(src.dirc)
            wrap = Dimension([])
            dst_ = ZeoTensor(dstd, dirc, wrap, flow)
            return [src], [dst_]
        yield anon
    @classmethod
    def aPipeG(cls):
        def anon(src: list, dst: list):
            assert len(src) == 1
            assert len(dst) == 1
            srcd = src[0]
            srcd = deepcopy(srcd)
            dst = dst[0]
            assert type(dst) == ZeoTensor
            flow = Flow(dst.flow.dir)
            dirc = deepcopy(dst.dirc)
            wrap = Dimension([])
            src_ = ZeoTensor(srcd, dirc, wrap, flow)
            return [src_], [dst]
        yield anon
    @classmethod
    def setWH(cls, src:list, dst:list):  # W,H
        a = src[0].dim[src[0].dirc[1]]
        b = 1
        return (b, a) if src[0].flow == Flow("SOUTH") else (a, b)

class OP_addlmm_schdlr(attachOP):
    pass

class OP_relu_uwp(attachOP):
    pass






















