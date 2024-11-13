# ImageToASCII
A Python script which converts an arbitrary image file into a collection of ASCII characters. Output is uncolored by default, but may be colored via UNIX color codes.

This was an older project I rewrote for the sake of this portfolio. I'm happy with the end result; I successfully added UNIX coloring to the output and reconfigured the IO such that it may be used though the CLI.

If you have any questions regarding this software, my email is mercerweissx@gmail.com.

# Usage
To convert an image into ASCII, simply pass the image to the script in the terminal:

`$ sudo python3 script.py example.png`

The output's `density` is the number of pixels covered by each ASCII character. The default `density` is 4, meaning each character is representative of every 4th pixel within the image. To set a custom `density`, tack an integer as an option
to the script. For example, to set the `density` to 8:

`$ sudo python3 script.py -8 example.png`

Output may be colored using UNIX color codes using the `-c` option:

`$ sudo python3 script.py -8 -c example.png`

NOTE: Single digit integer options may be combined with `-c`, resulting in `-c8`, however a multi-digit `density` (i.e. 12, 26, 102), must be listed as a separate option. The proper form for these options with a colored output is `-c -26`.

# Copyright and Licensing
Copyright (C) 2024 Xavier Mercerweiss

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
