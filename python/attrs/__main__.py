########################################
# Dataclass vs attrs                   #
########################################
#### SLOTS 사용 
# @dataclass -> no __slots__
# @attrs -> use __slots__ 
#        -> field 값 고정되어 있음
# -> kw_only 명시할 경우 동적으로 필드값 할당을 막아줌
# -> Version에 독립적
#

import inspect
from typing import Any

# validator, setter 설정 가능 
from attrs import validators, setters 
from attrs import define, field

# kw_only -> init 시, 키워드 명시 필요
@define
class User:
    id : int = field(validator=validators.instance_of(int),
                     on_setattr=setters.frozen)
    name: str = field(converter=str)
    email: str = field(repr=True)

    # 초기 default 함수 정의 가능
    @email.default
    def _email_default(self):
        return f"{self.name}@coding.io"



print(inspect.getsource(User.__init__))
var = User(id=1,name="lee")
User.nmae = "Kim"
print(var)

