import random

__version__ = "1.0.0.dev1"

class Matrix:
    """ 2D numerical Matrix class based on 2D python numerical list.
    
    Attributes:
        m_row (int): # of rows
        n_col (int): # of columns
        data (int/float): matrix-value in m_row x n_col grid        
    """
    
    def __init__(self, m_row, n_col, type=0.0):
        """ class constructor: set/init attributes of the class
        
        Args:
            m_row (int): # of matrix-row
            n_col (int): # of matrix-column
            type (int/float or str):
                type(int/float): initial value for matrix-element
                type(str): support few frequent matrix type,and can be expanded
                    str='rand': element from uniform random value [0,1]
                    str='norm': element from normal distribution, mean=0, std=1
                    str='zeros': all elements = 0.0
                    str='ones': all elements = 1.0
                    str='identity': Identity matrix, diagonal 1.0, others 0.0
                note:
                    random.random(): return random float number [0.0 - 1.0)
                    random.gauss(mu=mean, sigma=std) used for normal
            
        Returns:
            None
        """
        if not (isinstance(m_row, int) and isinstance(n_col, int)):
            raise TypeError('arg1,2: both matrix dimensions must be integers')
        if (n_col < 1)  or (m_row < 1):
            raise ValueError('arg1,2: both matrix dimensions must be integers >=1')            
        
        self.m_row = m_row
        self.n_col = n_col        
        init_fill = None
        
        if isinstance(type, str) and type == 'zeros':
            init_fill = 0.0
        elif isinstance(type, str) and type == 'ones':
            init_fill = 1.0
        elif isinstance(type, (float,int)):
            init_fill = type
        
        if(init_fill != None):
            self.data = [[init_fill]*self.n_col for z in range(self.m_row)]
        else:
            if isinstance(type, str) and type == 'identity':
                if self.m_row != self.n_col:
                    print("Warning: Identity matrix should have the same numbers of rows and colums, smaller is used!")
                    tmp = min(self.m_row, self.n_col)
                    self.m_row = tmp
                    self.n_col = tmp                    
                #
                self.data = [[0.0]*self.n_col for z in range(self.m_row)]
                for j in range(self.m_row):
                    self.data[j][j]=1.0
            #-----------------------------------------------------------------
            elif isinstance(type, str) and type == 'rand':
                self.data = [[0.0]*self.n_col for z in range(self.m_row)]
                for i in range(self.m_row):
                    for j in range(self.n_col):
                        self.data[i][j]=random.random()
            #------------------------------------------------------------------
            elif isinstance(type, str) and type == 'norm':
                self.data = [[0.0]*self.n_col for z in range(self.m_row)]
                for i in range(self.m_row):
                    for j in range(self.n_col):
                        self.data[i][j]=random.gauss(0.0, 1.0)
            #-----------------------------------------------------------------
            else:
                print('supported values for third arg are:')
                print('int or float= initial value for matrix-element')
                print('str="rand": element from uniform random value [0,1]')
                print('str="norm": element from normal distribution, mean=0, std=1')
                print('str="zeros: all elements = 0.0')
                print('str="ones": all elements = 1.0')
                print('str="identity": Identity matrix, diagonal 1.0, others 0.0')
                raise ValueError('arg3: Invalid value; see supported values at above')
                
    def __str__(self):
        mat_str='\n'
        for i in range(self.m_row):
            for j in range(self.n_col):
                mat_str += ' '+str(self.data[i][j])
            mat_str += '\n'            
            
        return mat_str
        
    @classmethod
    def fromList(cls,lst):
        """we can use existing 2D-python numerical list to initialize the matrix
        
        Args:
            2D-list with int/float values
            
        Returns:
            Matrix version of the given list                
        """
        
        if isinstance(lst, list):
            m_row = len(lst)
            if isinstance(lst[0], list):
                n_col = len(lst[0])
                if isinstance(lst[0][0], list):
                    raise ValueError('given list has more than 2 dimension, not supported')
                elif cls.isAllItemNumeric(lst):                    
                    mat=Matrix(m_row,n_col,lst[0][0])
                    mat.data = lst
                else:
                    raise TypeError('only 2D-list with numeric(int/float) values are supported')
            else:
                raise TypeError('1D-list is not a valid list to initiate 2D matrix')
                
        return mat
    
    @staticmethod
    def isAllItemNumeric(lst):
        """check if all elements of the list is int or float
        
        Args:
            lst (list): 2D list
            
        Returns:
            boolean True if all elements are numeric (int/float), False otherwise
        """
        result = True
        for row in lst:
            for item in row:
                if not isinstance(item, (int, float)):
                    result = False                    
                    break
        
        return result
               
        
    def __getitem__(self, idx):
        """ overwrite magic method to get matrix item at [i][j]
            
        Args:
            idx: is an implicit tuple made of (i,j)
            
        Returns:
            the matrix value at row: i, column: j
        """        
        return self.data[idx[0]][idx[1]]

    def __setitem__(self, idx, val):
        """ overwrite magic method to set matrix item at [i][j]
            
        Args:
            idx: is an implicit tuple made of (i,j)
            val (float): the value to set for element [i][j]
            
        Returns:
            None
        """            
        self.data[idx[0]][idx[1]] = val        


    def __repr__(self):
        """ overwrite magic method for matrix representation
        
        Args:
            None
            
        Returns:
            string of matrix representation
        """
        mat_str = '{}x{} 2D-Matrix:'.format(self.m_row,self.n_col)
        mat_str += self.__str__()
        return mat_str
    
    def size(self):
        """ return the size of matrix m_row and n_col in a tuple
        
        Args:
            None
            
        Returns:
            a tuple contains m_row and n_colm (matrix dimension)                
        """
        return (self.m_row, self.n_col)
    
    def round_ndigit(self, ndigit=0):
        """round function mainly added to help unittest for random cases
        It use usual python round function
        
        Args:
            ndigit (int): number of digits after floating point
            
        Returns:
            None (Note: rounding applied in place)
        """
        for i in range(self.m_row):
            for j in range(self.n_col):
                self.data[i][j]=round(self.data[i][j], ndigit)
    #-------------------------------------------------------------------------
    def __eq__(self, mat):
        """ equality test between this matrix and another using magic method
        
        Args:
            mat (Matrix)
            
        Returns:
            True if equal, False otherwise
        """
        return (self.data == mat.data)
    
    def __add__(self, mat):
        """ adding another matrix to this matrix or scalar to all of its element
        
        Args:
            mat (scaler:int/float or Matrix)
            
        Returns:
            new Matrix resulted from this + mat-Matrix or this-elements +mat-scalar        
        """
        if isinstance(mat,(int,float)):
            result = Matrix(self.m_row,self.n_col,mat)
            for i in range(self.m_row):
                for j in range(self.n_col):
                    result.data[i][j]+=self.data[i][j]
            
        elif isinstance(mat, Matrix):
            if self.size() != mat.size():
                raise ValueError('Cannot add two matrix of different size')
            else:
                result = Matrix(self.m_row,self.n_col,0.0)
                for i in range(self.m_row):
                    for j in range(self.n_col):
                        result.data[i][j] = self.data[i][j]+mat.data[i][j]                
        else:
            raise TypeError('Matrix can be added to another matrix or scalar')
            
        return result

    def __sub__(self, mat):
        """ subtracting another matrix from this matrix or scalar from all of its element
        
        Args:
            mat (scaler:int/float or Matrix)
            
        Returns:
            new Matrix resulted from this - mat-Matrix or this-elements -mat-scalar        
        """
        if isinstance(mat,(int,float)):
            result = Matrix(self.m_row,self.n_col,0.0)
            for i in range(self.m_row):
                for j in range(self.n_col):
                    result.data[i][j] = self.data[i][j]-mat
            
        elif isinstance(mat, Matrix):
            if self.size() != mat.size():
                raise ValueError('Cannot sub two matrix of different size')
            else:
                result = Matrix(self.m_row,self.n_col,0.0)
                for i in range(self.m_row):
                    for j in range(self.n_col):
                        result.data[i][j] = self.data[i][j] - mat.data[i][j]                
        else:
            raise TypeError('Matrix can be subtracted from another matrix or scalar')
            
        return result

    def __mul__(self, mat):
        """ multiply another matrix to this matrix or scalar to all of its element
        
        Args:
            mat (scaler:int/float or Matrix)
            
        Returns:
            new Matrix resulted from this x mat-Matrix or this-elements x mat-scalar        
        """
        if isinstance(mat,(int,float)):
            result = Matrix(self.m_row,self.n_col,mat)
            for i in range(self.m_row):
                for j in range(self.n_col):
                    result.data[i][j] *=self.data[i][j]
            
        elif isinstance(mat, Matrix):
            if self.n_col != mat.m_row:
                raise ValueError('Cannot multiply two matrix of different inner-size!')
            else:
                result = Matrix(self.m_row,mat.n_col,0.0)
                list_tuple=list(zip(*mat.data));# list of tuple contains column of mat
                for i in range(self.m_row):
                    for j in range(mat.n_col):
                        for k in range(self.n_col):
                            result.data[i][j] += self.data[i][k]*list_tuple[j][k]
        else:
            raise TypeError('Matrix can be added to another matrix or scalar')
            
        return result
 
    def __iadd__(self, mat):
        """ in place version of __add__
        
        Args:
            mat (scaler:int/float or Matrix)
            
        Returns:
            current matrix += mat-Matrix or its elements +mat-scalar        
        """
        tmp = self + mat #[TODO] not an optimum implementation
        self.data = tmp.data
        return self

    def __isub__(self, mat):
        """ in place version of __sub__
        
        Args:
            mat (scaler:int/float or Matrix)
            
        Returns:
            current matrix -= mat-Matrix or its elements -mat-scalar        
        """
        tmp = self - mat #[TODO] not an optimum implementation
        self.data = tmp.data
        return self

    def __imul__(self, mat):
        """ in place version of __mul__
        
        Args:
            mat (scaler:int/float or Matrix)
            
        Returns:
            current matrix *= mat-Matrix or its elements *at-scalar        
        """
        tmp = self * mat
        self.fromList(tmp.data)
        return self
##############################################################################