import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.plugins.toolkit import Invalid

def custom_empty_validator(value, context):
    if value is None:
        raise Invalid("Missing value")
    return value

class Data_Uploader_ThemePlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IConfigurer)
    
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'data_uploader_theme')

    def _modify_package_schema(self, schema):
        schema.update({
            'fname': [toolkit.get_validator('not_empty'), toolkit.get_converter('convert_to_extras')],
            'surname': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'user_email': [toolkit.get_validator('not_empty'), toolkit.get_validator('email_validator'), toolkit.get_converter('convert_to_extras')],
            'institute': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'orcid': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'grantnumber': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'latitude': [toolkit.get_validator('not_empty'), toolkit.get_converter('convert_to_extras')],
            'longitude': [toolkit.get_validator('not_empty'), toolkit.get_converter('convert_to_extras')],
            'rocktype': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'minofinterest': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')]
        })
        return schema

    def create_package_schema(self):
        schema = super(Data_Uploader_ThemePlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(Data_Uploader_ThemePlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(Data_Uploader_ThemePlugin, self).show_package_schema()
        print (schema)
        schema.update({
            'fname': [toolkit.get_converter('convert_from_extras'), toolkit.get_validator('ignore_missing')],
            'surname': [toolkit.get_converter('convert_from_extras'), toolkit.get_validator('ignore_missing')],
            'user_email': [toolkit.get_converter('convert_from_extras'), toolkit.get_validator('ignore_missing')],
            'institute': [toolkit.get_converter('convert_from_extras'), toolkit.get_validator('ignore_missing')],
            'orcid': [toolkit.get_converter('convert_from_extras'), toolkit.get_validator('ignore_missing')],
            'grantnumber': [toolkit.get_converter('convert_from_extras'), toolkit.get_validator('ignore_missing')],
            'latitude': [toolkit.get_converter('convert_from_extras'), toolkit.get_validator('ignore_missing')],
            'longitude': [toolkit.get_converter('convert_from_extras'), toolkit.get_validator('ignore_missing')],
            'rocktype': [toolkit.get_converter('convert_from_extras'), toolkit.get_validator('ignore_missing')],
            'minofinterest': [toolkit.get_converter('convert_from_extras'), toolkit.get_validator('ignore_missing')],
        })
        return schema
    
    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []