import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.lines as mlines 
import welly
import lasio
from utils import style_line, get_ticks, get_xlim, get_scale



class stdlog:
    """Python standardized logs class"""
    def __init__(self, fpath):
        """Create a well object - 
                
                params:
                    - Path to .las file directory
        """
        
        self.fpath = fpath
        self.wellobject = None
    
    def get_data(self, mnemonics):
        """Uploads log data from .las data"""
            
        """ params: mnemonics(dict) - Dictionory Containing the custom mnemonics being used in the las.
                                      stdlog package works with preset mnemonics names that helps in scaling and standardizing,
                                      as of current version 1.0 we for now use most popular ones:
                                            {    pre-set  custom
                                                 ===================
                                                'GR':   gamma ray, 
                                                'CALI': caliper ,
                                                'DEPTH': Measured Depth,
                                                'TVD':   True Vertical Depth,
                                                'LL9S':  Short resistivity Lateralog,
                                                'LL9D':  Long resistivity lateralog,
                                                'MSFL':  Micro Spherical,
                                                'RT':    True Resistivity,
                                                'RX0':   Flushed Zone Resistivity,
                                                'CNL':   Neutron,
                                                'DENS':  Density,
                                                'SONI':  Sonic 

                                            }
        """
        
        
        _well = {}
        input_mnemonics = list(mnemonics.keys())
        data = welly.Well.from_las(self.fpath)
        expanded_data = data.df()
        expanded_data[expanded_data.index.name.upper()] = expanded_data.index
        
        self.wellobject = data
        
        for mnem in input_mnemonics:
            if mnem == 'DEPTH':
                log_data = 3.28084 * np.array(expanded_data[mnemonics[mnem]])
                _well[mnem] = log_data
            else:
                log_data = np.array(expanded_data[mnemonics[mnem]])
                _well[mnem] = log_data
                
        return _well

    def visualize (self, mnemonics,  pltrange, tracks = None, sbsline = None ):
        """Visualizes the given log data in standard form"""
        
        """
             params: mnemonics(dict) - Dictionory Containing the custom mnemonics being used in the las.
                                      stdlog package works with preset mnemonics names that helps in scaling and standardizing,
                                      as of current version 1.0 we for now use most popular ones:
                                            {    pre-set  custom
                                                 ===================
                                                'GR':   gamma ray, 
                                                'CALI': caliper ,
                                                'DEPTH': Measured Depth,
                                                'TVD':   True Vertical Depth,
                                                'LL9S':  Short resistivity Lateralog,
                                                'LL9D':  Long resistivity lateralog,
                                                'MSFL':  Micro Spherical,
                                                'RT':    True Resistivity,
                                                'RX0':   Flushed Zone Resistivity,
                                                'CNL':   Neutron,
                                                'DENS':  Density,
                                                'SONI':  Sonic 

                                            }
                    tracks(list)  - nested list of tracks !! DEPTH and TVD should always be given in the second place
                                    Example:
                                       [['GR', 'CALI'], ['DEPTH', 'TVD'], ['CNL']]
                                       
                                       
                    pltrange(tuple) - A tuple for indicating plot min and max ranges - This is useful when comparing multiple wells that 
                                      all plots are in the same range 
                                      
                    
                    sbsline(tuple)  -  (position, state) Shalebaseline specific to Gamma Ray tracks
        """
                
        
        
        
        if not isinstance(tracks, list) and not isinstance(pltrange, tuple):
            print("Tracks should be given as nested lists representing individual tracks and pltrange as tuple")
            print("Terminated .....")
        
        else:
            well = self.get_data(mnemonics)
            
            conn = np.ones(len(well['DEPTH']))
            field_top, field_bottom = pltrange
            numtracks = len(tracks)
            topdiff = min(well['DEPTH']) - field_top
            bottomdiff =field_bottom - max(well['DEPTH'])
            mdbounds = [min(well['TVD']) - topdiff, max(well['TVD']) + bottomdiff]
            
            fig = plt.figure(figsize=(numtracks*4, 60))
            
            for i in range(1,numtracks + 1):
                host = fig.add_subplot(1, numtracks, i)


                # Building AX for log tracks
                if i != 2:

                    # For multi track
                    if isinstance(tracks[i-1], list):
                        nested_track = tracks[i-1]
                        
                      
                        
                        
                        d  = 0 
                        for j in range(len(nested_track)):
                            if nested_track[j] == 'GR':
                                grpos = i
                        
                            ax = host.twiny()
                            plt.setp(obj = ax, ylim = (field_top, field_bottom)[::-1], 
                                               xlim = get_xlim(nested_track[j]),
                                               xscale = get_scale(nested_track[j]))

                            c, ls = style_line(nested_track[j])

                            ax.xaxis.set_ticks_position('top')
                            ax.tick_params(axis='x', colors=c)
                            ax.spines['top'].set_position(('outward', 2+d))
                            d+=40

                            if len(get_ticks(nested_track[j])) == 0:
                                ax.plot(well[nested_track[j]], well['DEPTH'], c, ls = ls)
                                ax.set_xlabel(nested_track[j], color = c)    
                                host.set_yticks(get_ticks('DEPTH', field_top, field_bottom))
                                host.set_yticklabels([])
                                ax.grid(True, which = 'both', c = 'k', lw = 0.5, axis = 'both')

                            else:
                                ax.set_xticks(get_ticks(nested_track[j]), minor = False)    
                                ax.plot(well[nested_track[j]], well['DEPTH'], c, ls = ls)
                                ax.set_xlabel(nested_track[j], color = c)
                                host.set_yticks(get_ticks('DEPTH', field_top, field_bottom))
                                host.set_yticklabels([])

                            if j == 0:
                                host.grid(True, which = 'major', axis = 'both', color = 'k')


                # for DEPTH TVD track
                else:


                    host.plot(conn, well['DEPTH'], alpha = 0)
                    plt.setp(obj = host, ylim = (field_top, field_bottom)[::-1])
                    host.set_xlabel('MD[ft] --- TVD[ft]')
                    host.xaxis.set_label_position('top')
                    host.set_yticks(get_ticks('DEPTH', field_top, field_bottom))

                    host.tick_params(axis ='y', which = 'major', length = 4, pad = -45, direction = 'in')

                    host.grid(True, which = 'both', axis = 'y')


                    host = host.twinx()
                    host.plot(conn, well['TVD'], alpha = 0)
                    host.set_ylim(mdbounds[0], mdbounds[1])
                    host.set_yticks(get_ticks('DEPTH', mdbounds[0], mdbounds[1]))
                    host.tick_params(axis ='y', which = 'major', length = 4, pad = -45, direction = 'in')
                    host.grid(True, which = 'both', axis = 'y', ls = '--')

                    host.invert_yaxis()
                    
                if sbsline is not None:
                    val, state = sbsline
                    
                    xval = np.repeat(val, 10)
                    yval = np.linspace(field_top, field_bottom, 10)
                    # print("1{}{}".format(numtracks, grpos))
                    ax = fig.axes[grpos]
                    line = mlines.Line2D([100,100], [9000, 13000], color='red')
                    ax.add_line(line)
                    
            return plt     
        
