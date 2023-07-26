# Python attrs lib

***Python attrs is a Python library that simplifies the process of defining classes by generating boilerplate code.***

- Install

```bash
python -m pip install attrs
```

**Basic Code**

**Default**

모든 attribute에 대해서 class에 값을 넘겨주지 않을 경우, 초기 값을 위한 custom code 생성 가능

- Example Code

```python
from attrs import Factory
@define
class User:
 a: int = 42
 b: list = Factory(list)
 c: dict = field()
 
 @d.default
 def _any_name(self):
  return {}
```

** Factory

Class 객체마다 고유한 필드값을 가질 수 있도록 할당

기본 리스트 초기화로 선언할 경우, 다른 인스턴스와 필드값 공유가 되버림

```python
@define
class A:
    x = []
a = A()
b = A()
a.x.append(42)
b.x
>>> [42]
```

> *주의사항*
decorator 들은 attribute들이 set 될 때 수행되기 때문에, attr의 순서에 의존되어 있어 `self` Object가 완전하게 initialized 되지 않을 수 있다. `self` 를 되도록 적게 사용할것.!
>

- Official Docs

<https://www.attrs.org/en/stable/index.html>
