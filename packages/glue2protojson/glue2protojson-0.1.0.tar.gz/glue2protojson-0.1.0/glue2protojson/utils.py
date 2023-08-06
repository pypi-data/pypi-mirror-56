import logging
import boto3
from typing import List
from glue2protojson.gluetypes import GlueColumn, GlueColumnStruct, GlueColumnArray, GlueColumnBoolean, GlueColumnString


logger = logging.getLogger(__name__)


def get_schema_from_glue(database: str, table: str) -> List:
    glue = boto3.client('glue')
    response = glue.get_table(DatabaseName=database, Name=table)
    return response['Table']['StorageDescriptor']['Columns']


def get_meta_type(glue_type: str) -> str:
    """
    Detect if the glue type is simple or is an struct or array
    :param glue_type: Type of glue column output definition
    :return: return string meta type
    """
    logger.debug(glue_type)
    try:
        # Detect things like 'array<...' or 'struct<...'
        result = glue_type[:glue_type.index('<')]
        logger.debug(result)
        return result
    except ValueError:
        return glue_type


def remove_meta_type(glue_type: str) -> str:
    """
    Remove wrapping meta type. Example: array<string> -> string
    :param glue_type: Glue Type definition
    :return: unwrapped type definition
    """
    logger.debug(glue_type)
    result = glue_type[glue_type.index('<')+1:-1]
    logger.debug(result)
    return result


def snake_to_pascal(snake_name: str) -> str:
    """
    Convert an snake_case string to PascalCase
    :param snake_name: snake case text
    :return: pascal case conversion
    """
    return ''.join([w.capitalize() for w in snake_name.lower().split('_')])


def get_struct_mapping(glue_struct: str) -> dict:
    """
    Convert the content of struct<xx> from Glue to JSON with GlueColumns
    This will be the attribute content of a GlueColumnStruct
    It is a recursive function, each level just parse one field
    :param glue_struct: xx in struct<xx>, with the meta type removed
    :return: dict
    """
    logger.debug(glue_struct)
    result = {}

    first_colon = glue_struct.index(':')
    map_key = glue_struct[0:first_colon]
    logger.debug(f'key -> {map_key}')

    opens = 0
    comma_pos = 0
    for k2, c2 in enumerate(glue_struct[first_colon+1:]):
        if c2 == '<':
            opens += 1
        elif c2 == '>':
            opens -= 1
        elif c2 == ',' and opens == 0:
            comma_pos = first_colon + 1 + k2
            map_value = get_column(glue_type=glue_struct[first_colon + 1:comma_pos], glue_name=map_key)
            logger.debug(f'value -> {map_value}')
            result[map_key] = map_value
            break

    # Is last field
    if comma_pos == 0:
        map_value = get_column(glue_type=glue_struct[first_colon + 1:], glue_name=map_key)
        logger.debug(f'value -> {map_value}')
        result[map_key] = map_value
    # Continue recursively
    else:
        result.update(get_struct_mapping(glue_struct=glue_struct[comma_pos + 1:]))

    return result


def get_column(glue_type: str, glue_name: str) -> GlueColumn:
    """
    Parse a boto3 glue column data type output to GlueColumn object
    :param glue_type: Type field of a Glue column definition
    :param glue_name: Name field of the Glue column definition
    :return: GlueColumn Type
    """
    logger.debug(glue_type)
    meta_type = get_meta_type(glue_type)

    if meta_type == 'string':
        return GlueColumnString()

    elif meta_type == 'boolean':
        return GlueColumnBoolean()

    elif meta_type == 'array':
        # Parse the content inside 'array<>'
        nested_content = get_column(glue_type=remove_meta_type(glue_type), glue_name=glue_name)

        nested_meta_type = get_meta_type(remove_meta_type(glue_type))
        if nested_meta_type == 'struct':
            content_name = glue_name
        else:
            content_name = nested_meta_type

        return GlueColumnArray(content=nested_content, content_name=content_name)

    elif meta_type == 'struct':
        # Extract struct name from pluralized array ancestor
        if glue_name[-1] == 's':
            glue_name = glue_name[:-1]

        # The content of an struct is a Dict of Glue Columns
        nested_content = get_struct_mapping(remove_meta_type(glue_type))
        return GlueColumnStruct(content=nested_content, content_name=glue_name)

    else:
        raise ValueError(f'data type not found: {meta_type}')


def get_glue_table(glue_schema: List) -> dict:
    """
    Convert glue schema to JSON format, where each column is a GlueColumn Type
    :param glue_schema: boto3 glue schema columns output
    :return: JSON
    """
    result = {}

    for item in glue_schema:
        item_type = item['Type']
        item_name = item['Name']
        result[item_name] = get_column(item_type, item_name)

    return result


def get_proto(schema: dict, base_name: str) -> List[str]:
    proto_lines: List = []
    nested_messages: List = []
    tab: str = '    '
    # Header
    proto_lines.append(f'\nmessage {base_name} {{')
    # Fields
    for num, key in enumerate(schema, 1):
        # Catalog nested messages
        if schema[key].proto_type == 'message':
            nested_messages.append(key)
            proto_lines.append(f'{tab}{schema[key].content_name} {key} = {num}')
        elif schema[key].proto_type == 'repeated':
            nested_messages.append(key)
            proto_lines.append(f'{tab}{schema[key]} {key} = {num}')
        else:
            proto_lines.append(f'{tab}{schema[key]} {key} = {num}')
    # Footer
    proto_lines.append('}')

    for message in nested_messages:
        if schema[message].proto_type == 'repeated' and schema[message].content.proto_type == 'message':
            proto_lines.extend(get_proto(schema=schema[message].content.content,
                                         base_name=schema[message].content.content_name))
        elif schema[message].proto_type == 'message':
            proto_lines.extend(get_proto(schema=schema[message].content, base_name=schema[message].content_name))

    return proto_lines


def get_proto_text(schema: dict, base_name: str) -> str:
    return '\n'.join(get_proto(schema=schema, base_name=base_name))
