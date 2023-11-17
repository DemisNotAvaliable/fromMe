#   py 3.10
from copy import copy

def isparent(_object, _type):   return issubclass(type(_object), _type)

def pop_kwarg(key:str, kwargs:dict, default=None):
    try:    return kwargs.pop(key)
    except KeyError:    return default

def singleton(*args, **kwargs):
    def Singleton(cls):
        return cls(*args, **kwargs)
    return Singleton

"""------------------------------------------------ Dicts classes ---------------------------------------------------"""
#-------------------------------- Dict Object -------------------------------------------
class DictObject(dict):
    def __getattr__(self, item):
        return self[item]
    def __setattr__(self, key, value):
        self[key] = value

    def get_dict(self):
        return dict.copy(self)
#-------------------------------- Dict List ---------------------------------------------
class DictList(dict):
    """ a dict that work also like a list """
    def __getitem__(self, key):
        try:    return dict.__getitem__(self, key)
        except KeyError:
            if isinstance(key, int):
                for i, item in enumerate(self.values()):
                    if i == key:    return item
                raise IndexError(f' {self.__repr__()} has no index : {key}')
        raise KeyError(f' key : [ {key} ] not found in {self.__repr__()}')

    def __setitem__(self, key, value):
        if isinstance(key, int):
            for i, item in enumerate(self.keys()):
                if i == key:    dict.__setitem__(self, item, value)  ;   return
            raise IndexError(f' {self.__repr__()} has no index : {key}')
        else:   dict.__setitem__(self, key, value)

    def get_itemindex(self, key:str) -> int:
        for i, item in enumerate(self.keys()):
            if item == key:    return i
        raise KeyError(f'{self.__repr__()} : has no key : {key}')

    def get_itemkey(self, _index:int) -> str:
        for i, item in enumerate(self.keys()):
            if i == _index:    return item
        raise IndexError(f'{self.__repr__()} : has no index : {_index}')

if __name__ == '__main__' and 0:
    print('\n============== : class DictList : ===============\n')
    dictList = DictList()
    dictList['zero'] = 0
    dictList['uno'] = 1
    dictList['zero'] = 1
    dictList[0] = 2
    print(f"{dictList['zero'] = }")
    print(f"{dictList[0] = }")
    print(f"{id(dictList['zero']) == id(dictList[0]) = }")
    print(f"{dictList['zero'] is dictList[0] = }")
#-------------------------------- Default Dict ------------------------------------------
class DefaultDict(dict):
    """ a dict that always return the setted default option if key is missing """
    def __init__(self, get_default: callable, **kwargs):
        dict.__init__(self, **kwargs)
        self.__get_default__ = get_default

    def __missing__(self, key):
        item = self[key] = self.__get_default__()
        return item

    def change_default(self, getnew:callable): self.__get_default__ = getnew

if __name__ == '__main__' and 0:
    print('\n============== : class DefaultDict(dict) : ===============\n')
    defaultDict = DefaultDict(lambda: [], one=1)
    print(f'defaultDict = DefaultDict(lambda: [], one=1) : {defaultDict = }')
    defaultDict['pollo'] = 22
    print(f'defaultDict["pollo"] = 22 : {defaultDict["pollo"] = }')
    print(f'defaultDict["miss"] : {defaultDict["miss"] = }')
    defaultDict["nonpresent"].extend(range(10))
    print(f'defaultDict["nonpresent"].extend(range(10)) : {defaultDict["nonpresent"] = }')
#-------------------------------- ShadowDict --------------------------------------------
class ShadowDict(dict):
    class _Shadow_:
        exo = '$hadow'
        def __init__(self, value):
            self.value = value

    def shadow(self, name, value):
        sh = ShadowDict._Shadow_
        self[f'{sh.exo}{name}{sh.exo}'] = sh(value)

    def __iter__(self):
        siter = dict.__iter__(self)
        sh = ShadowDict._Shadow_.exo
        for key in siter:
            if sh in key:   continue
            yield key

    def keys(self):
        siter = dict.keys(self)
        sh = ShadowDict._Shadow_.exo
        for key in siter:
            if sh in key:   continue
            else:   yield key

    def values(self):
        for v in dict.values(self):
            if isinstance(v, ShadowDict._Shadow_):  continue
            else:   yield v

    def items(self):
        for k, val in dict.items(self):
            if isinstance(val, ShadowDict._Shadow_):  continue
            else:   yield k, val

    def __str__(self) -> str:  return f'{dict(self.items())}'
    def __repr__(self) -> str: return self.__str__()

    def __getitem__(self, key:str):
        try:    return dict.__getitem__(self, key)
        except KeyError as e:
            sh = ShadowDict._Shadow_.exo
            try:   return dict.__getitem__(self, f'{sh}{key}{sh}').value
            except KeyError:    raise e

    def __setitem__(self, key: str, value):
        sh = ShadowDict._Shadow_.exo
        try:    self[f'{sh}{key}{sh}'].value = value
        except KeyError:    dict.__setitem__(self, key, value)

if __name__ == '__main__' and 0:
    print('\n============== : class ShadowDict(dict) : ===============\n')
    shadowDict = ShadowDict(uno=1, due=2)
    print(f'shadowDict = ShadowDict(uno=1, due=2) : {shadowDict = }')
    shadowDict.shadow('tre', 3)
    print(f'shadowDict.shadow("tre", 3) : {shadowDict["tre"] = }')
    print(f'shadowDict : {shadowDict = }')
    shadowDict["tre"] = 'TRE'
    print(f'shadowDict["tre"] = "TRE : {shadowDict["tre"] = }')
    print(f'shadowDict.keys()   : {list(shadowDict.keys()) = }')
    print(f'shadowDict.values() : {list(shadowDict.values()) = }')
    print(f'shadowDict.items()  : {list(shadowDict.items()) = }')
#------------------------ Attributes_Counter --------------------------------------------
class Attributes_Counter:
    def __init__(self, _filter:object=None):
        self._keys = []
        self.__filter = filter(Attributes_Counter.__set_filter(_filter), self)

    def values(self):
        for key, attr in self:
            yield attr

    def items(self):
        for key, attr in self:
            yield key, attr

    def keys(self):
        for key in self._keys:
            yield str(key)

    @staticmethod
    def __set_filter(_filter:object):
        if filter is None:
            # noinspection PyUnusedLocal
            def none_filter(name_attribute:tuple):  return True
            return none_filter
        def filter_(name_attribute:tuple):
            if isparent(name_attribute[1], _filter):    return True
            else:   return False
        return filter_

    def _filtered(self, _filter=None):
        if _filter is None:   _filter = self.__filter
        else: _filter = filter(Attributes_Counter.__set_filter(_filter), self)
        return {key : it for key, it in _filter}

    def __setattr__(self, key, value):
        if key not in ['_keys', '__filter'] and key not in self._keys: self._keys.append(key)
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__getattribute__(item)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __iter__(self):
        for key in self._keys:
            yield key, self[key]

    def __contains__(self, item):
        return True if item in self._keys or item in self.values() else False
#-------------------------------- SingleActive ------------------------------------------
class SingleActive(DictList):
    """ subclass of Dictlist
        a dict that support also list interaction, provide some func for maintaine a single active element at once"""
    def __init__(self, cycle:bool=False, **kwargs):
        super().__init__(self, **kwargs)
        self._active_ : int = 0
        self.is_cycle : bool = cycle

    @property
    def active(self):
        try:    return self[self._active_]
        except IndexError:  return False

    @property
    def _active_(self):
        return self.__dict__.setdefault('__active__', 0)

    @_active_.setter
    def _active_(self, key:int|str):
        self.__dict__['__active__']: int = key if isinstance(key, int) else self.get_itemindex(key)

    def set_active(self, key:int|str):
        self._active_ = key

    def next(self):
        if len(self) - 1 > self._active_:   self._active_ += 1
        elif self.is_cycle: self._active_ = 0

    def back(self):
        if self._active_ > 0:   self._active_ -= 1
        elif self.is_cycle: self._active_ = len(self) - 1

if __name__ == '__main__' and 0:
    print('\n============== : class SingleActive(DictList) : ===============\n')
    singleActive = SingleActive(effe='f', gi='g', elle='elle')
    print(f'singleActive() : {singleActive.active = }')
    singleActive.set_active(1)
    print(f'singleActive.set_active(1) : {singleActive.active = }')
    singleActive.next()
    print(f'singleActive.next() : {singleActive.active = }')
    singleActive.back()
    print(f'singleActive.back() : {singleActive.active = }')
    singleActive.set_active("elle")
    print(f'singleActive.set_active("elle") : {singleActive.active = }')
    print(f'{singleActive.get_itemindex("gi") = }')
    print(f'{singleActive.get_itemkey(0) = }')
#----------------------------------- Slots ----------------------------------------------
class Slots(SingleActive):
    def __init__(self, defaultClass=None, cycle:bool=False):
        SingleActive.__init__(self, cycle)
        self.defaultClass = defaultClass

    def New(self, name:str|int, *params, **kwargs):
        try:    self[name]
        except KeyError:
            self[name] = obj = self.defaultClass(*params, **kwargs)
            return obj
        raise KeyError(f'[ {name} ] already exist! Slots.New(self, name, *args) must return a new instance of internal objects')

    def setdefault(self, name, *params, **kwargs):
        try:    obj = self[name]
        except KeyError:
            self[name] = obj = self.defaultClass(*params, **kwargs)
        return obj

    def update(self, kwargs:dict=None, **name_params:tuple):
        """ if the instances need 1 single parameter, insert it like this " istance_key = ( value , ) " """
        if kwargs is None: kwargs = {}
        for name, args in name_params.items():
            self.setdefault(name, *args, **kwargs)

"""------------------------------------------------ Lists Classes ---------------------------------------------------"""
#-------------------------------- List Dict ---------------------------------------------
class ListDict(list[dict[str, ...]]):
    """ a list containing dict
        support string research """
    def __getitem__(self, item):
        if isinstance(item, int):   return list.__getitem__(self, item)
        else:
            for dct in self:
                try:    return dct[item]
                except KeyError:    continue
        raise KeyError

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self[key] = value
            return self
        else:
            for dct in self:
                if key in dct.keys():
                    dct[key] = value
                    return self
            self.append({key:value})
            return self

    def update(self, **kwargs):
        for key, item in kwargs:
            self[key] = item
        return self

    def keys(self) -> str|int:
        for dct in self:
            for key in dct.keys():
                yield key
                break

    def values(self):
        for dct in self:
            for value in dct.values():  yield value
#------------------------------- Events List --------------------------------------------
class EventsList(list):
    def __init__(self, *args):
        list.__init__(self, *args)
        self.events = []

    def pushEvents(self, *events:callable):
        """ event must have an argument """
        self.events.extend(events)

    def loop(self):
        return self.checkevents(lambda: self, *self.events)

    def checkevents(self, funciter:callable, *events):
        for item in funciter():
            for event in events:   event(item)
            yield item
        self.events.clear()

    def __call__(self, *events):
        for item in self.checkevents(lambda: self, *events):    yield item

"""------------------------------------------------ Miscellaneous ---------------------------------------------------"""
#-------------------------------- Little Box --------------------------------------------
class LittleBox:
    """ an item with just a name and a value """
    def __init__(self, name:str|int, value):
        self.name, self.value = name, value

    def __contains__(self, item):
        return item in (self.name, self.value)
#----------------------------- Contenitor Property --------------------------------------
# dict type
class Class_dict(type):
    _dict_ = {}

    def __getattr__(cls, item):
        try:    return getattr(cls._dict_, item)
        except AttributeError:
            return cls._dict_[item]

    def __getitem__(cls, item):
        return cls._dict_[item]

    def __iter__(cls):
        for key, value in cls._dict_.items():
            yield key, value

    def __contains__(mcs, item):
        return mcs._dict_.__contains__(item)

    def __setitem__(cls, key, value):
        cls._dict_[key] = value

    def __len__(cls):
        return len(cls._dict_)

    @property
    def all(cls):
        return type(cls)._dict_.items()
# list type
class Class_list(type):
    _list_ = []

    @classmethod
    def __getattr__(mcs, item):
        return mcs._list_.__getattribute__(item)

    @classmethod
    def __getitem__(mcs, _index:int):
        return mcs._list_[_index]

    @classmethod
    def __iter__(mcs):
        for value in mcs._list_:    yield value

    @classmethod
    def __contains__(mcs, item):
        return mcs._list_.__contains__(item)

    @classmethod
    def __setitem__(mcs, key, value):
        mcs._list_[key] = value

    @classmethod
    def __len__(mcs):
        return len(mcs._list_)

    @property
    def all(self):
        return type(self)._list_
#------------------------------- Class Object -------------------------------------------
class Class_object(type):
    faked : object = None
    @classmethod
    def __getattr__(mcs, item):
        return mcs.faked.__getattribute__(item)

    @classmethod
    def set_faked(mcs, obj:object):
        mcs.faked = obj
#--------------------------- Enumerated id instances ------------------------------------
class EnumeratedID:
    _istances_count_ = 0
    def __init__(self):
        self._id = self.get_id()

    def get_id(self):
        try:    return self._id
        except AttributeError:
            self.__class__._istances_count_ += 1
        return self.__class__._istances_count_

"""--------------------------------------------- Single Instance Classes --------------------------------------------"""
#--------------------------- Single Instance Metaclass ----------------------------------
class SingleIstanceMeta(type):
    # noinspection PyUnresolvedReferences
    def __call__(cls, *args, **kwargs):
        try:    return cls.__instance
        except AttributeError:
            cls.__instance = cls.build_instance(*args, **kwargs)
            return cls.__instance

    def get_instance(cls):  return cls.__instance

    def build_instance(cls, *args, **kwargs):
        return type.__call__(cls, *args, **kwargs)

    def is_alive(cls):
        return hasattr(cls, '__instance')

#-------------------------- Single Instance Constructor ---------------------------------
class OnCallConstructor:
    def __init__(self, cls):
        self.type = cls

    def get_instance(self):  return self.__instance

    def __call__(self, *args, **kwargs):
        try:    # noinspection PyUnresolvedReferences
            return self.__instance
        except AttributeError:
            self.__instance = self.type(*args, **kwargs)
            return self.__instance
