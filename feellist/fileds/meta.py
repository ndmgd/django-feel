from django.db.models.base import ModelBase


class FieldComposeMeta(ModelBase):
    """自定义元类：兼容函数/字典两种赋值方式"""

    def __new__(cls, name, bases, attrs):
        compose_fields = {}
        new_attrs = {}

        for attr_name, attr_value in attrs.items():
            if attr_name.startswith("_compose_"):
                # 场景1：如果是可调用对象（函数），执行后合并字段
                if callable(attr_value):
                    compose_fields.update(attr_value())
                # 场景2：如果是字典（已执行的字段函数），直接合并
                elif isinstance(attr_value, dict):
                    compose_fields.update(attr_value)
            else:
                new_attrs[attr_name] = attr_value

        # 合并所有组合字段到模型属性
        new_attrs.update(compose_fields)

        # 创建模型类
        return super().__new__(cls, name, bases, new_attrs)
