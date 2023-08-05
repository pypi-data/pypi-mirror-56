mobipy is a Python 3 library for analyzing user movement patterns from geolocated data.

mobipy brings together metrics and functions frequently used to calculate user mobility patterns. It was developed with a focus on usability and compatibility with multiple data sets, facilitating the tasks of research and data analysis.

Mobipy is tested against Python 3.6 and 3.7.

### Installation

Install using [pip](http://www.pip-installer.org/en/latest/) with:
```
pip install mobipy
```
Or, [download a wheel or source archive from PyPI](https://pypi.org/project/MobiPy).

### Available metrics

- Radius of gyration;
- Home detection;
- User displacement distance;
- Group by closeness;
- Activity centers;

### Using mobipy metrics

```
dataIdentifier = Identifier("latitude", "longitude", "local_time", "start_time", "end_time", "item_id")
path = "data.csv"
dataframe = pd.read_csv(path)
result = metrics.radius_of_gyration(dataframe=dataframe,  ##use keyword parameters
                                        				 dataIdentifier=dataIdentifier, 
                                        				 selector= Selector())
```