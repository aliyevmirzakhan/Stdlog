import numpy as np

def style_line(track_name):

    if track_name == 'GR':
        return ('g', '-')
    if track_name ==  'CALI':
        return ('k', '-')
    if track_name == 'LL9S':
        return ('b', '--')
    if track_name ==  'LL9D':
        return ('r', '-')
    if track_name ==  'MSFL':
        return ('k', '--')
    if track_name ==  'RT':
        return ('b', '-.')
    if track_name ==  'RX0':
        return ('r', '-')
    if track_name ==  'CNL':
        return ('m', '-')
    if track_name ==  'DENS':
        return ('b', '--')
    if track_name ==  'SONI':
        return ('k', '-')
    
def get_ticks(track_name, ymin = None, ymax = None):

    if track_name == 'GR':
        return np.arange(0, 151, 150)
    if track_name ==  'CALI':
        return np.arange(0,17, 16)
    if track_name == 'DEPTH':
        return np.arange(ymin, ymax+1, 25)
    if track_name == 'LL9S':
        return []
    if track_name == 'LL9D':
        return []
    if track_name == 'MSFL':
        return []
    if track_name == 'RT':
        return []
    if track_name == 'RX0':
        return []
    if track_name == 'CNL':
        n = np.arange(-15, 46, 60)
        return n[::-1]
    if track_name == 'DENS':
        return np.arange(1.95, 2.96, 1)
    if track_name == 'SONI':
        return np.arange(40, 201, 160)[::-1]




def get_xlim (track_name):
    if track_name == 'GR':
        return (0, 150)
    if track_name == 'CALI':
        return (0,16)
    if track_name == 'LL9S':
        return (0.2, 2000)
    if track_name == 'LL9D':
        return (0.2, 2000)
    if track_name == 'MSFL':
        return (0.2, 2000)
    if track_name == 'RT':
        return (0.2, 2000)
    if track_name == 'RX0':
        return (0.2, 2000)
    if track_name == 'CNL':
        return (45, -15)
    if track_name == 'DENS':
        return (1.95, 2.95)
    if track_name == 'SONI':
        return (200, 40)


def get_scale(track_name):
    if (track_name == 'GR') | (track_name == 'CALI') | (track_name == 'CNL') | (track_name == 'DENS') | (track_name == 'SONI'):
        return 'linear'
    if (track_name == 'LL9S') | (track_name == 'LL9D') | (track_name == 'MSFL') | (track_name == 'RT') | (track_name == 'RX0'):
        return 'log'
    


if __name__ == '__main___':
    style_line('GR')
    get_ticks('GR')
    get_xlim('GR')
    get_scale('GR')
