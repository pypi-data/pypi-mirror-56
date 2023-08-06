import logging
import os
from glue2protojson import utils
from glue2protojson import gluetypes


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s:::%(levelname)s:::%(name)s:::%(module)s:::%(funcName)s:::%(message)s',
        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Read Schema from Glue
    glue_schema_tenant = utils.get_schema_from_glue(database=os.environ['GLUE_DATABASE'],
                                                    table=os.environ['GLUE_TABLE'])
    logger.info(f'GLUE CONTENT:::{glue_schema_tenant}')

    # Parse Glue Schema to Json
    glue_table = utils.get_glue_table(glue_schema=glue_schema_tenant)
    logger.info(f'GLUE CONTENT PARSED TO JSON:::{glue_table}')

    # Glue Schema to Proto
    proto_text = utils.get_proto_text(schema=glue_table, base_name='Tenant')
    logger.info(f'GLUE CONTENT PARSED TO PROTO:::{proto_text}')
