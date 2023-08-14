from ..utils import MultiSet
from .wl2base import WL2Base

class WL2(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.color,
            self.global_u(),
            self.global_v(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_all(coloring)

class FWL2(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.color,
            self.global_fwl2(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_all(coloring)
    
class LFWL(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.color,
            self.local_u_fwl2(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_all(coloring)
    
class SLFWL(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.color,
            self.local_uv_fwl2(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_all(coloring)
    
class SWL_SV(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.pointwise_uv(),
            self.local_u(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_sv(coloring)
    
class SWL_VS(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.pointwise_uv(),
            self.local_u(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_vs(coloring)
    
class SWL_SV_P(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.pointwise_uv(),
            self.local_u(),
            self.pointwise_uu(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_sv(coloring)
    
class SWL_VS_P(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.pointwise_uv(),
            self.local_u(),
            self.pointwise_uu(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_vs(coloring)

class SWL_SV_G(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.pointwise_uv(),
            self.local_u(),
            self.pointwise_uu(),
            self.global_u(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_sv(coloring)
    
class SWL_VS_G(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.pointwise_uv(),
            self.local_u(),
            self.pointwise_uu(),
            self.global_u(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_vs(coloring)
    
class PSWL_SV(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.pointwise_uv(),
            self.local_u(),
            self.pointwise_vv(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_sv(coloring)
    
class PSWL_VS(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.pointwise_uv(),
            self.local_u(),
            self.pointwise_vv(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_vs(coloring)
    
class GSWL_SV(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.pointwise_uv(),
            self.local_u(),
            self.global_v(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_sv(coloring)
    
class GSWL_VS(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.pointwise_uv(),
            self.local_u(),
            self.global_v(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_vs(coloring)
    
class GSWL_SV_P(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.pointwise_uv(),
            self.local_u(),
            self.global_v(),
            self.pointwise_vv(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_sv(coloring)
    
class GSWL_VS_P(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.pointwise_uv(),
            self.local_u(),
            self.global_v(),
            self.pointwise_vv(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_vs(coloring)
    
class GSWL_SV(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.pointwise_uv(),
            self.local_u(),
            self.global_v(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_sv(coloring)
    
class SSWL_VS(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.pointwise_uv(),
            self.local_u(),
            self.local_v(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_vs(coloring)
    
class SSWL_SV(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.pointwise_uv(),
            self.local_u(),
            self.local_v(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_sv(coloring)

class FullSWL_VS(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.pointwise_uv(),
            self.pointwise_vu(),
            self.pointwise_uu(),
            self.pointwise_vv(),
            self.global_u(),
            self.global_v(),
            self.local_u(),
            self.local_v(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_vs(coloring)
    
class FullSWL_SV(WL2Base):
    def aggregate_colors(self):
        return self.color_concat(
            self.pointwise_uv(),
            self.pointwise_vu(),
            self.pointwise_uu(),
            self.pointwise_vv(),
            self.global_u(),
            self.global_v(),
            self.local_u(),
            self.local_v(),
        )
    def pool_colors(self, coloring) -> MultiSet:
        return self.pool_sv(coloring)