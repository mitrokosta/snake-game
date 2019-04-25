import datetime

def arguments_check(*types):
  def decorator(function):
    def wrapped(*args):
      for t, a in zip(types, args):
        if not isinstance(a, t):
          raise TypeError('Invalid input types: expected {}; found {}.'.format(', '.join(map(str, types)), ', '.join(map(str, map(type, args)))))
      return function(*args)
    wrapped.__name__ = function.__name__
    wrapped.__doc__ = function.__doc__
    wrapped.__module__ = function.__module__
    return wrapped
  return decorator

@arguments_check(datetime.date, str)
def formatter(date, sep):
  return date.strftime('%d{}%m{}%Y'.format(sep, sep))

