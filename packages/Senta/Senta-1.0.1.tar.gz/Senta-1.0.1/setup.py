# -*- coding: UTF-8 -*-
################################################################################
#
#   Copyright (c) 2019  Baidu.com, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

"""
Setup script.

"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Senta",
    version="1.0.1",
    author="Baidu NLP",
    author_email="jiyunjie@baidu.com",
    description="A sentiment classification tools made by Baidu NLP.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PaddlePaddle/models/tree/develop/PaddleNLP/sentiment_classification",
    # packages=setuptools.find_packages(),
    packages = ['Senta'],
    package_dir={'Senta':'Senta'},
    package_data={'Senta':['*.*', 'char_bilstm_final_model/*', 'infer_model/*', 'conf/*']},
    install_requires=[],
    platforms = "any",
    license='Apache 2.0',

    classifiers = [
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
          ],
)

