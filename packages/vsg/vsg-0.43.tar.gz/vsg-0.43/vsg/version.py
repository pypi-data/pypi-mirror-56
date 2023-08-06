version = '0.43'


def print_version(oCommandLineArguments):

    if (oCommandLineArguments.version):
        print('VHDL Style Guide (VSG) version ' + str(version))
        exit(0)
