Provide `vlog(log_level, *args, **kwargs)` function
which simply does `print(*args, **kwargs)` iff `vlog.GLOBAL_LOG_LEVEL >= log_level`.

Also provides a command line wrapper so you can call

    vlog <log_level> "Some words"

to get appropriate echoing on the command line if `$GLOBAL_VLOG_LEVEL >= <log_level> `

After

    pip3 install .

`vlog --help` will show the flags to the executable script `vlog`.

EXAMPLE
=======

In Python,

    from vlog import vlog
    vlog.GLOBAL_LOG_LEVEL = 10
    vl = vlog.vlog

    vl(9, "This will print,")
    vl(10, "so will this,")
    vl(11, "but this will not print.")

and at the shell,

    $ GLOBAL_VLOG_LEVEL=10 vlog 10 This will print,
    $ GLOBAL_VLOG_LEVEL=10 vlog 11 but this will not print.
