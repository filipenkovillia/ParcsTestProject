from Pyro4 import expose


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        arr = self.read_input()

        step = int(len(arr) / len(self.workers))
        mapped = []

        for i in xrange(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(([str(i) for i in arr[i * step:i * step + step]])))

        self.write_output(mapped)

    @staticmethod
    @expose
    def mymap(a):
        primes = []
        for el in a:
            if Solver.isGrow(int(el)):
                primes.append(str(el))
        return primes

    @staticmethod
    @expose
    def myreduce(mapped):
        print("reduce")
        output = []
        for primes in mapped:
            print("reduce loop")
        output = output + primes.value
        print("reduce done")
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = [int(line.rstrip('\n')) for line in f]
        f.close()
        return line

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        for a in output:
            for i in a.value: f.write(str(i) + ' ')
        f.close()

    @staticmethod
    @expose
    def isGrow(n):
        num_as_str = str(n)
        if len(num_as_str) == 1:
            return True
        for i in range(1, len(num_as_str)):
            if num_as_str[i] < num_as_str[i - 1]:
                return False
        return True