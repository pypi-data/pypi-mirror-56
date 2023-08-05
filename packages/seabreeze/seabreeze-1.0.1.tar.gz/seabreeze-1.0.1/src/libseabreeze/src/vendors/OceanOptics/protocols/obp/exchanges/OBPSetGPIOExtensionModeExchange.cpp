/***************************************************//**
 * @file    OBPSetGPIOExtensionModeExchange.cpp
 * @date    April 2017
 * @author  Ocean Optics, Inc.
 *
 * LICENSE:
 *
 * SeaBreeze Copyright (C) 2017, Ocean Optics Inc
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
#include <string.h>
#include "vendors/OceanOptics/protocols/obp/exchanges/OBPSetGPIOExtensionModeExchange.h"
#include "vendors/OceanOptics/protocols/obp/hints/OBPControlHint.h"
#include "vendors/OceanOptics/protocols/obp/constants/OBPMessageTypes.h"

using namespace seabreeze;
using namespace seabreeze::oceanBinaryProtocol;

OBPSetGPIOExtensionModeExchange::OBPSetGPIOExtensionModeExchange()
{

    this->hints->push_back(new OBPControlHint());

    this->messageType = OBPMessageTypes::OBP_SET_EGPIO_MODE;

    this->payload.resize(sizeof(unsigned char)+ sizeof(unsigned char) + sizeof(float)); 
}

OBPSetGPIOExtensionModeExchange::~OBPSetGPIOExtensionModeExchange()
{

}

void OBPSetGPIOExtensionModeExchange::setPinNumber(unsigned char pinNumber)
{
	this->payload[0] = pinNumber;
}

void OBPSetGPIOExtensionModeExchange::setMode(unsigned char mode)
{
	this->payload[1] = mode;
}

void OBPSetGPIOExtensionModeExchange::setValue(float value)
{
	memcpy(&(this->payload[2]), &value, sizeof(float));
}
