import sys
from inspect import signature, Parameter, getsource

from makefun import wraps, add_signature_parameters


def add_fixture_to_signature(sig, fixture_name):
    add_request = fixture_name not in sig.parameters
    request_arg = (
        [Parameter(fixture_name, kind=Parameter.POSITIONAL_OR_KEYWORD)]
        if add_request
        else []
    )

    return (
        add_signature_parameters(sig, request_arg) if request_arg else sig,
        add_request,
    )


def pytester_run(request, func, cmd_args):
    # TODO: better fixtures discovery & auto-imports?
    # TODO: copy fixtures from current test module

    testdir = request.getfixturevalue("testdir")

    # we could dump only one test if we had a good fixture importing mechanism
    # source = remove_some_decorators_from_source(getsource(func))
    # testdir.makepyfile(source)

    # create a temporary pytest test module
    module_path = func.__module__
    module = sys.modules[module_path]
    module_content = getsource(module)

    testdir.makepyfile(remove_some_decorators_from_source(module_content))

    module_tokens = module_path.split(".")

    # /!\ Copying the conftest located at the same level as the test file
    conftest_path = ".".join(module_tokens[:-1] + ["conftest"])
    if conftest_path in sys.modules:
        conftest_source = getsource(sys.modules[conftest_path])
        testdir.makeconftest(conftest_source)

    # run pytest with the following cmd args
    nodeid = "{}.py::{}".format(func.__name__, func.__name__)

    args = ["-v", nodeid]
    args.append(cmd_args) if cmd_args else None
    result = testdir.runpytest(*args)

    # Doesn't work with -s option
    # result.stdout.fnmatch_lines(["*::* PASSED*"],)

    result.assert_outcomes(passed=1)

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0

    return result


def remove_some_decorators_from_source(src):
    lines = src.splitlines()

    # TODO: better way to remove decorators (whatever their names are)
    lines = [l for l in lines if not l.strip().startswith("@isolate")]

    # xfail will stay and be used on the initial test
    # TODO: imagine a test highlighting the need of such behavior
    lines = [l for l in lines if not l.strip().startswith("@pytest.mark.xfail")]

    return "\n".join(lines)


def isolate(wrapped=None, cmd_args=None):
    def real_decorator(func):
        sig = signature(func)
        sig, request_added = add_fixture_to_signature(sig, fixture_name="request")

        @wraps(func, new_sig=sig)
        def wrapper(*args, **kwargs):
            request = kwargs.pop("request") if request_added else kwargs["request"]

            # Instead of running the wrapped function
            # return func(*args, **kwargs)

            # We execute the test with pytester plugin
            pytester_run(request, func, cmd_args)

        return wrapper

    # wrapped will be a callable if the decorator is invocated without parenthesis
    if callable(wrapped):
        return real_decorator(wrapped)
    else:
        return real_decorator
