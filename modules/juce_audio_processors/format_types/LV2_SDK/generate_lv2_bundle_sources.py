# ==============================================================================

#  This file is part of the JUCE framework.
#  Copyright (c) Raw Material Software Limited

#  JUCE is an open source framework subject to commercial or open source
#  licensing.

#  By downloading, installing, or using the JUCE framework, or combining the
#  JUCE framework with any other source code, object code, content or any other
#  copyrightable work, you agree to the terms of the JUCE End User Licence
#  Agreement, and all incorporated terms including the JUCE Privacy Policy and
#  the JUCE Website Terms of Service, as applicable, which will bind you. If you
#  do not agree to the terms of these agreements, we will not license the JUCE
#  framework to you, and you must discontinue the installation or download
#  process and cease use of the JUCE framework.

#  JUCE End User Licence Agreement: https://juce.com/legal/juce-8-licence/
#  JUCE Privacy Policy: https://juce.com/juce-privacy-policy
#  JUCE Website Terms of Service: https://juce.com/juce-website-terms-of-service/

#  Or:

#  You may also use this code under the terms of the AGPLv3:
#  https://www.gnu.org/licenses/agpl-3.0.en.html

#  THE JUCE FRAMEWORK IS PROVIDED "AS IS" WITHOUT ANY WARRANTY, AND ALL
#  WARRANTIES, WHETHER EXPRESSED OR IMPLIED, INCLUDING WARRANTY OF
#  MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, ARE DISCLAIMED.
#
# ==============================================================================

# This script is used to convert the data files from the LV2 distribution into
# a form suitable for inclusion in a C++ project. An LV2 host would normally
# expect these files to be installed on disk, but this places a burden on host
# developers to include these files in their product installers, and to install
# them to sensible locations. Instead of forcing host developers to handle this
# case, JUCE hosts will use the embedded copy of this data to write all of the
# files to a temporary location at runtime.

import argparse
import os

BUNDLE_TEMPLATE = """juce::lv2::Bundle
{{
"{}",
{{
{}
}}
}}
"""

BUNDLE_RESOURCE_TEMPLATE = """juce::lv2::BundleResource
{{
"{}",
{}
}}
"""

FUNCTION_TEMPLATE = """/*
  ==============================================================================

   This file is part of the JUCE framework.
   Copyright (c) Raw Material Software Limited

   JUCE is an open source framework subject to commercial or open source
   licensing.

   By downloading, installing, or using the JUCE framework, or combining the
   JUCE framework with any other source code, object code, content or any other
   copyrightable work, you agree to the terms of the JUCE End User Licence
   Agreement, and all incorporated terms including the JUCE Privacy Policy and
   the JUCE Website Terms of Service, as applicable, which will bind you. If you
   do not agree to the terms of these agreements, we will not license the JUCE
   framework to you, and you must discontinue the installation or download
   process and cease use of the JUCE framework.

   JUCE End User Licence Agreement: https://juce.com/legal/juce-8-licence/
   JUCE Privacy Policy: https://juce.com/juce-privacy-policy
   JUCE Website Terms of Service: https://juce.com/juce-website-terms-of-service/

   Or:

   You may also use this code under the terms of the AGPLv3:
   https://www.gnu.org/licenses/agpl-3.0.en.html

   THE JUCE FRAMEWORK IS PROVIDED "AS IS" WITHOUT ANY WARRANTY, AND ALL
   WARRANTIES, WHETHER EXPRESSED OR IMPLIED, INCLUDING WARRANTY OF
   MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, ARE DISCLAIMED.

  ==============================================================================
*/

/*
    This file is auto-generated by generate_lv2_bundle_sources.py.
*/

#pragma once

#ifndef DOXYGEN

#include <vector>

namespace juce
{{
namespace lv2
{{

struct BundleResource
{{
    const char* name;
    const char* contents;
}};

struct Bundle
{{
    const char* name;
    std::vector<BundleResource> contents;

    static std::vector<Bundle> getAllBundles();
}};

}}
}}

std::vector<juce::lv2::Bundle> juce::lv2::Bundle::getAllBundles()
{{
    return {{
{}
}};
}}

#endif"""


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_chunked_string_literal(s):
    return ' '.join(map(lambda x: 'R"lv2ttl({})lv2ttl"'.format(''.join(x)), chunks(s, 8000)))


def get_file_source_string(ttl):
    with open(ttl) as f:
        return BUNDLE_RESOURCE_TEMPLATE.format(os.path.basename(ttl),
                                               get_chunked_string_literal(f.read()))


def generate_bundle_source(root, files):
    if len(files) == 0:
        return ""

    return BUNDLE_TEMPLATE.format(os.path.basename(root),
                                  ", ".join(get_file_source_string(os.path.join(root, ttl)) for ttl in files))

def filter_turtle(files):
    return [f for f in files if f.endswith(".ttl")]


def filter_ttl_files(lv2_dir):
    for root, _, files in os.walk(args.lv2_dir):
        yield root, filter_turtle(files)


parser = argparse.ArgumentParser()
parser.add_argument("lv2_dir")
args = parser.parse_args()

print(FUNCTION_TEMPLATE.format(", ".join(generate_bundle_source(root, files)
                                         for root, files in filter_ttl_files(args.lv2_dir)
                                         if len(files) != 0))
                       .replace("\t", "    "),
      end = "\r\n")
