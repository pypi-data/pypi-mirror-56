'''
@Author: hua
@Date: 2019-02-10 09:55:10
@LastEditors: hua
@LastEditTime: 2019-11-25 10:38:05
'''
import cerberus

class CustomErrorHandler(cerberus.errors.BasicErrorHandler):
    def __init__(self, tree=None, custom_messages=None):
        super(CustomErrorHandler, self).__init__(tree)
        self.custom_messages = custom_messages or {}

    def format_message(self, field, error):
        tmp = self.custom_messages
        for x in error.schema_path:
            try:
                tmp = tmp[x]
            except KeyError:
                new = super(CustomErrorHandler, self)
                return new.format_message(field, error)
        if isinstance(tmp, dict):  # if "unknown field"
            new = super(CustomErrorHandler, self)
            return new.format_message(field, error)
        else:
            return tmp
        
        
def validateInputByName(value:dict, name:str, rules:dict, error_msg:dict=dict(), default:str=''):
    ''' 
    * validate input value by column name 
    * @param  dict value
    * @param  string name
    * @param  dict rules
    * @param  dict error_msg
    * @param  string default
    * @return response
    * @validator(name="per_page", rules={'type': 'integer'}, error_msg={}, default=15)
    '''
    v = cerberus.Validator(
        {name:rules}, error_handler=CustomErrorHandler(custom_messages={name:error_msg}))
    if name not in value:
        value[name] = default
    cookedReqVal = {name: value[name]}
    if (v.validate(cookedReqVal)):  # validate
        return value
    return v.errors