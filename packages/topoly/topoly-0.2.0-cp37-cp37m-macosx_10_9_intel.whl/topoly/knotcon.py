import os
import numpy as np
import polvalues
import re
from abc import ABC, abstractmethod
from numpy.polynomial.polynomial import Polynomial
# Na razie dziala tylko dla Yamady

class Poly(ABC):
    @abstractmethod
    def __init__(self, name, value, invariant = None):
        self.name  = name
        self.val   = value[0]
        self.inv   = invariant
        if value[1] == None: self.power = None
        else: self.power = float(value[1])
    def __add__(self, other):
        self.check_compatibility(other)
        new_name = self.name + ' U ' + other.name
        return new_name
    def __mul__(self, other):
        self.check_compatibility(other)
        new_name = self.name + ' # ' + other.name
        return new_name
    def __repr__(self):
        return '{}: {}'.format(self.name, self.pol2str())
    def check_compatibility(self,other):
        if self.inv != other.inv:
            print("Don't mix invariants!!")
            return None
    def pol2str(self):
        arr = [str(int(s)) for s in self.val]
        return ' '.join(arr)
    @staticmethod
    def str2pol(poly):
        if '{' in poly:
            power, poly = poly.split(' | ')
            power = power.lstrip('{ ').rstrip(' }')
        else:
            power = None
        converted = [int(s) for s in poly.split(' ')] 
        return Polynomial(converted), power


class Poly2D(Poly):
    @abstractmethod
    def __init__(self, name, value, invariant = None):
        self.name = name
        self.val  = value
        self.inv  = invariant
    def pol2str(self):
        val, col0, row0 = self.val
        y = val.shape[0]
        arr = val.tolist()
        string = ''
        for j in range(y):
            arr[j][col0] = '[{}]'.format(str(arr[j][col0]))
            arr[j] = '{}'.format(str(arr[j])).replace("'",'')[1:-1]
            arr[j] = arr[j].replace(',','').strip(' 0')
        arr[row0] = '[{}]'.format(arr[row0])
        arr = '|'.join(arr)
        return arr
    @staticmethod
    def mul_val(val1, val2):
        arr1, col01, row01 = val1
        arr2, col02, row02 = val2
        x1,y1 = arr1.shape
        x2,y2 = arr2.shape
        new_arr = np.zeros([x1+x2-1,y1+y2-1], dtype=np.int)
        col0 = col01 + col02
        row0 = row01 + row02
        for j in range(y1):
            for i in range(x1):
                new_arr[i:i+x2,j:j+y2] += arr2*arr1[i,j]
        return new_arr, col0, row0
    @staticmethod
    def str2pol(poly):
        poly   = poly.split('|')
        col0   = []
        rowlen = []
        # identify where second variable vanishes
        for j in range(len(poly)):
            poly[j] = poly[j].split(' ')
            for i in range(len(poly[j])):
                m = re.search('\[-?[0-9]+\]', poly[j][i])
                if m:
                    poly[j][i] = poly[j][i][1:-1]
                    col0.append(i)
                    rowlen.append(len(poly[j]))
                    break
        # identify where first variable vanishes
        for j in range(len(poly)):
            m = re.search('\[.*',poly[j][0])
            if m:
                poly[j][0] = poly[j][0][1:]
                poly[j][-1] = poly[j][-1][:-1]
                row0 = j
        # create matrix
        left = max(col0)
        right = max([rowlen[i] - col0[i] - 1 for i in range(len(col0))])
        arr = np.zeros([len(rowlen),left+right+1], dtype=np.int)
        for j in range(len(poly)):
            for i in range(len(poly[j])):
                arr[j,i+left-col0[j]] = poly[j][i]
        col0 = left
        return arr, col0, row0

class HOMFLYPT(Poly2D):
    def __init__(self, name, value):
        super().__init__(name, value, 'HOMFLYPT')
    def __add__(self, other):
        new_name = super().__add__(other)
        new_val = self.mul_val(self.val, other.val)
        new_val = self.mul_val(new_val, invs[inv].str2pol('[[0]]|-1 [0] 1'))
        return invs[self.inv](new_name, new_val)
    def __mul__(self, other):
        new_name = super().__mul__(other)
        new_val = Poly2D.mul_val(self.val, other.val)
        return invs[self.inv](new_name, new_val)

class Kauffman_polynomial(Poly2D):
    def __init__(self, name, value):
        super().__init__(name, value, 'Kauffman polynomial')
    def __add__(self, other):
        new_name = super().__add__(other)
        new_val = self.mul_val(self.val, other.val)
        new_val = self.mul_val(new_val, invs[inv].str2pol('[[-1]]|1 [0] 1'))
        return invs[self.inv](new_name, new_val)
    def __mul__(self, other):
        new_name = super().__mul__(other)
        new_val = Poly2D.mul_val(self.val, other.val)
        return invs[self.inv](new_name, new_val)

class Jones(Poly):
    def __init__(self, name, value):
        super().__init__(name, value, 'Jones')
    def __add__(self, other):
        new_name = super().__add__(other)
        new_val = self.val * other.val * Polynomial((-1, -1))
        new_power = self.power + other.power - 0.5
        return invs[self.inv](new_name, (new_val, new_power))
    def __mul__(self, other):
        new_name = super().__mul__(other)
        new_val = self.val * other.val
        new_power = self.power + other.power
        return invs[self.inv](new_name, (new_val, new_power))
    def pol2str(self):
        if self.power == int(self.power):
            power = int(self.power)
        else:
            power = self.power
        arr = [str(int(s)) for s in self.val]
        string = "{{ {} }} | {}".format(power, ' '.join(arr))
        return string

# jeszcze poprawić, jak wyglada suma?
class BLMHo(Poly):
    def __init__(self, name, value):
        super().__init__(name, value, 'BLM/Ho')
    def __add__(self, other):
        new_name = super().__add__(other)
        new_val = self.val * other.val * Polynomial((-1, -1))
        new_power = self.power + other.power
        return invs[self.inv](new_name, (new_val, new_power))
    def __mul__(self, other):
        new_name = super().__mul__(other)
        new_val = self.val * other.val
        new_power = self.power + other.power
        return invs[self.inv](new_name, (new_val, new_power))
    def pol2str(self):
        if self.power == int(self.power):
            power = int(self.power)
        else:
            power = self.power
        arr = [str(int(s)) for s in self.val]
        string = "{{ {} }} | {}".format(power, ' '.join(arr))
        return string

class Yamada(Poly):
    def __init__(self, name, value):
        super().__init__(name, value, 'Yamada')
    def __add__(self, other):
        new_name = super().__add__(other)
        new_val = self.val * other.val
        return invs[self.inv](new_name, (new_val, None))
    def __mul__(self, other):
        self.check_compatibility(other)
        new_name = self.name + ' #2 ' + other.name
        new_val = self.val * other.val // Polynomial((1,1,1))
        return invs[self.inv](new_name, (new_val, None))
    def __pow__(self, other):
        self.check_compatibility(other)
        new_name = self.name + ' #3 ' + other.name
        new_val = self.val * other.val // Polynomial((-1,-1,-2,-1,-1))
        return invs[self.inv](new_name, (new_val, None))

class Alexander(Poly):
    def __init__(self, name, value):
        super().__init__(name, value, 'Alexander')
    def __add__(self, other):
        new_name = super().__add__(other)
        new_val  = Polynomial((0))
        return invs[self.inv](new_name, (new_val, None))
    def __mul__(self, other):
        new_name = super().__mul__(other)
        new_val = self.val * other.val
        return invs[self.inv](new_name, (new_val, None))

class Conway(Poly):
    def __init__(self, name, value):
        super().__init__(name, value, 'Conway')
    def __add__(self, other):
        new_name = super().__add__(other)
        new_val  = Polynomial((0))
        return invs[self.inv](new_name, (new_val, None))
    def __mul__(self, other):
        new_name = super().__mul__(other)
        new_val = self.val * other.val
        return invs[self.inv](new_name, (new_val, None))

class Kauffman_bracket(Poly):
    def __init__(self, name, value):
        super().__init__(name, value, 'Kauffman bracket')
    def __add__(self, other):
        new_name = super().__add__(other)
        new_val = self.val * other.val * Polynomial((-1, 0, 0, 0, -1))
        return invs[self.inv](new_name, (new_val, None))
    def __mul__(self, other):
        new_name = super().__mul__(other)
        new_val = self.val * other.val
        return invs[self.inv](new_name, (new_val, None))

invs={'Alexander': Alexander,
      'Conway': Conway,
      'Jones': Jones,
      'HOMFLY': HOMFLYPT,
      'HOMFLYPT': HOMFLYPT,
      'HOMFLY-PT': HOMFLYPT,
      'Yamada': Yamada,
      'Kauffman bracket': Kauffman_bracket,                               
      'Kauffman polynomial': Kauffman_polynomial,                         
      'BLM/Ho': BLMHo,     
      'BLMHo': BLMHo}     
    
polval_invs={'Alexander': polvalues.Alexander,
             'Conway': polvalues.Conway,
             'Jones': polvalues.Jones,
             'HOMFLY': polvalues.HOMFLYPT,
             'HOMFLYPT': polvalues.HOMFLYPT,
             'HOMFLY-PT': polvalues.HOMFLYPT,
             'Yamada': polvalues.Yamada,
             'APS': polvalues.APS,
             'Kauffman bracket': polvalues.Kauffman_bracket,
             'Kauffman polynomial': polvalues.Kauffman_polynomial,
             'BLM/Ho': polvalues.BLMHo, 
             'BLMHo': polvalues.BLMHo}     

def create(inv, name, val = None):
    if val != None:
        return [invs[invariant](name, invs[inv].str2pol(val))]
    topols_list = np.array(list(polval_invs[inv].values()))
    polys_list = np.array(list(polval_invs[inv].keys()))
    indexes = np.where(name == topols_list)[0]
    polys = []
    for index in indexes:
        val  = str(polys_list[index]).replace("'",'')
        val  = invs[inv].str2pol(val)
        poly = invs[inv](name, val)
        polys.append(poly)
    return polys

def export(polys, export_file = 'new_polvalues.py'):
    print('export_file: ', export_file)
    try: os.mknod(export_file)
    except: print('{} exists. Deleting'.format(export_file))
    with open(export_file, 'w') as f:
        for poly in polys:
            f.write("{}['{}'] = '{}'\n".format(poly.inv, str(poly), poly.name))
        dic = """\npolvalues = {'Alexander': Alexander,
             'Conway': Conway,
             'Jones': Jones,
             'HOMFLY': HOMFLYPT,
             'HOMFLYPT': HOMFLYPT,
             'HOMFLY-PT': HOMFLYPT,
             'Yamada': Yamada,
             'APS': APS,
             'Kauffman bracket': Kauffman_bracket,
             'Kauffman polynomial': Kauffman_polynomial,
             'BLM/Ho': BLMHo,
             'BLMHo': BLMHo}"""
        f.write(dic)

if __name__ == '__main__':
    polys = []
    for inv in invs.keys():
        print('====={}====='.format(inv))
        aa = create(inv, '3_1')
        bb = create(inv, '4_1')
        print(aa)
        print(bb)
        for a in aa:
            for b in bb:
                polys.append(a+b)
                polys.append(a*b)
    export(polys) 
