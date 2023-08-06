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

class Cart(BaseObject):
    """
    
    """

    __config = {
        
        "9b4c2cf0-adfe-4117-8f14-2920918643d3" : OperationConfig("/labs/proxy/qkr2/internal/api2/cart/{id}", "delete", ["X-Auth-Token"], []),
        
        "c9f081aa-c690-42b9-b4e5-bf9385b25b5e" : OperationConfig("/labs/proxy/qkr2/internal/api2/cart", "query", ["X-Auth-Token"], []),
        
        "cac52d46-cf6e-4870-803b-24caff78ecf7" : OperationConfig("/labs/proxy/qkr2/internal/api2/cart/{id}", "read", ["X-Auth-Token"], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())





    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type Cart by id

        @param str id
        @return Cart of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("9b4c2cf0-adfe-4117-8f14-2920918643d3", Cart(mapObj))

    def delete(self):
        """
        Delete object of type Cart

        @return Cart of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("9b4c2cf0-adfe-4117-8f14-2920918643d3", self)








    @classmethod
    def query(cls,criteria):
        """
        Query objects of type Cart by id and optional criteria
        @param type criteria
        @return Cart object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("c9f081aa-c690-42b9-b4e5-bf9385b25b5e", Cart(criteria))





    @classmethod
    def read(cls,id,criteria=None):
        """
        Returns objects of type Cart by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of Cart
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

        return BaseObject.execute("cac52d46-cf6e-4870-803b-24caff78ecf7", Cart(mapObj))



