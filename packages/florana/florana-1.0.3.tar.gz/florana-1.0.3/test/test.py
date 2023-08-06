try:
    raise StopIteration("hello, error")
except Exception as e:
    print('\n'.join(e.args))
