from hop_B_Manager import hop_B_Manager
from hop_Source_controller import hop_Source_controller
from pyfastbss_core import PyFastbss, pyfbss


class hop_MeICA_newton_iteration:

    def __init__(self,max_iter,tol,break_coef,ext_multi_ica,_X,B_temp) -> None:
        super().__init__()
        self.max_iter=max_iter
        self.tol=tol
        self.break_coef=break_coef
        self.ext_multi_ica=ext_multi_ica
        self.X=_X
        self.B=B_temp

    def meica_newton_iteration_autobreak(self):
    # self.B=pyfbss.multi_level_extraction_newton_iteration(self.X, self.B, self.max_iter, self.tol, self.break_coef, self.ext_multi_ica)
        self.Stack=[]
        _sum = 0
        _max = 0
        for _ in range(self.max_iter):
            self.B, lim = pyfbss._iteration(self.B, self.X)
            self.Stack.append(lim)
            if lim > _max:
                _max = lim
                self.Stack = [lim]
                _sum = 0
            _sum += lim
            if _sum < self.break_coef*0.5*(self.Stack[0]+self.Stack[-1])*len(self.Stack) or self.Stack[-1] < self.tol:
                break
        return self.B,lim

        # return B
    

