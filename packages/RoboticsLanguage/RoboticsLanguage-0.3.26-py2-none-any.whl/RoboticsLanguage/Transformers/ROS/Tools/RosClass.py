#
#   This is the Robotics Language compiler
#
#   Topics.py: Processes all code for Ros topics, messages and types
#
#   Created on: June 22, 2017
#       Author: Gabriel A. D. Lopes
#      Licence: Apache 2.0
#    Copyright: 2014-2017 Robot Care Systems BV, The Hague, The Netherlands. All rights reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from RoboticsLanguage.Base import Utilities

def process(code, parameters):

  for item in code.xpath('//RosClass'):

      package_name = item.xpath('./option[@name="package"]/string/text()')[0]

      parameters['Transformers']['ROS']['buildDependencies'].add(package_name)
      parameters['Transformers']['ROS']['runDependencies'].add(package_name)

  return code, parameters
