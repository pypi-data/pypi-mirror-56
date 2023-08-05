# Copyright (C) 2019 Joshua Kim Rivera
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
# associated documentation files (the "Software"), to deal in the Software without restriction, including without
# limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import base64
import os
import requests
import json
from robotlibcore import HybridCore,keyword

from PIL import Image

__version__ = '0.3dev'


class CaptchaLibrary(HybridCore):
    """ ``CaptchaLibrary`` is a Robotframework Test Library for decoding captchas.

    This document explains the usage of each keywords in this test library.

    == Table of contents ==
    - `Importing`
    - `About`
    - `Developer Manual`
    - `Shortcuts`
    - `Keywords`

    == Importing ==

    | =Settings=    | =Value=           | =Parameter=                           |
    | Library       | CaptchaLibrary    | http://www.sample/captcha/service/url |

    == About ==

    Created: 23/09/2019  

    Author: Joshua Kim Rivera | joshua.rivera@mnltechnology.com  

    Company: Spiralworks Technologies Inc.  


    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__
    
    def __init__(self,  serviceUrl=None,
                        header={'Content-Type':'application/x-www-form-urlencoded'},
                        payloadType='base64Captcha'
                ):
        """CaptchaLibrary requires that you provide the captha service's url upon import.

        - ``serviceUrl``:
            The Captcha URL Service.
        - ``header``
            (optional) default = Content-Type=application/x-www-form-urlencoded
        - ``payloadType``:
            (optional) default = base64Captcha
        """
        libraries = [
        ]
        HybridCore.__init__(self,libraries)
        self.payloadType = payloadType
        self.header = header
        self.serviceUrl = serviceUrl

    @keyword
    def capture_element_from_screenshot(self, imagepath, location, size, outputPath):
        """Crops the specified element from a screenshot given the location and size.

        :param imagepath: path to the captcha image
        :param location: element location, must be a dictionary
        :param size: element size, must be a dictionary
        :param outputPath
        :return: None

        """
        image = Image.open(imagepath)
        element = image.crop((  int(location['x']),
                                int(location['y']),
                                int(size['width'])+int(location['x']),
                                int(size['height'])+int(location['y'])
                            ))
        element.save(outputPath)

    @keyword
    def convert_captcha_image_to_base64(self, imagepath):
        """Converts the supplied captcha image to a Base64 String
        fails if the image does not exist

        :param imagepath
        :return base64 string
        """
        try:
            with open(imagepath, "rb") as img_file:
	            decoded_string = base64.b64encode(img_file.read())
            decoded_string = decoded_string.decode("utf-8")
            return decoded_string

        except Exception as err:
            raise err
    
    @keyword
    def get_bypass_captcha_token(self, baseURL, header={'Accept': 'application/json'}):
        """Send a GET Request to the base URL to retrieve the token to be 
            used to bypass the captcha.
        """
        return self._create_get_request_for_captcha_bypass_token(baseURL, header)

    def _create_get_request_for_captcha_bypass_token(self, baseURL, header):
        """
        """
        req = requests.get(baseURL, headers=header)
        req = req.json()
        return req['ResponseData']

    def _send_post_request_to_service_url(self, serviceUrl, header, payload):
        """Send a POST Request to the Captcha Service API
        
        """
        req = requests.post(serviceUrl,data=payload,headers=header)
        return req

    @keyword
    def decode_base64_captcha(self, imagepath):
        """Decodes the Base64 Captcha Image by converting the supplied captcha image and sending a request to the 
        captcha service URL

        :param imagepath
        :return the decoded captcha string

        """
        base64_string = self.convert_captcha_image_to_base64(imagepath)
        payload = {self.payloadType:base64_string}
        decoded_string = self._send_post_request_to_service_url(self.serviceUrl, self.header, payload)
        return decoded_string.text

