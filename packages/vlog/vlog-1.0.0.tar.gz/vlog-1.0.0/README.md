Provide `vlog(log_level, *args, **kwargs)` function
which simply does `print(*args, **kwargs)` iff `log_level >= vlog.GLOBAL_LOG_LEVEL`.

Also provides a command line wrapper so you can call

    vlog <log_level> "Some words"

to get appropriate echoing on the command line if `<log_level> >= $GLOBAL_VLOG_LEVEL`

After

    pip3 install .

`vlog --help` will show the flags to the executable script `vlog`.

EXAMPLE
=======

In Python,

    from vlog import vlog
    vlog.GLOBAL_LOG_LEVEL = 10
    vl = vlog.vlog

    vl(9, "This will not print,")
    vl(10, "but this will print.")

and at the shell,

    $ GLOBAL_VLOG_LEVEL=11 vlog 10 This will not print,
    $ GLOBAL_VLOG_LEVEL=11 vlog 11 but this will print.
