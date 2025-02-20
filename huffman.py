import tkinter as tk
import six
import sys

class HuffNode(object):
    def get_wieght(self):
        raise NotImplementedError(
            "The Abstract Node Class doesn't define 'get_wieght'")
    def isleaf(self):
        raise NotImplementedError(
            "The Abstract Node Class doesn't define 'isleaf'")

class LeafNode(HuffNode):
    def __init__(self, value=0, freq=0, ):
        super(LeafNode, self).__init__()
        self.value = value
        self.wieght = freq

    def isleaf(self):
        return True

    def get_wieght(self):
        return self.wieght

    def get_value(self):
        return self.value

class IntlNode(HuffNode):
    def __init__(self, left_child=None, right_child=None):
        super(IntlNode, self).__init__()
        self.wieght=left_child.get_wieght()+right_child.get_wieght()
        self.left_child=left_child
        self.right_child=right_child
    def isleaf(self):
        return False
    def get_wieght(self):
        return self.wieght
    def get_left(self):
        return self.left_child
    def get_right(self):
        return self.right_child

class HuffTree(object):
    def __init__(self, flag, value =0, freq=0, left_tree=None, right_tree=None):
        super(HuffTree, self).__init__()
        if flag == 0:
            self.root = LeafNode(value, freq)
        else:
            self.root = IntlNode(left_tree.get_root(), right_tree.get_root())
    def get_root(self):
        return self.root
    def get_wieght(self):
        return self.root.get_wieght()
    def traverse_huffman_tree(self, root, code, char_freq):
        if root.isleaf():
            char_freq[root.get_value()] = code
            print(("it = %c  and  freq = %d  code = %s")%(chr(root.get_value()),root.get_wieght(), code))
            return None
        else:
            self.traverse_huffman_tree(root.get_left(), code+'0', char_freq)
            self.traverse_huffman_tree(root.get_right(), code+'1', char_freq)

def buildHuffmanTree(list_hufftrees):
    while len(list_hufftrees) > 1:
        list_hufftrees.sort(key=lambda x: x.get_wieght())
        temp1 = list_hufftrees[0]
        temp2 = list_hufftrees[1]
        list_hufftrees = list_hufftrees[2:]
        newed_hufftree = HuffTree(1, 0, 0, temp1, temp2)
        list_hufftrees.append(newed_hufftree)
    return list_hufftrees[0]


def compress():
    global input
    global output

    inputfilename = input.get()
    outputfilename = output.get()
    f = open(inputfilename, 'rb')
    filedata = f.read()
    filesize = f.tell()

    char_freq = {}
    for x in range(filesize):

        tem = filedata[x]
        if tem in char_freq.keys():
            char_freq[tem] = char_freq[tem] + 1
        else:
            char_freq[tem] = 1


    for tem in char_freq.keys():
        print(tem, ' : ', char_freq[tem])

    list_hufftrees = []
    for x in char_freq.keys():
        tem = HuffTree(0, x, char_freq[x], None, None)
        list_hufftrees.append(tem)

    length = len(char_freq.keys())
    output = open(outputfilename, 'wb')

    a4 = length & 255
    length = length >> 8
    a3 = length & 255
    length = length >> 8
    a2 = length & 255
    length = length >> 8
    a1 = length & 255
    output.write(six.int2byte(a1))
    output.write(six.int2byte(a2))
    output.write(six.int2byte(a3))
    output.write(six.int2byte(a4))

    for x in char_freq.keys():
        output.write(six.int2byte(x))
        temp = char_freq[x]
        a4 = temp & 255
        temp = temp >> 8
        a3 = temp & 255
        temp = temp >> 8
        a2 = temp & 255
        temp = temp >> 8
        a1 = temp & 255
        output.write(six.int2byte(a1))
        output.write(six.int2byte(a2))
        output.write(six.int2byte(a3))
        output.write(six.int2byte(a4))

    tem = buildHuffmanTree(list_hufftrees)
    tem.traverse_huffman_tree(tem.get_root(), '', char_freq)

    code = ''
    for i in range(filesize):
        key = filedata[i]
        code = code + char_freq[key]
        out = 0
        while len(code) > 8:
            for x in range(8):
                out = out << 1
                if code[x] == '1':
                    out = out | 1
            code = code[8:]
            output.write(six.int2byte(out))
            out = 0

    output.write(six.int2byte(len(code)))
    out = 0
    for i in range(len(code)):
        out = out << 1
        if code[i] == '1':
            out = out | 1
    for i in range(8 - len(code)):
        out = out << 1
    output.write(six.int2byte(out))

    output.close()


def decompress():
    global input
    global output

    inputfilename = input.get()
    outputfilename = output.get( )
    f = open(inputfilename, 'rb')
    filedata = f.read()
    filesize = f.tell()

    a1 = filedata[0]
    a2 = filedata[1]
    a3 = filedata[2]
    a4 = filedata[3]
    j = 0
    j = j | a1
    j = j << 8
    j = j | a2
    j = j << 8
    j = j | a3
    j = j << 8
    j = j | a4

    leaf_node_size = j


    char_freq = {}
    for i in range(leaf_node_size):
        c = filedata[4 + i * 5 + 0]


        a1 = filedata[4 + i * 5 + 1]
        a2 = filedata[4 + i * 5 + 2]
        a3 = filedata[4 + i * 5 + 3]
        a4 = filedata[4 + i * 5 + 4]
        j = 0
        j = j | a1
        j = j << 8
        j = j | a2
        j = j << 8
        j = j | a3
        j = j << 8
        j = j | a4
        print(c, j)
        char_freq[c] = j

    list_hufftrees = []
    for x in char_freq.keys():
        tem = HuffTree(0, x, char_freq[x], None, None)
        list_hufftrees.append(tem)

    tem = buildHuffmanTree(list_hufftrees)
    tem.traverse_huffman_tree(tem.get_root(), '', char_freq)

    output = open(outputfilename, 'wb')
    code = ''
    currnode = tem.get_root()
    for x in range(leaf_node_size * 5 + 4, filesize):
        c = filedata[x]
        for i in range(8):
            if c & 128:
                code = code + '1'
            else:
                code = code + '0'
            c = c << 1

        while len(code) > 24:
            if currnode.isleaf():
                tem_byte = six.int2byte(currnode.get_value())
                output.write(tem_byte)
                currnode = tem.get_root()

            if code[0] == '1':
                currnode = currnode.get_right()
            else:
                currnode = currnode.get_left()
            code = code[1:]

    sub_code = code[-16:-8]
    last_length = 0
    for i in range(8):
        last_length = last_length << 1
        if sub_code[i] == '1':
            last_length = last_length | 1

    code = code[:-16] + code[-8:-8 + last_length]

    while len(code) > 0:
        if currnode.isleaf():
            tem_byte = six.int2byte(currnode.get_value())
            output.write(tem_byte)
            currnode = tem.get_root()

        if code[0] == '1':
            currnode = currnode.get_right()
        else:
            currnode = currnode.get_left()
        code = code[1:]

    if currnode.isleaf():
        tem_byte = six.int2byte(currnode.get_value())
        output.write(tem_byte)
        currnode = tem.get_root()

    output.close()

window = tk.Tk()
window.title=('Huffman')
window.geometry('500x400')
tk.Label(window,text='input filename',font=('IBM 3270',16),fg='black',bg='white').place(x=60,y=100)
tk.Label(window,text='output filename',font=('IBM 3270',16),fg='black',bg='white').place(x=300,y=100)

input=tk.StringVar()
entry=tk.Entry(window,textvariable=input,font=('IBM 3270',16),width=13,show=None).place(x=60,y=130)
output=tk.StringVar()
entry=tk.Entry(window,textvariable=output,font=('IBM 3270',16),width=14,show=None).place(x=300,y=130)

ch1=tk.Button(window,text='compress',font=('IBM 3270',16),command=compress,width=11).place(x=60,y=300)
ch2=tk.Button(window,text='decompress',font=('IBM 3270',16),command=decompress,width=11).place(x=310,y=300)
window.mainloop()