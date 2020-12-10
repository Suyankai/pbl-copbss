import numpy as np
import math

'''
# FAST BSS Version 0.1.0:

    meica: Multi-level extraction ICA (stable)
    
# Divide the MultiLevelExtractionICA into several microservices.

# Basic definition:

    S: Source signals. shape = (source_number, time_slots_number)
    X: Mixed source signals. shape = (source_number, time_slots_number)
    A: Mixing matrix. shape = (source_number, source_number)
    B: Separation matrix. shape = (source_number, source_number)
    hat_S: Estimated source signals durch ICA algorithms. 
        shape = (source_number, time_slots_number)

# Notes:

    X = A @ S
    S = B @ X
    B = A ^ -1
    This version is based on the thoughts of Mingyu Ma.
'''

class FastbssBasic():

    def whiten(self, X):
        '''
        # whiten(self, X):

        # Usage:

            Whitening the mixed signals, i.e. matrix X. Let the 
            mixed signals X are uncorrelated with each other. 
            Meanwhile the variance of each mixed signal 
            (i.e. each channel) x is 1, which is the premise of
            standard normal distribution.

        # Parameters:

            X: Mixed signals, matrix X.

        # Output:

            X, V
            X: Whitened mixed signals X.
            V: Whitening matrix.
        '''
        X = X - X.mean(-1)[:, np.newaxis]
        A = np.dot(X, X.T)
        D, P = np.linalg.eig(A)
        D = np.diag(D)
        D_inv = np.linalg.inv(D)
        D_half = np.sqrt(D_inv)
        V = np.dot(D_half, P.T)
        m = X.shape[1]
        return np.sqrt(m)*np.dot(V, X), V

    def whiten_with_inv_V(self, X):
        '''
        # whiten_with_inv_V(self, X):

        # Usage:

            Whitening the mixed signals, i.e. matrix X. Let the 
            mixed signals X are uncorrelated with each other. 
            Meanwhile the variance of each mixed signal 
            (i.e. each channel) x is 1, which is the premise of
            standard normal distribution.

        # Parameters:

            X: Mixed signals, matrix X.

        # Output:

            X, V, V_inv
            X: Whitened mixed signals X.
            V: Whitening matrix.
            V_inv: The inverse of the whitening matrix V.
        '''
        X = X - X.mean(-1)[:, np.newaxis]
        A = np.dot(X, X.T)
        D, P = np.linalg.eig(A)
        D = np.diag(D)
        D_inv = np.linalg.inv(D)
        D_half = np.sqrt(D_inv)
        V = np.dot(D_half, P.T)
        m = X.shape[1]
        V_inv = np.dot(P, np.sqrt(D))
        return np.sqrt(m)*np.dot(V, X), V, V_inv

    def _tanh(self, x):
        gx = np.tanh(x)
        g_x = gx ** 2
        g_x -= 1
        g_x *= -1
        return gx, g_x.sum(axis=-1) 

    def _exp(self, x):
        exp = np.exp(-(x ** 2) / 2)
        gx = x * exp
        g_x = (1 - x ** 2) * exp
        return gx, g_x.sum(axis=-1)

    def _cube(self, x):
        return x ** 3, (3 * x ** 2).sum(axis=-1)

    def decorrelation(self, B):
        '''
        # decorrelation(self, B):

        # Usage:

            Decorrelate the signals. Let each signal (i.e. channel) of 
            B@X is uncorrelated with each other.

        # Parameters:

            B: The estimated separation matrix B.

        # Output:

            Decorrelated separation matrix B.
        '''
        U, S = np.linalg.eigh(np.dot(B, B.T))
        U = np.diag(U)
        U_inv = np.linalg.inv(U)
        U_half = np.sqrt(U_inv)
        rebuild_B = np.dot(np.dot(np.dot(S, U_half), S.T), B)
        return rebuild_B

    def generate_initial_matrix_B(self, V, A=None):
        '''
        # generate_initial_matrix_B(self, V, A=None):

        # Usage:

            Generate the intial separation matrix for newton iteration.

        # Parameters:

            V: The whitening matrix, also used for getting the number of 
                the original sources. 
            A: The estimated mixing matrix. Then, the initial matrix B is 
                (V @ A)^-1. When the value of A is None, this function 
                will return a random matrix B, its size is according to
                the shape of matirx V.

        # Output:

            Initial separation matrix B. 
        '''
        n = np.shape(V)[0]
        if A is None:
            B = np.random.random_sample((n, n))
        else:
            B = np.linalg.inv(np.dot(V, A))
        try:
            return self.decorrelation(B)
        except:
            raise SystemError(
                'Error - initial matrix generation : unkown, please try it again!')
        else:
            return self.generate_initial_matrix_B(V)

    def _iteration(self, B, X):
        '''
        # _iteration(self, B, X):

        # Usage:

            Basic part of newton iteration for BSS.

        # Parameters:

            B: Separation matrix.
            X: Whitened mixed signals.

        # Output:

            Updated separation matrix B.
        '''
        gbx, g_bx = self._tanh(np.dot(B, X))
        B1 = self.decorrelation(np.dot(gbx, X.T) - g_bx[:, None] * B)
        lim = max(abs(abs(np.diag(np.dot(B1, B.T))) - 1))
        # print(lim)
        return B1, lim

    def newton_iteration(self, B, X, max_iter, tol):
        '''
        # newton_iteration(self, B, X, max_iter, tol):

        # Usage:

            Newton iteration part for BSS, the iteration jumps out
            when the convergence is smaller than the determined
            tolerance.

        # Parameters:

            B: Separation matrix.
            X: Whitened mixed signals.
            max_iter: Maximum number of iteration.
            tol: Tolerance of the convergence of the matrix B 
                calculated from the last iteration and the 
                matrix B calculated from current newton iteration.

        # Output:

            B,lim
            B: Separation matrix B.
            lim: Convergence of the iteration.
        '''
        for _ in range(max_iter):
            B, lim = self._iteration(B, X)
            if lim < tol:
                break
        return B, lim

class MultiLevelExtractionICA_new(FastbssBasic): #需要放到节点里的函数

    def newton_iteration_auto_break_new(self, B, X, miu, max_iter, tol, break_coef):
        '''
        # newton_iteration_auto_break(self, B, X, max_iter, break_coef):

        # Usage:

            Newton iteration part for BSS, the iteration jumps out
            automatically when the convergence decrease slower.

        # Parameters:

            B: Separation matrix.
            X: Whitened mixed signals.
            max_iter: Maximum number of iteration.
            break_coef: The paramter, which determine when the iteration
                should jump out.
            miu: The parameter, which simulate the extraction intervall by change its original tolerance

        # Output:

            B,lim
            B: Separation matrix B.
            lim: Convergence of the iteration.
        '''
        _sum = 0
        _max = 0
        for _ in range(max_iter):
            B, lim = self._iteration(B, X)
            self.Stack.append(lim)
            if lim > _max:
                _max = lim
                self.Stack = [lim]
                _sum = 0
            _sum += lim
            if _sum < math.sqrt(miu)*break_coef*0.5*(self.Stack[0]+self.Stack[-1])*len(self.Stack) or self.Stack[-1] < math.sqrt(miu)*tol:# 要进行分割的地方
                break
        return B, lim

    def multi_level_extraction_newton_iteration_new(self, X, B, lim, step, miu, max_iter, tol, break_coef, _ext_multi_ica):
        '''
        # multi_level_extraction_newton_iteration
        # (self, X, B, max_iter,  break_coef, _ext_multi_ica):

        # Usage:

            Newton iteration with multi-level signal extraction, the extraction
            interval is (_ext_multi_ica)^grad, grad=_ext_multi_ica,...,3,2,1.

        # Parameters:

            B: Separation matrix.
            X: Whitened mixed signals.
            lim: Convergence of the iteration.
            step: The step of determanition of the loop and the start of the next loop.
            miu: The parameter, which simulate the extraction intervall by change its original tolerance            
            max_iter: Maximum number of iteration.
            break_coef: The paramter, which determine when the iteration
                should jump out.            
            _ext_multi_ica: The maximum signal extraction interval is  m/((_ext_multi_ica)^grad) >= n

        # Output:

            Separation matrix B.
            LS: the combined matrix of lim and step
            LS[0] = lim
            LS[1] = step
        '''
        n, m = X.shape
        _grad = int(math.log(m//n, _ext_multi_ica))
        _prop_series = _ext_multi_ica**np.arange(_grad, -1, -1)
        for i in range(step, _grad+1):
            _X = X[:, ::_prop_series[i]]
            _X, V, V_inv = self.whiten_with_inv_V(_X)
            B = self.decorrelation(np.dot(B, V_inv))
            self.Stack = []
            B, lim = self.newton_iteration_auto_break_new(
                B, _X, miu, max_iter, tol, break_coef)
            B = np.dot(B, V) #为何此处没有break
            step += 1#此处可能会有问题
        LS = [lim, step]
        return B, LS
    

    def meica_new(self, X, B, lim, step, miu, max_iter=100, tol=1e-04, break_coef=0.9, ext_multi_ica=8):
        '''
        # mleica(self, X, max_iter=100, break_coef=0.9, ext_multi_ica=8): 

        # Usage:

            Newton iteration with multi-level signal extraction, the extraction
            interval is 2^n, n=_ext_multi_ica,...,3,2,1.

        # Parameters:

            X: Mixed signals, which is obtained from the observers.
            lim: Convergence of the iteration.
            step: The step of determanition of the loop and the start of the next loop.
            miu: The parameter, which simulate the extraction intervall by change its original tolerance 
            max_iter: Maximum number of iteration.
            break_coef: The paramter, which determine when the iteration
                should jump out.
            _ext_multi_ica: The maximum signal extraction interval is  2^_ext_multi_ica

        # Output:

            Seperation matrix B2
            LS: the combined matrix of lim and step
            LS[0] = lim
            LS[1] = step
        '''
        self.Stack = []
        self.LS = []
        B1 = self.generate_initial_matrix_B(X)
        B2, LS = self.multi_level_extraction_newton_iteration_new(
            X, B1, lim, step, miu, max_iter, tol, break_coef, ext_multi_ica)
        #S2 = np.dot(B2, X)# 节点中X记得传过来
        return B2, LS


microservice = MultiLevelExtractionICA_new()
    
    
    
    
    
    
    
    