class a:
    def foo(self, x):
        def f(s, x):
            return x+1
        self.foo = f = f.__get__(self, a)
        return f(x)


z = a()
print(z.foo(10))
