class Output:

    def __init__(self, file="", verbose=False):
        self.file = file
        self.is_verbose = verbose

    def output(self, text, only_verbose=False):
        if not only_verbose or self.is_verbose:
            print(text)

        if not only_verbose and self.file:
            self.__write_to_file(text)

    def verbose(self, text):
        self.output(text, True)

    def __write_to_file(self, content):
        if self.verbose:
            print("Writing to " + self.file)
        f = open(self.file, "w+")
        f.write(content)
        f.write("\n")
        f.close()
