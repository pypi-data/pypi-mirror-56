# -*- coding: utf-8 -*-
"""
@author: Noemi E. Cazzaniga - 2019
@email: noemi.cazzaniga@polimi.it
"""


from urllib.request import urlopen
from pandas import DataFrame
from pandasdmx import Request
from itertools import product
from gzip import decompress
from re import sub



def get_data(code, flags=False):
    """
    Download an Eurostat dataset.
    Return it as a list of tuples.
    """

    url="https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=data%2F" + code + ".tsv.gz"
    response = urlopen(url)
    try:
        raw_part_data = list(decompress(response.read()).decode('utf-8').partition("\t"))
    except Exception:
        print("FATAL ERROR: '{0}' not found in the Eurostat server.".format(code))
        return
    raw_part_data[2] = sub(r"\t", ",", raw_part_data[2])
    n_text_fields = raw_part_data[0].count(",") + 1
    if flags == True:
        raw_data = raw_part_data[0] + ',' + raw_part_data[2]
        data = [tuple(i.split(',')) for i in raw_data.split('\n')]
        header = list(data[0])
        header[n_text_fields:] = [int(i) for i in header[n_text_fields:]]
        data[0] = tuple(header)
    else:   
        raw_data = raw_part_data[0] + ',' + sub(r"[ a-z:]", "", raw_part_data[2])
        j = 0
        data = []
        for l in raw_data.split('\n'):
            l = l.split(',')
            if j == 0:
                l[n_text_fields:] = [int(i) for i in l[n_text_fields:]]
                j += 1
            else:
                l[n_text_fields:] = [float(i) if i!='' else None for i in l[n_text_fields:]]
            data.append(tuple(l))

    return data



def get_data_df(code, flags=False):
    """
    Download an Eurostat dataset.
    Return it as a Pandas dataframe.
    """
    
    d = get_data(code, flags)
    
    return DataFrame(d[1:], columns = d[0])



def get_dic(code):
    """
    Download an Eurostat dictionary.
    Return it as a list of tuples.
    """

    strerr = 'File {0}'.format(code) + '.dic does not exist or is not readable on the server.'
    tmp = urlopen("https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=dic%2Fen%2F" + code + ".dic")
    dic = []
    for i in tmp.readlines():
        d = i.decode('utf-8').rstrip('\r\n').split('\t')
        if strerr in d:
            print(strerr)
            return
        else:
            dic.append(tuple(d))

    return dic



def get_toc():
    """
    Download the Eurostat table of contents.
    Return it as a list of tuples.
    """
    
    tmp = urlopen("https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=table_of_contents_en.txt").readlines()
    toc = []
    for line in tmp:
        row = sub(r'["\n]','',line.decode('utf-8'))
        toc.append(tuple(row.lstrip().split('\t')[:-1]))

    return toc



def get_sdmx_dims(code):
    """
    Download the Eurostat dimension names of a dataset available via SDMX service.
    Return them as a list.
    """
    
    estat = Request('ESTAT', timeout = 100.)
    try:
        structure = estat.datastructure('DSD_'+code)
    except Exception:
        print("FATAL ERROR: '{0}' not found in the Eurostat server.".format(code))
        return
    dims = list(structure.write().conceptscheme.reset_index()['level_1'][1:])
    try:
        dims.remove('OBS_VALUE')
    except:
        pass
    try:
        dims.remove('OBS_STATUS')
    except:
        pass
    try:
        dims.remove('PERIOD')
    except:
        pass
    
    return dims



def get_sdmx_dic(code, dim):
    """
    Download the Eurostat dimension values with their meaning of a dataset available via SDMX service.
    Return them as a dictionary.
    """
    
    estat = Request('ESTAT', timeout = 100.)
    try:
        structure = estat.datastructure('DSD_'+code)
    except Exception:
        print("FATAL ERROR: '{0}' not found in the Eurostat server.".format(code))
        return
    try:
        idx = structure.write().codelist.loc[dim].reset_index()['index'][1:]
        name = structure.write().codelist.loc[dim].reset_index()['name'][1:]
    except Exception:
        print("FATAL ERROR: Dimension '{0}' not found for the dataset '{1}'.".format(dim, code))
        return
    vals = dict(zip(idx, name))
    
    return vals



def get_sdmx_data(code, StartPeriod, EndPeriod, filter_pars, verbose=False):
    """
    Download a subset of an Eurostat dataset available via SDMX service.
    Return it as a list of tuples.
    """
    
    estat = Request('ESTAT', timeout = 100.)
    dims = filter_pars.keys()
    filter_lists = [tuple(zip((d,)*len(filter_pars[str(d)]),filter_pars[str(d)])) for d in dims]
    cart = [el for el in product(*filter_lists)]
    cart_len = len(cart)
    data = []
    if verbose:
        i = 0
        print("\rProgress: {:2.1%}".format(i), end="\r")
    for c in cart:
        try:
            resp = estat.data(code, key = dict(c), params = {'startPeriod': str(StartPeriod), 'endPeriod': str(EndPeriod)})
        except Exception:
            print("FATAL ERROR: '{0}' not found in the Eurostat server.".format(code))
            return
        for s in resp.data.series:
            data.append(tuple(list(s.key._asdict().values()).__add__([float(o.value) for o in s.obs()])))
        if verbose:
            i += 1
            print("\rProgress: {:2.1%}".format(i / cart_len), end="\r")
    header = list(s.key._fields).__add__([int(o.dim) for o in s.obs()]) # only from the last data row
    data.insert(0,tuple(header))
    print("")

    return data



def get_sdmx_data_df(code, StartPeriod, EndPeriod, filter_pars, verbose=False):
    """
    Download an Eurostat dataset.
    Return it as a Pandas dataframe.
    """
    
    d = get_sdmx_data(code, StartPeriod, EndPeriod, filter_pars, verbose)
    
    return DataFrame(d[1:], columns = d[0])
