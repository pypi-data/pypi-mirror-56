# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools

from tftest import __version__


with open("README.md", "r") as fh:
  long_description = fh.read()


setuptools.setup(
    name="tftest",
    version=__version__,
    author="Ludovico Magnocavallo",
    author_email="ludomagno@google.com",
    description="Simple Terraform test helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GoogleCloudPlatform/terraform-python-testing-helper",
    py_modules=['tftest'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    setup_requires=['nose>=1.3'],
    test_suite='nose.collector'
)
