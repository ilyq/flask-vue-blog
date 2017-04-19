# coding:utf-8


class ParameterException(Exception):
    '''参数错误'''
    pass

class UsernameException(Exception):
    '''注册失败'''
    pass

class LoginException(Exception):
    '''登陆'''
    pass

class NoLoginException(Exception):
    '''尚未登录'''
    pass

class TokenException(Exception):
    '''token无效'''
    pass

class DataAlreadyExistsException(Exception):
    '''数据已存在'''
    pass

class DataDoesNotExistException(Exception):
    '''数据不存在'''
    pass
