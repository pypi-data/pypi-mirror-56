# Eurostat Python Package 

Tools to read data from Eurostat website.

# Features

* Read Eurostat data and metadata as list of tuples.
* MIT license.

# Documentation


## Getting started:

Requires Python 3.6+

```bash
pip install eurostat
```


## Read the table of contents of the main database:

```python
eurostat.get_toc()
```

Read the table of contents and return a list of tuples. The first element of the list contains the header line. Dates are represented as strings.

Example:

```python
>>> import eurostat
>>> toc = eurostat.get_toc()
>>> toc[0]
('title', 'code', 'type', 'last update of data', 'last table structure change', 'data start', 'data end')
>>> toc[10:13]
[('Industry - quarterly data', 'ei_bsin_q_r2', 'dataset', '30.10.2019', '30.10.2019', '1980Q1', '2019Q4'),
 ('Construction - monthly data', 'ei_bsbu_m_r2', 'dataset', '30.10.2019', '30.10.2019', '1980M01', '2019M10'),
 ('Construction - quarterly data', 'ei_bsbu_q_r2', 'dataset', '30.10.2019', '30.10.2019', '1981Q1', '2019Q4')]
```


## Read a dataset from the main database:

### As a list of tuples:

```python
eurostat.get_data(code, flags=False)
```

Read a dataset from the main database (available from the [bulk download facility]) and returns it as a list of tuples. The first element of the list ("the first row") is the data header.
Pay attention: the data format changes if flags is True or not.

Example:

```python
>>> import eurostat
>>> data = eurostat.get_data('demo_r_d2jan')
>>> data
[('unit', 'sex', 'age', 'geo\\time', 2018, 2017, 2016, 2015, 2014, ...),
 ('NR', 'F', 'TOTAL', 'AL', 1431715.0, None, 1417141.0, 1424597.0, 1430827.0, ...),
  ...]
>>> data = eurostat.get_data('demo_r_d2jan', True)
>>> data
[('unit', 'sex', 'age', 'geo\\time', 2018, 2017, 2016, 2015, 2014, ...),
 ('NR', 'F', 'TOTAL', 'AL', '1431715 ', ': ', '1417141 ', '1424597 ', '1430827 ', ...),
  ...]
```

### As a pandas dataframe:

```python
eurostat.get_data_df(code, flags=False)
```

Read a dataset from the main database (available from the [bulk download facility]) and returns it as a pandas dataframe.
Pay attention: the data format changes if flags is True or not.

Example:

```python
>>> import eurostat
>>> df = eurostat.get_data_df('demo_r_d2jan')
>>> df
       unit   sex     age geo\time  ...     1993     1992  1991  1990
0        NR     F   TOTAL       AL  ...      NaN      NaN   NaN   NaN
1        NR     F   TOTAL      AL0  ...      NaN      NaN   NaN   NaN
2        NR     F   TOTAL     AL01  ...      NaN      NaN   NaN   NaN
3        NR     F   TOTAL     AL02  ...      NaN      NaN   NaN   NaN
4        NR     F   TOTAL     AL03  ...      NaN      NaN   NaN   NaN
    ...   ...     ...      ...  ...      ...      ...   ...   ...
168608   NR     T  Y_OPEN     UKM8  ...      NaN      NaN   NaN   NaN
168609   NR     T  Y_OPEN     UKM9  ...      NaN      NaN   NaN   NaN
168610   NR     T  Y_OPEN      UKN  ...  17934.0  17566.0   NaN   NaN
168611   NR     T  Y_OPEN     UKN0  ...  17934.0  17566.0   NaN   NaN
168612       None    None     None  ...      NaN      NaN   NaN   NaN
>>> df = eurostat.get_data_df('demo_r_d2jan', True)
>>> df
       unit   sex     age geo\time  ...    1993    1992  1991  1990
0        NR     F   TOTAL       AL  ...      :       :     :     : 
1        NR     F   TOTAL      AL0  ...      :       :     :     : 
2        NR     F   TOTAL     AL01  ...      :       :     :     : 
3        NR     F   TOTAL     AL02  ...      :       :     :     : 
4        NR     F   TOTAL     AL03  ...      :       :     :     : 
    ...   ...     ...      ...  ...     ...     ...   ...   ...
168608   NR     T  Y_OPEN     UKM8  ...      :       :     :     : 
168609   NR     T  Y_OPEN     UKM9  ...      :       :     :     : 
168610   NR     T  Y_OPEN      UKN  ...  17934   17566     :     : 
168611   NR     T  Y_OPEN     UKN0  ...  17934   17566     :     : 
168612       None    None     None  ...    None    None  None  None
```


## Get an Eurostat dictionary:

```python
eurostat.get_dic(code)
```

Read the metadata related to a particular code. Return a list of tuples, where the first element of each tuple is the code value and the second one is its description.

Example:

```python
>>> import eurostat
>>> dic = eurostat.get_dic('sex')
>>> dic
[('T', 'Total'),
 ('M', 'Males'),
 ('F', 'Females'),
 ('DIFF', 'Absolute difference between males and females'),
 ('NAP', 'Not applicable'),
 ('NRP', 'No response'),
 ('UNK', 'Unknown')]
```


## Read the Eurostat dimensions of a dataset via SDMX service:

```python
eurostat.get_sdmx_dims(code)
```

Read the dimension names of a dataset that is provided via SDMX service. Require the dataset code and return a list.
Example:

```python
>>> import eurostat
>>> dims = eurostat.get_sdmx_dims('DS-066341')
>>> dims
['DECL', 'FREQ', 'INDICATORS', 'PERIOD', 'PRCCODE']
```


## Read an Eurostat dictionary for a given SDMX dimension:

```python
eurostat.get_sdmx_dic(code, dim)
```

Read the Eurostat dimension values with their meaning for a dataset provided via SDMX service. Return them as a dictionary.

Example:
```python
>>> import eurostat
>>> dic = get_sdmx_dic('DS-066341', 'FREQ')
>>> dic
{'A': 'Annual',
 'D': 'Daily',
 'H': 'Half-year',
 'M': 'Monthly',
 'Q': 'Quarterly',
 'S': 'Semi-annual',
 'W': 'Weekly'}
```


## Read a dataset from the SDMX service:

### As a list of tuples:

```python
eurostat.get_sdmx_data(code, StartPeriod, EndPeriod, filter_pars, verbose=False)
```

Read a dataset from SDMX service. Return a list of tuples. The first tuple (row) contains the header.
This service is slow, so you will better select the subset you need and set the filter parameters along the available dimensions by setting filter_pars (a dictionary where keys are dimensions names, values are lists).
It allows to download some datasets that are not available from the main database.
To see a rough progress indication, set verbose = True.

```python
>>> import eurostat
>>> StartPeriod = 2007
>>> EndPeriod = 2008
>>> filter_pars = {'FREQ': ['A',], 'PRCCODE': ['08111250','08111150']}
>>> data = eurostat.get_sdmx_data('DS-066341', StartPeriod, EndPeriod, filter_pars, verbose=True)
Progress: 0.0%
Progress:50.0%
Progress:100.0%
>>> data
[('INDICATORS', 'DECL', 'PRCCODE', 'FREQ', 2007, 2008),
 ('EXPQNT', '001', '08111250', 'A', 10219200.0, 16082600.0),
 ('EXPVAL', '001', '08111250', 'A', 1697160.0, 1875920.0),
 ...]
```

### As a pandas dataframe:

```python
eurostat.get_sdmx_data(code, StartPeriod, EndPeriod, filter_pars, verbose=False)
```

Read a dataset from SDMX service. Return a pandas dataframe.
This service is slow, so you will better select the subset you need and set the filter parameters along the available dimensions by setting filter_pars (a dictionary where keys are dimensions names, values are lists).
It allows to download some datasets that are not available from the main database.
To see a rough progress indication, set verbose = True.

```python
>>> import eurostat
>>> StartPeriod = 2007
>>> EndPeriod = 2008
>>> filter_pars = {'FREQ': ['A',], 'PRCCODE': ['08111250','08111150']}
>>> df = get_sdmx_data_df(code, StartPeriod, EndPeriod, filter_pars, verbose=True)
Progress: 0.0%
Progress:50.0%
Progress:100.0%
>>> df
    INDICATORS DECL   PRCCODE FREQ        2007        2008
0       EXPQNT  001  08111250    A  10219200.0  16082600.0
1       EXPVAL  001  08111250    A   1697160.0   1875920.0
2       IMPQNT  001  08111250    A   7526000.0   4272200.0
3       IMPVAL  001  08111250    A   1802940.0   1208030.0
4     PQNTBASE  001  08111250    A         0.0         0.0
..         ...  ...       ...  ...         ...         ...
875    PRODQNT  600  08111150    A         0.0         0.0
876    PRODVAL  600  08111150    A         0.0         0.0
877   PVALBASE  600  08111150    A         0.0         0.0
878   PVALFLAG  600  08111150    A         NaN         NaN
879    QNTUNIT  600  08111150    A         NaN         NaN
```


## Bug reports and feature requests:

Please [open an issue][] or send a message to noemi.cazzaniga [[at]] polimi.it .


## Disclaimer:

Download and usage of Eurostat data is subject to Eurostat's general copyright notice and licence policy (see [Policies][pol]). Please also be aware of the European Commission's [general conditions][cond].


## Data sources:

* Eurostat database: [online catalog][onlinecat] and [bulk download facility][bulkdown].
* Eurostat nomenclatures: [RAMON][ram] metadata.
* Eurostat Interactive Data Explorer: [Data Explorer][expl].
* Eurostat Interactive Tool for Comext Data: [Easy Comext][comext].


## References:

* R package [eurostat][es]: R Tools for Eurostat Open Data.
* Python package [pandaSDMX] [pandasdmx]: Statistical Data and Metadata eXchange.
* Python package [pandas][pd]: Python Data Analysis Library.

[pol]: https://ec.europa.eu/eurostat/web/main/about/our-partners/copyright
[cond]: http://ec.europa.eu/geninfo/legal_notices_en.htm
[onlinecat]: https://ec.europa.eu/eurostat/data/database
[bulkdown]: https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing
[ram]: https://ec.europa.eu/eurostat/ramon/nomenclatures/index.cfm?TargetUrl=LST_NOM&StrGroupCode=SCL&StrLanguageCode=EN
[expl]: http://appsso.eurostat.ec.europa.eu/nui/
[comext]: http://epp.eurostat.ec.europa.eu/newxtweb/
[pandasdmx]: https://pandasdmx.readthedocs.io/en/stable/
[pd]: https://pandas.pydata.org/
[es]: http://ropengov.github.io/eurostat/
