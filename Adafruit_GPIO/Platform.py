# Copyright (c) 2014 Adafruit Industries
# Copyright (c) 2024 Cam Parsfield

# Author: Tony DiCola
# Author: Cam Parsfield

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import platform
import re

# Platform identification constants.
UNKNOWN          = 0
RASPBERRY_PI     = 1
BEAGLEBONE_BLACK = 2
MINNOWBOARD      = 3

def platform_detect():
    """Detect if running on the Raspberry Pi, Beaglebone Black, or other platforms, and return the
    platform type. Will return RASPBERRY_PI, BEAGLEBONE_BLACK, MINNOWBOARD, or UNKNOWN."""
    
    #print("Running platform detection...")  # Debugging output
    
    # Handle Raspberry Pi
    pi = pi_version()
    if pi is not None:
        print(f"Detected Raspberry Pi version: {pi}")  # Debugging output
        return RASPBERRY_PI

    # Handle Beaglebone Black
    plat = platform.platform()
    if 'armv7l-with-debian' in plat.lower():
        return BEAGLEBONE_BLACK
    elif 'armv7l-with-ubuntu' in plat.lower():
        return BEAGLEBONE_BLACK
    elif 'armv7l-with-glibc2.4' in plat.lower():
        return BEAGLEBONE_BLACK
        
    # Handle Minnowboard
    try: 
        import mraa 
        if mraa.getPlatformName() == 'MinnowBoard MAX':
            return MINNOWBOARD
    except ImportError:
        pass
    
    print("Platform detection failed: UNKNOWN platform.")  # Debugging output
    
    # Couldn't figure out the platform, just return unknown.
    return UNKNOWN

def pi_revision():
    """Detect the revision number of a Raspberry Pi, useful for changing
    functionality like default I2C bus based on revision."""
    # Revision list available at: http://elinux.org/RPi_HardwareHistory#Board_Revision_History
    with open('/proc/cpuinfo', 'r') as infile:
        cpuinfo = infile.read()
        print(cpuinfo)  # Debugging output
        for line in cpuinfo.splitlines():
            # Match a line of the form "Revision : 0002"
            match = re.match(r'Revision\s+:\s+(\w+)', line, flags=re.IGNORECASE)
            if match:
                revision = match.group(1)
                print(f"Detected Pi revision: {revision}")  # Debugging output
                return revision
        # Couldn't find the revision, throw an exception.
        raise RuntimeError('Could not determine Raspberry Pi revision.')

def pi_version():
    """Detect the version of the Raspberry Pi. Returns a version number (1, 2, 3, 4, 5, Zero, Pico)
    depending on if it's a Raspberry Pi 1, 2, 3, 4, 5, Zero, Pico or None if not a Raspberry Pi.
    """
    print("Reading /proc/cpuinfo...")  # Debugging output
    revision = pi_revision()
    
    pi_revisions = {
        # Raspberry Pi 1 Models
        '0002': 1,  # Model B Rev 1
        '0003': 1,  # Model B Rev 1 (ECN0001)
        '0004': 1,  # Model B Rev 2
        '0005': 1,  # Model B Rev 2
        '0006': 1,  # Model B Rev 2
        '0007': 1,  # Model A
        '0008': 1,  # Model A
        '0009': 1,  # Model A
        '000d': 1,  # Model B Rev 2
        '000e': 1,  # Model B Rev 2
        '000f': 1,  # Model B Rev 2
        '0010': 1,  # Model B+
        '0011': 1,  # Compute Module 1
        '0012': 1,  # Model A+
        '0013': 1,  # Model B+
        '0014': 1,  # Compute Module 1
        '0015': 1,  # Model A+
        # Raspberry Pi 2 Models
        'a01041': 2,  # Pi 2 Model B v1.1
        'a21041': 2,  # Pi 2 Model B v1.1
        'a22042': 2,  # Pi 2 Model B v1.2
        # Raspberry Pi 3 Models
        'a02082': 3,  # Pi 3 Model B
        'a22082': 3,  # Pi 3 Model B
        'a32082': 3,  # Pi 3 Model B (Sony, Japan)
        'a020d3': 3,  # Pi 3 Model B+
        '9020e0': 3,  # Pi 3 Model A+
        # Raspberry Pi 4 Models
        'a03111': 4,  # Pi 4 Model B
        'b03111': 4,  # Pi 4 Model B
        'b03112': 4,  # Pi 4 Model B
        'c03111': 4,  # Pi 4 Model B
        'c03112': 4,  # Pi 4 Model B
        'a03140': 4,  # Pi 400
        'a020a0': 4,  # Compute Module 4
        # Raspberry Pi 5 Models
        '9023e0': 5,  # Pi 5 Model B
        # Raspberry Pi Zero Models
        '900092': 'Zero',  # Pi Zero v1.2
        '900093': 'Zero',  # Pi Zero v1.3
        '9000c1': 'Zero',  # Pi Zero W
        '902120': 'Zero 2 W',  # Pi Zero 2 W
        # Raspberry Pi Pico Models
        'e31a': 'Pico',  # Pico
        'e31b': 'Pico',  # Pico W
        'e31c': 'Pico',  # Pico 2
    }

    version = pi_revisions.get(revision, None)
    if version is None:
        print(f"Unknown Raspberry Pi revision: {revision}")  # Debugging output
        return None

    print(f"Detected Raspberry Pi version: {version}")  # Debugging output
    return version
