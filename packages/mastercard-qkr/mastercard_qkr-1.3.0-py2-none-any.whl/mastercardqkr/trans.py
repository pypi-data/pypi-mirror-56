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

class Trans(BaseObject):
    """
    
    """

    __config = {
        
        "474791ab-51fc-4f4e-a229-a5bea1de2a07" : OperationConfig("/labs/proxy/qkr2/internal/api2/trans", "create", ["X-Auth-Token"], []),
        
        "8f5a5a33-fc05-4f8a-ae35-9ccae859d5f4" : OperationConfig("/labs/proxy/qkr2/internal/api2/trans", "query", ["X-Auth-Token"], ["from","to"]),
        
        "c67ac159-c9ed-4ba5-b836-5d1c2f4dabb2" : OperationConfig("/labs/proxy/qkr2/internal/api2/trans/{id}", "read", ["X-Auth-Token"], []),
        
        "539b9ae4-0287-4cae-b1d3-218e354f06c5" : OperationConfig("/labs/proxy/qkr2/internal/api2/trans/{id}", "update", ["X-Auth-Token"], []),
        
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
        Creates object of type Trans

        @param Dict mapObj, containing the required parameters to create a new object
        @return Trans of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("474791ab-51fc-4f4e-a229-a5bea1de2a07", Trans(mapObj))











    @classmethod
    def query(cls,criteria):
        """
        Query objects of type Trans by id and optional criteria
        @param type criteria
        @return Trans object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("8f5a5a33-fc05-4f8a-ae35-9ccae859d5f4", Trans(criteria))





    @classmethod
    def read(cls,id,criteria=None):
        """
        Returns objects of type Trans by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of Trans
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

        return BaseObject.execute("c67ac159-c9ed-4ba5-b836-5d1c2f4dabb2", Trans(mapObj))



    def update(self):
        """
        Updates an object of type Trans

        @return Trans object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("539b9ae4-0287-4cae-b1d3-218e354f06c5", self)






