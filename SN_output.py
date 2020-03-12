

class Output:
    @classmethod
    def from_file(cls, path):
        data = []
        with open(path) as f:
            for line in f:
                value = line.split()
                data.append((float(value[0]), float(value[1]), float(value[2])))
        
        return data
    
    @classmethod
    def width(cls, data):
        o1_width = cls.object_width(data, 0)
        o2_width = cls.object_width(data, 1)
        o3_width = cls.object_width(data, 2)
        return (o1_width, o2_width, o3_width)

    @classmethod
    def object_width(cls, data, key):
        sort_key = sorted(data, key=lambda tup: tup[key])
        return (sort_key[-1][key] - sort_key[0][key])

path = "./output/output/{}/converge_no-dem1_r25_1/{}.out".format("mode", 0)
data = Output.from_file(path)
print(Output.width(data))
