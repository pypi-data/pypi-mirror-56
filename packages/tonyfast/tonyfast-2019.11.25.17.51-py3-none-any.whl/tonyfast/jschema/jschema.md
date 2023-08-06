Semantic JsonSchema types in python.


```python
    import jsonschema, requests, requests_cache, altair.vega.v4, json
    import dataclasses, typing, pandas, toolz.curried as toolz, anyconfig
    requests_cache.install_cache('schemas.sqlite')
```


```python
    class Schema(__import__('munch').Munch):
        __validator__ = None
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs), jsonschema.validate(self, __import__('jsonschema').Draft7Validator.META_SCHEMA)
            self.__validator__ = __import__('jsonschema').Draft7Validator(self, format_checker=__import__('jsonschema').draft7_format_checker)
        def validate(self, object): return self.__validator__.validate(object)
        def valid(cls, object) -> bool:
            try: cls.validate(object); return True
            except BaseException: return False
```


```python
    class Validator:
        def __init_subclass__(cls, **schema):
            for object in reversed(cls.__mro__): schema = {**(getattr(object, '__schema__', {}) or {}), **schema}
            cls.__schema__ = Schema(schema, title=cls.__name__, **(dict(description=cls.__doc__) if cls.__doc__ else {})) # Schema will validate the schema
            
    class MetaType(Validator, __import__('abc').ABCMeta):             
        def new(cls, object=None, **schema):  
            schema = {**cls.__schema__, **(object if isinstance(object, dict) else {}), **schema}
            return type(schema.get('title', __import__('json').dumps(schema)), (cls,), {}, **schema)
        def __instancecheck__(cls, object): return cls.__schema__.valid(object)

```


```python
    class Type(Validator, metaclass=MetaType): 
        __schema__ = None
        def __new__(cls, object=None, *args, **kwargs):
            if object is None: object = __import__('copy').copy(cls.__schema__.get('default', super().__new__(cls)))
            if isinstance(object, dict): object.update(kwargs); kwargs = {}
            cls.__schema__.validate(object)
            self = super().__new__(cls, object, *args, **kwargs); self.__init__(object, *args, **kwargs)
            return self
        
        @classmethod
        def discover(x, object=None, **schema):
            for cls in x.__subclasses__():
                try: object = cls(object); break
                except BaseException as e: ...
            else: return object
            return cls.discover(object)
        
        def _repr_mimebundle_(x, include=None, exclude=None, **metadata): 
            for k, v in globals().items():
                if k[0].isalpha() and v is getattr(x, 'object', x): metadata['@id'] = k; break
            metadata.update(x.__schema__, examples=[x])
            return {}, metadata

    
    class Null(Type, type='null'): 
        def __new__(cls, object=None, *args, **kwargs): return cls.__schema__.validate(object)
    class Integer(Type, int, type='integer'): ...
    class Number(Type, float, type='number'): ...
    class List(Type, list, type='array'): 
        
        def __new__(cls, object=None, *args, **kwargs): 
            if isinstance(object, tuple): object = list(object)
            return super().__new__(cls, object, *args, **kwargs)        
    class Dict(Type, dict): 
        def __init_subclass__(cls, **schema): 
            if schema: ...
            else: schema = dict(schema, type='object', properties={key: value.__schema__ for key, value in getattr(cls, '__annotations__', {}).items() if hasattr(value, '__schema__')}, default={})
            cls.__schema__ = Schema(**schema)

    class String(Type, str, type='string'): ...
    class Uri(String, format='uri'): ...
    class Date(String, format='date'): ...
    class Datetime(String, format='date-time'): ...
    class Time(String, format='time'): ...
    class Email(String, format='email'): ...
    class JsonPointer(String, format='json-pointer'): ...
    class File(String): 
        """`File` is only valid if it exists on disk."""
        def __init__(self, object):
            if __import__('pathlib').Path(object).exists(): return 
            raise ValueError(F"{object} is not a file.")
    @toolz.do(toolz.partial(setattr, File, 'load'))
    def load(x): return Type.discover(__import__('anyconfig').load(x))
    @toolz.do(toolz.partial(setattr, File, 'json'))
    def file_json(x): return Type.discover(__import__('json').loads(__import__('pathlib').Path(x).read_text()))
    @toolz.do(toolz.partial(setattr, Uri, 'json'))
    def json(x): return Type.discover(__import__('requests').get(x).json())
    @toolz.do(toolz.partial(setattr, Uri, 'text'))
    def text(x): return Type.discover(__import__('requests').get(x).text)
    
    class UserObject(Type, str):
        """Use abc registration to connect to python types."""
        object: None        
        def __post_init__(x): 
            x.object = getattr(x, 'object', x.object)
            assert issubclass(
                type(x.object), tuple(UserObject.__subclasses__()) 
                if type(x)==UserObject else type(x))
        def _repr_mimebundle_(x, include=None, exclude=None, **metadata): return {}, metadata
    dataclasses.dataclass(UserObject)        
    
    class Pandas(UserObject): 
        def _repr_mimebundle_(x, include=None, exclude=None):
            data, metadata = super()._repr_mimebundle_(include, exclude)
            return data, {**metadata, 'allOf':[
                TableSchema(__import__('json').loads(x.object.to_json(orient='table'))['schema']),
                List.new(minItems=len(x.object), maxItems=len(x.object)).__schema__,]}
        
    Pandas.register(pandas.DataFrame), Pandas.register(pandas.Series)
        

```




    (pandas.core.frame.DataFrame, pandas.core.series.Series)




```python
    class ListofUri(List, items=Uri.__schema__, minItems=1): 
        def text(x): return [Uri.text(x) for x in x]
        def json(x): return [Uri.json(x) for x in x]
```


```python
    class NbFormat(Dict, **__import__('nbformat').validator._get_schema_json(__import__('nbformat').v4)): ...
    class JsonPatch(List, **requests.get("http://json.schemastore.org/json-patch").json()):
        def __call__(self, object): return Type.discover(__import__('jsonpatch').apply_patch(object, self))
    class TableSchema(Dict, **requests.get("https://frictionlessdata.io/schemas/table-schema.json").json()): ...
    class GeoJson(Dict, **requests.get("http://json.schemastore.org/geojson").json()): ...
```


```python
    class DictofDict(Dict, additionalProperties=Dict.__schema__): ...
    class DictofList(Dict, additionalProperties=List.__schema__): ...
    class ListofList(List, additionalProperties=List.__schema__): ...
    class ListofDict(List, additionalProperties=Dict.__schema__): ...
```


```python
    class Jpeg(String, pattern='[.jpeg|.jpg]$', contentMediaType='image/jpeg'): ...
    class Png(String, pattern='.png$', contentMediaType='image/png'): ...
```

# tests


```python
    class Test(__import__('unittest').TestCase):
        def test_instance(x):
            assert isinstance('http://xx', Uri)
            assert not isinstance('xx', Date)
            assert isinstance('2019-01-01', Date)
        def test_schema(x):
            schema = Schema({'type': 'object'})
            assert schema.valid({})
            assert not schema.valid(1)
            
        def test_discovery(x):
            assert isinstance(Type.discover(10), Integer)
            assert isinstance(Type.discover(10.1), Number)
            assert isinstance(Type.discover('http://thing'), Uri)
            assert isinstance(Type.discover('jschema.ipynb'), File)
            assert isinstance(Type.discover('2019-08-01'), Date)
            assert isinstance(Type.discover({}), Dict)
            assert isinstance(Type.discover([]), List)
                        
        def test_import(x):
            with __import__('importnb').Notebook(): import jschema
            assert jschema.__file__.endswith('.ipynb')
            
        def test_custom_dict(x):
            class Custom(Dict): a: Integer
            with pytest.raises(jsonschema.ValidationError): Custom(a='asdf')
            assert Custom(a=10)
            
        def test_new_api(x):
            type = String.new(pattern='^x')
            with pytest.raises(jsonschema.ValidationError): type('asdf')            
            assert type('xxxx')
            
        def test_pandas(x):
            assert Pandas(object=pandas.util.testing.makeDataFrame())
            assert isinstance(Type.discover(pandas.util.testing.makeDataFrame()), Pandas)
    class TestSchemaDiscovery(__import__('unittest').TestCase):
        def test_geojson(x):
            assert not isinstance({'xx': 2}, GeoJson)
            assert isinstance(File('geojson_sample.geojson').json(), GeoJson)
            
        def test_table_schema(x):
            assert not isinstance({'a': 10}, TableSchema)
            assert isinstance(__import__('json').loads(
                __import__('pandas').util.testing.makeDataFrame().to_json(orient='table'))['schema'], TableSchema)
        
        def test_nb(x):
            assert not isinstance({'a': 10}, NbFormat)
            assert isinstance(File('jschema.ipynb').json(), NbFormat)

```


```python
    def load_tests(loader, tests, ignore): tests.addTests(doctest.DocTestSuite(importlib.import_module(__name__), optionflags=doctest.ELLIPSIS)); return tests
    if __name__ == '__main__': 
        import unittest, pytest, jsonschema, importlib, doctest
        unittest.main(argv=' ', exit=False, verbosity=1)
```

    ../Users/tonyfast/anaconda3/lib/python3.7/site-packages/IPython/core/inputsplitter.py:22: DeprecationWarning: IPython.core.inputsplitter is deprecated since IPython 7 in favor of `IPython.core.inputtransformer2`
      DeprecationWarning)
    ........
    ----------------------------------------------------------------------
    Ran 10 tests in 0.212s
    
    OK


http://schemastore.org/json/


```python
    if __name__ == '__main__': 
        !jupyter nbconvert --to script jschema.ipynb
        !black jschema.py
        !pyreverse jschema -osvg -pjschema
        !rm jschema.py
        display(__import__('IPython').display.SVG('classes_jschema.svg'))
```

    [NbConvertApp] Converting notebook jschema.ipynb to script
    [NbConvertApp] Writing 9213 bytes to jschema.py
    [1mreformatted jschema.py[0m
    [1mAll done! ✨ 🍰 ✨[0m
    [1m1 file reformatted[0m.[0m

