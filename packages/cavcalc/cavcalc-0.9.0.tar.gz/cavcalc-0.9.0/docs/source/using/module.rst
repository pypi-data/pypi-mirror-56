.. _module:

Using as a Python module
========================

Whilst `cavcalc` is primarily a command line tool, it can also be used just as easily from within Python
in a more "programmatic" way. The recommended method for doing this is to use the single function interface
provided via :func:`cavcalc.calculate`. This function works similarly to the command line interface, where a target
can be specified along with a variable number of keyword arguments corresponding to physical parameters. It then
returns a :class:`cavcalc.Output` object which has a number of properties and methods for accessing the results and
plotting them against the parameters provided.

For example, the following script will compute all available targets from the cavity length and mirror radii
of curvature provided::

    import cavcalc as cc

    # target = "all" is default behaviour
    # parameters can be given as single values, an array of values or a tuple
    # where the first element is as before and the second element is a valid
    # string representing the units of the parameter
    out = cc.calculate(L=(4, 'km'), Rc1=1934, Rc2=2245)

    # we can get a dictionary of all the computed results...
    computed = out.get()

    # ... or just a single one if we want
    w0 = out['w0']

    # out can also be printed displaying results in the same way as the command line tool
    print(out)
