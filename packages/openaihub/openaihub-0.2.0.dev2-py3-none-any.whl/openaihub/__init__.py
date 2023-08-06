# Copyright 2019 IBM Corporation 
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
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
name = "openaihub"

import openaihub.func as func
install = func.install
install_operator = func.install_operator
register = func.register
install_application = func.install_application
uninstall_application = func.uninstall_application
get_applications = func.get_applications

__all__ = ["install", 
           "install_operator", 
           "register", 
           "install_application", 
           "uninstall_application",
           "get_applications"]
           