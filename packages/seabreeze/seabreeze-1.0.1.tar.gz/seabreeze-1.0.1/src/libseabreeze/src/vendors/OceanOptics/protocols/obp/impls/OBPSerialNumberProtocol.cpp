/***************************************************//**
 * @file    OBPSerialNumberProtocol.cpp
 * @date    February 2011
 * @author  Ocean Optics, Inc.
 *
 * LICENSE:
 *
 * SeaBreeze Copyright (C) 2014, Ocean Optics Inc
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject
 * to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *******************************************************/

#include "common/globals.h"
#include "vendors/OceanOptics/protocols/obp/impls/OBPSerialNumberProtocol.h"
#include "vendors/OceanOptics/protocols/obp/exchanges/OBPGetSerialNumberExchange.h"
#include "vendors/OceanOptics/protocols/obp/exchanges/OBPGetSerialNumberMaximumLengthExchange.h"
#include "vendors/OceanOptics/protocols/obp/impls/OceanBinaryProtocol.h"
#include "common/ByteVector.h"
#include "common/exceptions/ProtocolBusMismatchException.h"

using namespace seabreeze;
using namespace seabreeze::oceanBinaryProtocol;
using namespace std;

OBPSerialNumberProtocol::OBPSerialNumberProtocol()
        : SerialNumberProtocolInterface(new OceanBinaryProtocol()) {

}

OBPSerialNumberProtocol::~OBPSerialNumberProtocol() {

}

string *OBPSerialNumberProtocol::readSerialNumber(const Bus &bus) {

    vector<byte> *result;
    string *retval = NULL;

    OBPGetSerialNumberExchange xchange;

    TransferHelper *helper = bus.getHelper(xchange.getHints());
    if(NULL == helper) {
        string error("Failed to find a helper to bridge given protocol and bus.");
        throw ProtocolBusMismatchException(error);
    }

    result = xchange.queryDevice(helper);
    if(NULL == result) {
        string error("Expected queryDevice to produce a non-null result "
            "containing a serial number.  Without this data, it is not possible to "
            "continue.");
        throw ProtocolException(error);
    }

    retval = new string();
    vector<byte>::iterator iter;
    /* This is probably not the most efficient way to copy
     * from a vector of bytes into a string, but at least
     * this way issues of string encoding should be
     * avoided (i.e. the sizeof a string element is not
     * assumed here).  Since this function will not be called
     * continuously nor is the serial number ever very long,
     * this should suffice.
     */
    for(iter = result->begin(); iter != result->end(); iter++) {
        retval->push_back((char) * iter);
        if('\0' == *iter) {
            break;
        }
    }

    delete result;

    return retval;
}

unsigned char OBPSerialNumberProtocol::readSerialNumberMaximumLength(const Bus &bus)
{
    vector<byte> *result = NULL;
    unsigned char length;
    
    OBPGetSerialNumberMaximumLengthExchange xchange;
	
    TransferHelper *helper = bus.getHelper(xchange.getHints());
    if(NULL == helper) 
    {
        string error("Failed to find a helper to bridge given protocol and bus.");
        throw ProtocolBusMismatchException(error);
    }
    
	result = xchange.queryDevice(helper);
	if(NULL == result) 
	{
		string error("Expected Transfer::transfer to produce a non-null result "
			"containing temperature.  Without this data, it is not possible to "
			"continue.");
		throw ProtocolException(error);
	}
		
	length=(*result)[0]; 
	delete result;
	
	return length;
}
