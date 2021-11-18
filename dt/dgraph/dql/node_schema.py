from typing import List, Set, Optional

from dt.dgraph.dql.i_schema_item import ISchemaItem
from dt.dgraph.dql.type_attribute import TypeAttribute
from dt.dgraph.error.schema_duplicate_error import SchemaDuplicateError


class NodeSchema(ISchemaItem):
    '''Defines a schema for a single DGraph node type'''

    node_type: str
    _attribute_list: List[TypeAttribute]
    _attribute_name_set: Set[str]

    def __init__(self, node_type: str, attr_list: Optional[List[TypeAttribute]] = None):
        self.node_type = node_type
        self._attribute_list = []
        self._attribute_name_set = set()
        if attr_list is not None:
            for attribute in attr_list:
                self.add_attribute(attribute)

    def add_attribute(self, attribute: TypeAttribute) -> TypeAttribute:
        if attribute.attr_name in self._attribute_name_set:
            message = f"Attribute with name: {attribute.attr_name} already " + \
                f"exists in schema for node_type: {self.node_type}"
            raise SchemaDuplicateError(message)
        self._attribute_name_set.add(attribute.attr_name)
        self._attribute_list.append(attribute)
        return attribute

    def get_attributes(self) -> List[TypeAttribute]:
        return self._attribute_list

    def to_schema_statement(self) -> str:
        type_statement = f"type {self.node_type}" + " {\n"
        attribute_name_list_str = "\n".join(self._attribute_name_set)
        schema_statement = f"{type_statement}{attribute_name_list_str}" + "\n}"
        return schema_statement