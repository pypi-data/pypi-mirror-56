//  SuperTuxKart - a fun racing game with go-kart
//  Copyright (C) 2014-2015 SuperTuxKart-Team
//
//  This program is free software; you can redistribute it and/or
//  modify it under the terms of the GNU General Public License
//  as published by the Free Software Foundation; either version 3
//  of the License, or (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program; if not, write to the Free Software
//  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

#include "network/network_string.hpp"

#include "utils/string_utils.hpp"

#include <algorithm>   // for std::min
#include <iomanip>
#include <ostream>

// ============================================================================
/** Unit testing function.
 */
void NetworkString::unitTesting()
{
}   // unitTesting

// ============================================================================

// ----------------------------------------------------------------------------
/** Adds one byte for the length of the string, and then (up to 255 of)
 *  the characters of the given string. */
BareNetworkString& BareNetworkString::encodeString(const std::string &value)
{
    int len = (int)value.size();
    if(len<=255)
        return this->addUInt8(len).addString(value);
    else
        return addUInt8(255).addString(value.substr(0, 255));
}   // encodeString

// ----------------------------------------------------------------------------
 /** Adds one byte for the length of the string, and then (up to 255 of)
 *  the characters of the given string. */
BareNetworkString& BareNetworkString::encodeString(const irr::core::stringw &value)
{
    std::string v = StringUtils::wideToUtf8(value);
    return encodeString(v);
}   // encodeString

// ----------------------------------------------------------------------------
/** Returns a string at the given position. The first byte indicates the
 *  length, followed by the actual string (not 0 terminated).
 *  \param[in] pos Buffer position where the encoded string starts.
 *  \param[out] out The decoded string.
 *  \return number of bytes read = 1+length of string
 */
int BareNetworkString::decodeString(std::string *out) const
{
    uint8_t len = get<uint8_t>();
    *out = getString(len);
    return len+1;
}    // decodeString

// ----------------------------------------------------------------------------
/** Returns an irrlicht wide string from the utf8 encoded string at the 
 *  given position.
 *  \param[out] out The decoded string.
 *  \return number of bytes read. If there are no special characters in the
 *          string that will be 1+length of string, but multi-byte encoded
 *          characters can mean that the length of the returned string is
 *          less than the number of bytes read.
 */
int BareNetworkString::decodeStringW(irr::core::stringw *out) const
{
    std::string s;
    int len = decodeString(&s);
    *out = StringUtils::utf8ToWide(s);
    return len;
}   // decodeStringW

// ----------------------------------------------------------------------------
/** Encode string with max length of 16bit and utf32, used in motd or
 *  chat. */
BareNetworkString& BareNetworkString::encodeString16(
                                               const irr::core::stringw& value)
{
    size_t utf32_len = 0;
    const uint32_t* utf32 = NULL;
    std::u32string convert;

    if (sizeof(wchar_t) == 2)
    {
        convert = StringUtils::wideToUtf32(value);
        utf32_len = convert.size();
        utf32 = (const uint32_t*)convert.c_str();
    }
    else
    {
        utf32_len = value.size();
        utf32 = (const uint32_t*)value.c_str();
    }

    uint16_t str_len = (uint16_t)utf32_len;
    if (utf32_len > 65535)
        str_len = 65535;
    addUInt16(str_len);
    for (unsigned i = 0; i < str_len; i++)
        addUInt32(utf32[i]);
    return *this;
}   // encodeString16

// ----------------------------------------------------------------------------
int BareNetworkString::decodeString16(irr::core::stringw* out) const
{
    uint16_t str_len = getUInt16();
    std::u32string convert;
    for (unsigned i = 0; i < str_len; i++)
    {
        uint32_t c = getUInt32();
        if (sizeof(wchar_t) == 2)
            convert += (char32_t)c;
        else
            out->append((wchar_t)c);
    }
    if (str_len > 0 && !convert.empty())
        *out = StringUtils::utf32ToWide(convert);
    return str_len * 4 + 2;
}   // decodeString16

// ----------------------------------------------------------------------------
/** Returns a string representing this message suitable to be printed
 *  to stdout or via the Log mechanism. Format
 *   0000 : 1234 5678 9abc  ...    ASCII-
 */
std::string BareNetworkString::getLogMessage(const std::string &indent) const
{
    std::ostringstream oss;
    for(unsigned int line=0; line<m_buffer.size(); line+=16)
    {
        oss << "0x" << std::hex << std::setw(3) << std::setfill('0') 
            << line << " | ";
        unsigned int upper_limit = std::min(line+16, (unsigned int)m_buffer.size());
        for(unsigned int i=line; i<upper_limit; i++)
        {
            oss << std::hex << std::setfill('0') << std::setw(2) 
                << int(m_buffer[i])<< ' ';
            if(i%8==7) oss << " ";
        }   // for i
        // fill with spaces if necessary to properly align ascii columns
        for(unsigned int i=upper_limit; i<line+16; i++)
        {
            oss << "   ";
            if (i%8==7) oss << " ";
        }

        // Add ascii representation
        oss << " | ";
        for(unsigned int i=line; i<upper_limit; i++)
        {
            uint8_t c = m_buffer[i];
            // Don't print tabs, and characters >=128, which are often shown
            // as more than one character.
            if(isprint(c) && c!=0x09 && c<=0x80)
                oss << char(c);
            else
                oss << '.';
        }   // for i
        oss << "\n";
        // If it's not the last line, add the indentation in front
        // of the next line
        if(line+16<m_buffer.size())
            oss << indent;
    }   // for line

    return oss.str();
}   // getLogMessage

