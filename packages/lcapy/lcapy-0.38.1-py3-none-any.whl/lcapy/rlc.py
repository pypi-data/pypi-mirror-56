from .oneport import OnePort

class RLC(Oneport):
    pass
    

class RC(Oneport):

    def noisy(self):

        dummy_node = self.dummy_node()

        opts = self.opts.copy()

        rnet = '%s %s %s %s; %s' % (self.defname, 
                                    self.relnodes[0], dummy_node,
                                    arg_format(self.args[0]),
                                    opts)
        
        Vn = 'sqrt(4 * k * T * %s)' % self.args[0]
        vnet = '%sVn%s %s %s noise %s; %s' % (
            self.namespace, self.relname, dummy_node,
            self.relnodes[1], arg_format(Vn), opts)
        return rnet + '\n' + vnet
    
    def stamp(self, mna):

        # L's can also be added with this stamp but if have coupling
        # it is easier to generate a stamp that requires the branch current
        # through the L.
        n1, n2 = self.node_indexes

        if self.type == 'C' and mna.kind == 'dc':
            Y = 0
        else:
            Y = self._cptYselect.expr

        if n1 >= 0 and n2 >= 0:
            mna._G[n1, n2] -= Y
            mna._G[n2, n1] -= Y
        if n1 >= 0:
            mna._G[n1, n1] += Y
        if n2 >= 0:
            mna._G[n2, n2] += Y

        if mna.kind == 'ivp' and self.cpt.hasic:
            I = self.Isc.expr
            if n1 >= 0:
                mna._Is[n1] += I 
            if n2 >= 0:
                mna._Is[n2] -= I               


class R(RC):
    """Resistor"""

    def __init__(self, Rval):

        self.args = (Rval, )
        self._R = cExpr(Rval)
        self._Z = Impedance(self._R)


        
