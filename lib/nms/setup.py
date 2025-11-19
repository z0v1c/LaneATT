from setuptools import setup
from torch.utils.cpp_extension import CUDAExtension, BuildExtension

setup(
    name='nms',
    packages=['nms'],
    package_dir={'': 'src'},
    ext_modules=[
        CUDAExtension(
            'nms.details',
            ['src/nms.cpp', 'src/nms_kernel.cu'],
            extra_compile_args={
                'nvcc': [
                    '-gencode=arch=compute_120,code=sm_120',  # RTX 50 series support
                    '-gencode=arch=compute_90,code=sm_90',
                    '-gencode=arch=compute_86,code=sm_86',  # for extra compatibility
                    '-gencode=arch=compute_80,code=sm_80',
                    '-std=c++17',
                ]
            }
        )
    ],
    cmdclass={'build_ext': BuildExtension}
)
