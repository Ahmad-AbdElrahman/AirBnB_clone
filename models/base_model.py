#!usr/bin/python3
import uuid
from datetime import datetime
from .engine import storage


class BaseModel:

    def __init__(self, *args, **kwargs) -> None:
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key == "created_at" or key == "updated_at":
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        data = self.__dict__
        data["__class__"] = self.__class__.__name__
        data['created_at'] = data['created_at'].isoformat()
        data['updated_at'] = data['updated_at'].isoformat()
        return data


# ========= TESTS ==========
if __name__ == "__main__":
    my_model = BaseModel()
    my_model.name = "My_First_Model"  # type: ignore
    my_model.my_number = 89  # type: ignore
    print(my_model.id)
    print(my_model)
    print(type(my_model.created_at))
    print("--")
    my_model_json = my_model.to_dict()
    print(my_model_json)
    print("JSON of my_model:")
    for key in my_model_json.keys():
        print(
            "\t{}: ({}) - {}".format(
                key, type(my_model_json[key]), my_model_json[key]
            )
        )

    print("--")
    my_new_model = BaseModel(**my_model_json)
    print(my_new_model.id)
    print(my_new_model)
    print(type(my_new_model.created_at))

    print("--")
    print(my_model is my_new_model)
