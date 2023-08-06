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
        print("{0} not found in the Eurostat server".format(code))
        return
    raw_part_data[2] = sub(r"\t", ",", raw_part_data[2])
    n_text_fields = raw_part_data[0].count(",") + 1
    if flags == True:
        raw_data = raw_part_data[0] + ',' + raw_part_data[2]
        j = 0
        data = []
        for l in raw_data.split('\n'):
            l = l.split(',')
            len_l = len(l)
            if j == 0:
                l_tmp = zip(map((lambda i: i.strip() + "_value"), l[n_text_fields:]),map((lambda i: i.strip() + "_flag"), l[n_text_fields:]))
                l2 = l[:n_text_fields].__add__([x for pair in l_tmp for x in pair])
                j += 1
            else:
                for i in range(n_text_fields, len_l):
                    k = (i - n_text_fields) * 2 + n_text_fields
                    l2[:n_text_fields] = l[:n_text_fields]
                    try:
                        l2[k:k+2] = l[i].split(' ')
                        try:
                            l2[k] = float(l2[k])
                        except:
                            l2[k:k+2] = [None, l2[k]]
                    except AttributeError:
                        l2[k:k+2] = [None, '']
            data.append(tuple(l2))
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

    data.pop()
    return data



def get_data_df(code, flags=False):
    """
    Download an Eurostat dataset.
    Return it as a Pandas dataframe.
    """
    
    d = get_data(code, flags)
    
    if d != None:
        return DataFrame(d[1:], columns = d[0])
    else:
        return



def get_dic(code):
    """
    Download an Eurostat dictionary.
    Return it as a dictionary.
    """

    strerr = 'File {0}'.format(code) + '.dic does not exist or is not readable on the server'
    tmp = urlopen("https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=dic%2Fen%2F" + code + ".dic")
    dic = []
    for i in tmp.readlines():
        d = i.decode('utf-8').rstrip('\r\n').split('\t')
        if strerr in d:
            print(strerr)
            return
        else:
            dic.append(tuple(d))

    return dict(dic)



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



def get_toc_df():
    """
    Download the Eurostat table of contents.
    Return it as a pandas dataframe.
    """
    
    t = get_toc()

    return DataFrame(t[1:], columns = t[0])




def subset_toc_df(toc_df, keyword):
    """
    Extract from the Eurostat table of contents where the title contains a given keyword.
    Return a pandas dataframe.
    """

    return toc_df[toc_df['title'].str.contains(keyword, case=False)]




def get_sdmx_dims(code):
    """
    Download the Eurostat dimension names of a dataset available via SDMX service.
    Return them as a list.
    """
    
    estat = Request('ESTAT', timeout = 100.)
    try:
        structure = estat.datastructure('DSD_'+code)
    except Exception:
        print("{0} not found in the Eurostat server".format(code))
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
        print("{0} not found in the Eurostat server".format(code))
        return
    try:
        idx = structure.write().codelist.loc[dim].reset_index()['index'][1:]
        name = structure.write().codelist.loc[dim].reset_index()['name'][1:]
    except Exception:
        print("Dimension '{0}' not found for the dataset '{1}'".format(dim, code))
        return
    vals = dict(zip(idx, name))
    
    return vals




def get_sdmx_data(code, StartPeriod, EndPeriod, filter_pars, flags=False, verbose=True):
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
        print("\rProgress: {:3.1%}".format(i), end="\r")
    if flags:
        for c in cart:
            try:
                resp = estat.data(code, key = dict(c), params = {'startPeriod': str(StartPeriod), 'endPeriod': str(EndPeriod)})
            except ValueError as e:
                print("\r" + str(e))
                return
            except Exception:
                print("\r{0} not found in the Eurostat server".format(code))
                return
            for s in resp.data.series:
                data.append(tuple(list(s.key._asdict().values()).__add__([x for pair in [(float(o.value), o.attrib.OBS_STATUS if (len(o.attrib) > 0 and o.attrib._fields[0] == 'OBS_STATUS') else '') for o in s.obs()] for x in pair])))
            if verbose:
                i += 1
                print("\rProgress: {:3.1%}".format(i / cart_len), end="\r")
        header = list(s.key._fields).__add__([x for pair in [(int(o.dim), o.dim + '_OBS_STATUS') for o in s.obs()] for x in pair]) # only from the last data row
    else:
        for c in cart:
            try:
                resp = estat.data(code, key = dict(c), params = {'startPeriod': str(StartPeriod), 'endPeriod': str(EndPeriod)})
            except ValueError as e:
                print("\r" + str(e))
                return
            except Exception:
                print("\r{0} not found in the Eurostat server".format(code))
                return
            for s in resp.data.series:
                data.append(tuple(list(s.key._asdict().values()).__add__([float(o.value) for o in s.obs()])))
            if verbose:
                i += 1
                print("\rProgress: {:3.1%}".format(i / cart_len), end="\r")
        header = list(s.key._fields).__add__([int(o.dim) for o in s.obs()]) # only from the last data row        
    data.insert(0,tuple(header))
    print("")

    return data



def get_sdmx_data_df(code, StartPeriod, EndPeriod, filter_pars, flags=True, verbose=True):
    """
    Download an Eurostat dataset.
    Return it as a Pandas dataframe.
    """
    
    d = get_sdmx_data(code, StartPeriod, EndPeriod, filter_pars, flags, verbose)
    
    if d != None:
        return DataFrame(d[1:], columns = d[0])
    else:
        return
