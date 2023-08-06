#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2016-2020 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#


from __future__ import absolute_import
from mastercardapicore import BaseObject
from mastercardapicore import RequestMap
from mastercardapicore import OperationConfig
from mastercardapicore import OperationMetadata
from mastercardqkr import ResourceConfig

class ExternalTrans(BaseObject):
    """
    
    """

    __config = {
        
        "a2a21d9e-d7a0-49f0-bf14-c5e97dc35342" : OperationConfig("/labs/proxy/qkr2/internal/api2/externalTrans", "create", [], []),
        
        "42319eea-d9cd-4593-9d0c-7e8b9302eada" : OperationConfig("/labs/proxy/qkr2/internal/api2/externalTrans", "query", [], []),
        
        "cc9c2c76-d566-47fa-8f64-1bd5495697e2" : OperationConfig("/labs/proxy/qkr2/internal/api2/externalTrans/{id}", "read", [], []),
        
        "c07f7576-61cb-45b6-abea-5fe15269bec2" : OperationConfig("/labs/proxy/qkr2/internal/api2/externalTrans/{id}", "update", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())


    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type ExternalTrans

        @param Dict mapObj, containing the required parameters to create a new object
        @return ExternalTrans of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("a2a21d9e-d7a0-49f0-bf14-c5e97dc35342", ExternalTrans(mapObj))











    @classmethod
    def query(cls,criteria):
        """
        Query objects of type ExternalTrans by id and optional criteria
        @param type criteria
        @return ExternalTrans object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("42319eea-d9cd-4593-9d0c-7e8b9302eada", ExternalTrans(criteria))





    @classmethod
    def read(cls,id,criteria=None):
        """
        Returns objects of type ExternalTrans by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of ExternalTrans
        @raise ApiException: raised an exception from the response status
        """
        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if criteria:
            if (isinstance(criteria,RequestMap)):
                mapObj.setAll(criteria.getObject())
            else:
                mapObj.setAll(criteria)

        return BaseObject.execute("cc9c2c76-d566-47fa-8f64-1bd5495697e2", ExternalTrans(mapObj))



    def update(self):
        """
        Updates an object of type ExternalTrans

        @return ExternalTrans object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("c07f7576-61cb-45b6-abea-5fe15269bec2", self)






