# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import platform

import setuptools
from torch.utils import cpp_extension

extra_compile_args = []
extra_link_args = []

# This is a problem of macOS: https://github.com/pytorch/pytorch/issues/16805.
if platform.system() == "Darwin":
    extra_compile_args += ["-stdlib=libc++"]
    extra_link_args += ["-stdlib=libc++"]

brownian_lib_prefix = os.path.join(".", "csrc")
sources = os.listdir(brownian_lib_prefix)
sources = filter(lambda x: x.endswith('.cpp'), sources)
sources = map(lambda x: os.path.join(brownian_lib_prefix, x), sources)
sources = list(sources)

setuptools.setup(
    name="torchsde",
    version="0.1.0",
    author="Xuechen Li",
    author_email="lxuechen@cs.toronto.edu",
    description="SDE solvers and stochastic adjoint sensitivity analysis in PyTorch.",
    url="https://github.com/google-research/torchsde",
    packages=setuptools.find_packages(exclude=['diagnostics', 'tests']),
    ext_modules=[
        cpp_extension.CppExtension(name='torchsde._brownian_lib',
                                   sources=sources,
                                   extra_compile_args=extra_compile_args,
                                   extra_link_args=extra_link_args,
                                   optional=True)
    ],
    cmdclass={'build_ext': cpp_extension.BuildExtension},
    install_requires=['torch>=1.5.0', 'blist', 'numpy>=1.17.0', 'scipy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
)
