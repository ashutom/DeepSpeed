"""
Copyright 2020 The Microsoft DeepSpeed Team
"""
import torch
from .builder import CUDAOpBuilder, is_rocm_pytorch


class FusedAdamBuilder(CUDAOpBuilder):
    BUILD_VAR = "DS_BUILD_FUSED_ADAM"
    NAME = "fused_adam"

    def __init__(self):
        super().__init__(name=self.NAME)

    def absolute_name(self):
        return f'deepspeed.ops.adam.{self.NAME}_op'

    def sources(self):
        return ['csrc/adam/fused_adam_frontend.cpp', 'csrc/adam/multi_tensor_adam.cu']

    def include_paths(self):
        return ['csrc/includes', 'csrc/adam']

    def cxx_args(self):
        args = super().cxx_args()
        return args + self.version_dependent_macros()

    def nvcc_args(self):
        nvcc_flags=['-O3'] + self.version_dependent_macros()
        if not is_rocm_pytorch:
            nvcc_flags.extend(['-lineinfo', '--use_fast_math'] + self.compute_capability_args())
        return nvcc_flags
