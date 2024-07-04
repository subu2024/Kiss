# KISS - Static Site Generator based on Python 3
# (keep it simple senorita)
# Key features - see readme.md
# filename - main.py 

# The MIT License (MIT)
#
# Copyright (c) Lumos AI LLC
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# custom modules
# read and parse the customization variables
import configParser as config
# read and parse data
import myDatabase as db
# the heart and soul of this project
import blogEngine as blogger
# the debugging engine
import programWatch as pwatch

import datetime


def main():

    start_process = datetime.datetime.now()
    all_data = {}

    # read the config file
    #all_data = {'site': config.site}
    
    pwatch.summary_write("begin build ..", config.show_summary)
    pwatch.summary_write(str(config.site['title'] + " " + config.site['ver']), config.show_summary)

    # read data file
    all_data =  db.read_data(config, pwatch)
    # now include the site data 
    all_data['site'] =  config.site #TBD is there a better way?

    
    # call blogger to create the final file
    blogger.start(all_data, config, pwatch )

    # stats on computing time
    time_diff = (datetime.datetime.now() - start_process).total_seconds()

    pwatch.summary_write("process time in seconds " + str(time_diff), config.show_summary)
    pwatch.summary_write(".. end build", config.show_summary)


# letting python know explicitly where to start
if __name__ == '__main__':
    main()