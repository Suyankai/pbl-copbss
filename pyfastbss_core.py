import numpy as np
import math

'''
# FAST BSS Version 0.1.0:

    fastica: FastICA (most stable)
    meica: Multi-level extraction ICA (stable)
    cdica: Component dependent ICA (stable)
    aeica: Adaptive extraction ICA (*warning: unstable!)
    ufica: Ultra-fast ICA (cdica + aeica) (*warning: unstable!)

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
        # decorrelation(self, B):

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


# version3.0
class MultiLevelExtractionICA(FastbssBasic):

    def newton_iteration_auto_break(self, B, X, max_iter, tol, break_coef):
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
            if _sum < break_coef*0.5*(self.Stack[0]+self.Stack[-1])*len(self.Stack) or self.Stack[-1] < tol:
                break
        return B, lim

    def multi_level_extraction_newton_iteration(self, X, B, max_iter, tol, break_coef, _ext_multi_ica):
        '''
        # multi_level_extraction_newton_iteration
        # (self, X, B, max_iter,  break_coef, _ext_multi_ica):

        # Usage:

            Newton iteration with multi-level signal extraction, the extraction
            interval is (_ext_multi_ica)^grad, grad=_ext_multi_ica,...,3,2,1.

        # Parameters:

            B: Separation matrix.
            X: Whitened mixed signals.
            max_iter: Maximum number of iteration.
            break_coef: The paramter, which determine when the iteration
                should jump out.
            _ext_multi_ica: The maximum signal extraction interval is  m/((_ext_multi_ica)^grad) >= n

        # Output:

            Separation matrix B.
        '''
        n, m = X.shape
        _grad = int(math.log(m//n, _ext_multi_ica))
        _prop_series = _ext_multi_ica**np.arange(_grad, -1, -1)
        for i in range(1, _grad+1):
            _X = X[:, ::_prop_series[i]]
            _X, V, V_inv = self.whiten_with_inv_V(_X)
            B = self.decorrelation(np.dot(B, V_inv))
            self.Stack = []
            B,lim= self.newton_iteration_auto_break(
                B, _X, max_iter, tol, break_coef)
            B = np.dot(B, V)
            if lim<=tol:break
        return B

    def meica(self, X, max_iter=100, tol=1e-04, break_coef=0.9, ext_multi_ica=8):
        '''
        # mleica(self, X, max_iter=100, break_coef=0.9, ext_multi_ica=8):

        # Usage:

            Newton iteration with multi-level signal extraction, the extraction
            interval is 2^n, n=_ext_multi_ica,...,3,2,1.

        # Parameters:

            X: Mixed signals, which is obtained from the observers.
            max_iter: Maximum number of iteration.
            break_coef: The paramter, which determine when the iteration
                should jump out.
            _ext_multi_ica: The maximum signal extraction interval is  2^_ext_multi_ica

        # Output:

            Estimated source signals matrix S.
        '''
        self.Stack = []
        B1 = self.generate_initial_matrix_B(X)
        B2 = self.multi_level_extraction_newton_iteration(
            X, B1, max_iter, tol, break_coef, ext_multi_ica)
        S2 = np.dot(B2, X)
        return S2


class ComponentDependentICA(FastbssBasic):

    def mixing_matrix_estimation(self, X, ext_initial_matrix):
        '''
        # mixing_matrix_estimation(self, X, ext_initial_matrix):

        # Usage:

            According to the mixed signals observed from the observers, estimate
            a rough mixing matrix, which is used for calculating the intial
            separation matrix B_0.

        # Parameters:

            X: Mixed signals, which is obtained from the observers.
            ext_initial_matrix: The signal extraction interval for mixed signals
                extraction, default value is 0, which means use all the inputed 
                signals.

        # Output:

            Estimated mixing matrix A.
        '''
        m, n = X.shape
        sampling_interval = np.int(ext_initial_matrix)
        _signals = X[:,
                     ::sampling_interval] if sampling_interval else X
        m, n = _signals.shape
        A = np.zeros([m, m])
        indexs_max_abs = np.nanargmax(np.abs(_signals), axis=-2)
        indexs_max_abs_positive = np.where(
            _signals[indexs_max_abs, np.arange(n)] > 0, indexs_max_abs, np.nan)
        for y in range(m):
            selected_indexs = np.argwhere(indexs_max_abs_positive == y)
            if selected_indexs.shape[0] < 5:
                return None
            A[:, [y]] = np.sum(_signals[:, selected_indexs], axis=-2)
        A = np.dot(A, np.diag(1/np.max(A, axis=-1)))
        A = np.clip(A, 0.01, None)
        return A

    def cdica(self, X, max_iter=100, tol=1e-04, ext_initial_matrix=0):
        '''
        # cdica(self, X, max_iter=100, tol=1e-04, ext_initial_matrix=0):

        # Usage:

            Component dependent ICA. 
            It is a combination of initial 
            mixing matrix estimation and original fastica.

        # Parameters:

            X: Mixed signals, which is obtained from the observers.
            max_iter: Maximum number of iteration.
            tol: Tolerance of the convergence of the matrix B 
                calculated from the last iteration and the 
                matrix B calculated from current newton iteration.
            ext_initial_matrix: The signal extraction interval for mixed signals
                extraction, default value is 0, which means use all the inputed 
                signals.

        # Output:

            Estimated source signals matrix S.
        '''
        X, V = self.whiten(X)
        A1 = self.mixing_matrix_estimation(X, ext_initial_matrix)
        B1 = self.generate_initial_matrix_B(V, A1)
        B2 = self.newton_iteration(B1, X, max_iter, tol)[0]
        S2 = np.dot(B2, X)
        return S2


class AdapiveExtractionICA(FastbssBasic):

    def adaptive_extraction_iteration(self, X, B, max_iter, tol, ext_adapt_ica):
        '''
        # adaptive_extraction_iteration(self, X, B, max_iter, tol, _ext_adapt_ica):

        # Usage:

            Adaptive extraction newton iteration.
            It is a combination of several fastica algorithm with different partial
            signals, which is extracted by different intervals. the extraction 
            interval can be detemined by the convergence of the iteration.

        # Parameters:

            X: Mixed signals, which is obtained from the observers.
            max_iter: Maximum number of iteration.
            tol: Tolerance of the convergence of the matrix B 
                calculated from the last iteration and the 
                matrix B calculated from current newton iteration.
            _ext_adapt_ica: The intial and the maximum extraction interval of the 
                input signals.

        # Output:

            Estimated source separation matrix B.
        '''
        _prop_series = np.arange(1, ext_adapt_ica)
        grads_num = _prop_series.shape[0]
        _tols = tol*(_prop_series**0.5)
        _tol = 1
        for i in range(grads_num-1, 0, -1):
            if _tol > _tols[i]:
                _X = X[:, ::np.int(_prop_series[i])]
                _X, V, V_inv = self.whiten_with_inv_V(_X)
                B = self.decorrelation(np.dot(B, V_inv))
                B, _tol = self.newton_iteration(B, _X, max_iter, _tols[i])
                B = np.dot(B, V)
        _X = X
        _X, V, V_inv = self.whiten_with_inv_V(_X)
        B = self.decorrelation(np.dot(B, V_inv))
        B, _tol = self.newton_iteration(B, _X, max_iter, _tols[i])
        B = np.dot(B, V)
        return B

    def aeica(self, X, max_iter=100, tol=1e-04, ext_adapt_ica=50):
        '''
        # aeica(self, X, max_iter=100, tol=1e-04, ext_adapt_ica=30):

        # Usage:

            Adaptive extraction ICA.
            It is a combination of several fastica algorithm with different partial
            signals, which is extracted by different intervals. the extraction 
            interval can be detemined by the convergence of the iteration.
            A original fastica is added at the end, in order to get the best result.

        # Parameters:

            X: Mixed signals, which is obtained from the observers.
            max_iter: Maximum number of iteration.
            tol: Tolerance of the convergence of the matrix B 
                calculated from the last iteration and the 
                matrix B calculated from current newton iteration.
            _ext_adapt_ica: The intial and the maximum extraction interval of the 
                input signals.

        # Output:

            Estimated source signals matrix S.
        '''
        B1 = self.generate_initial_matrix_B(X)
        B2 = self.adaptive_extraction_iteration(
            X, B1, max_iter, tol, ext_adapt_ica)
        S2 = np.dot(B2, X)
        return S2


class UltraFastICA(ComponentDependentICA, AdapiveExtractionICA):

    def ufica(self, X, max_iter=100, tol=1e-04, ext_initial_matrix=0, ext_adapt_ica=100):
        '''
        # ufica(self, X, max_iter=100, tol=1e-04, ext_initial_matrix=0, ext_adapt_ica=100):

        # Usage:

            Ultra-fast ICA.
            It is a combination of CdICA and AeICA. Firstly, CdICA, then, AeICA.

        # Parameters:

            X: Mixed signals, which is obtained from the observers.
            max_iter: Maximum number of iteration.
            tol: Tolerance of the convergence of the matrix B 
                calculated from the last iteration and the 
                matrix B calculated from current newton iteration.
            ext_initial_matrix: The signal extraction interval for mixed signals
                extraction, default value is 0, which means use all the inputed 
                signals.
            _ext_adapt_ica: The intial and the maximum extraction interval of the 
                input signals.

        # Output:

            Estimated source signals matrix S.
        '''
        #X, V = self.whiten(X)
        A1 = self.mixing_matrix_estimation(X, ext_initial_matrix)
        B1 = np.linalg.inv(A1)
        B2 = self.adaptive_extraction_iteration(
            X, B1, max_iter, tol, ext_adapt_ica)
        S2 = np.dot(B2, X)
        return S2


class FastICA(FastbssBasic):

    def newton_iteration_auto_break2(self, B, X, max_iter, break_coef):
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

        # Output:

            B,lim
            B: Separation matrix B.
            lim: Convergence of the iteration.
        '''
        _sum = 0
        _max = 0
        for _ in range(max_iter):
            B, lim = self._iteration(B, X)
            # print("3:",lim)
            self.Stack.append(lim)
            if lim > _max:
                _max = lim
                self.Stack = [lim]
                _sum = 0
            _sum += lim
            if _sum < break_coef*0.5*(self.Stack[0]+self.Stack[-1])*len(self.Stack):
                break
        # print("3:",_)
        return B, lim

    def fastica(self, X, max_iter=100, tol=1e-04):
        '''
        # fastica(self, X, max_iter=100, tol=1e-04):

        # Usage:

            Original FastICA.

        # Parameters:

            B: Separation matrix.
            X: Whitened mixed signals.
            max_iter: Maximum number of iteration.
            tol: Tolerance of the convergence of the matrix B 
                calculated from the last iteration and the 
                matrix B calculated from current newton iteration.

        # Output:

            Estimated source signals matrix S.
        '''
        X, V = self.whiten(X)
        B1 = self.generate_initial_matrix_B(V)
        B2 = self.newton_iteration(B1, X, max_iter, tol)[0]
        S2 = np.dot(B2, X)
        return S2

    def fastica_auto_break(self, X, max_iter=100, break_coef=0.98):
        _X = X
        _X, V = self.whiten(_X)
        B1 = self.generate_initial_matrix_B(V)
        self.Stack = []
        B2 = self.newton_iteration_auto_break2(
            B1, _X, max_iter, break_coef)[0]
        B2 = np.dot(B2, V)
        S2 = np.dot(B2, X)
        return S2


class PyFastbss(MultiLevelExtractionICA, UltraFastICA, FastICA):

    def fastbss(self, method, X, max_iter=100, tol=1e-04, break_coef=0.9, ext_initial_matrix=0, ext_adapt_ica=100, ext_multi_ica=8):
        if method == 'fastica':
            return self.fastica(X, max_iter, tol)
        elif method == 'meica':
            return self.meica(X, max_iter, tol, break_coef, ext_multi_ica)
        elif method == 'cdica':
            return self.cdica(X, max_iter, tol, ext_initial_matrix)
        elif method == 'aeica':
            return self.aeica(X, max_iter, tol, ext_adapt_ica)
        elif method == 'ufica':
            return self.ufica(X, max_iter, tol, ext_initial_matrix, ext_adapt_ica)
        else:
            print('Method Identification Error!')
            return None


# pyfastbss core
pyfbss = PyFastbss()
