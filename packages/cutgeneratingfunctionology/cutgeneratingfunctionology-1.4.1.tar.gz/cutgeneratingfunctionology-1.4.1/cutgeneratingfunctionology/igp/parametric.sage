"""
    sage: import warnings
    sage: warnings.filterwarnings('ignore', 'Matplotlib is building the font cache using fc-list. This may take a moment.')
"""

import sage.structure.element
from sage.structure.element import FieldElement

try:
    from ppl import Variable, Constraint, Linear_Expression, Constraint_System, NNC_Polyhedron, Poly_Con_Relation, Poly_Gen_Relation, Generator, MIP_Problem, point as ppl_point
except ImportError:
    # old Sage
    from sage.libs.ppl import Variable, Constraint, Linear_Expression, Constraint_System, NNC_Polyhedron, Poly_Con_Relation, Poly_Gen_Relation, Generator, MIP_Problem, point as ppl_point

from six.moves import zip
from six.moves import range

from sage.structure.sage_object import SageObject
from sage.structure.richcmp import richcmp, op_LT, op_LE, op_EQ, op_NE, op_GT, op_GE
import time

from cutgeneratingfunctionology.spam.basic_semialgebraic import *
from cutgeneratingfunctionology.spam.polyhedral_complex import PolyhedralComplex

debug_new_factors = False
debug_cell_exceptions = False

###############################
# Parametric Real Number Field
###############################

def richcmp_op_negation(op):
    if op == op_LT:
        return op_GE
    elif op == op_LE:
        return op_GT
    elif op == op_EQ:
        return op_NE
    elif op == op_NE:
        return op_EQ
    elif op == op_GT:
        return op_LE
    elif op == op_GE:
        return op_LT
    else:
        raise ValueError("{} is not a valid richcmp operator".format(op))

def format_richcmp_op(op):
    if op == op_LT:
        return '<'
    elif op == op_LE:
        return '<='
    elif op == op_EQ:
        return '=='
    elif op == op_NE:
        return '!='
    elif op == op_GT:
        return '>'
    elif op == op_GE:
        return '>='
    else:
        raise ValueError("{} is not a valid richcmp operator".format(op))

class ParametricRealFieldElement(FieldElement):
    r"""
    A :class:`ParametricRealFieldElement` stores a symbolic expression of the parameters in the problem and a concrete value, which is the evaluation of this expression on the given parameter tuple.

    When a comparison takes place on elements of the class, their concrete values are compared to compute the Boolean return value of the comparison. The constraint on the parameters that gives the same Boolean return value is recorded.
    """

    def __init__(self, value, symbolic=None, parent=None):
        if parent is None:
            raise ValueError("ParametricRealFieldElement invoked with parent=None. That's asking for trouble")
        FieldElement.__init__(self, parent) ## this is so that canonical_coercion works.
        if not parent._mutable_values and value is not None:
            ## Test coercing the value to RR, so that we do not try to build a ParametricRealFieldElement
            ## from something like a tuple or vector or list or variable of a polynomial ring
            ## or something else that does not make any sense.
            if not isinstance(value, sage.interfaces.mathematica.MathematicaElement):
                RR(value)
            self._val = value
        if symbolic is None:
            self._sym = value # changed to not coerce into SR. -mkoeppe
        else:
            self._sym = symbolic

    def sym(self):
        return self._sym

    def val(self):
        try:
            return self._val
        except AttributeError:
            return self.parent()._eval_factor(self._sym)

    def _richcmp_(left, right, op):
        r"""
        Examples for traditional cmp semantics::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)             # Suppress output in automatic tests.
            sage: K.<f> = ParametricRealField([0], big_cells=False, allow_refinement=True)
            sage: f >= 0
            True
            sage: K._eq
            {f}

        Examples for big_cells semantics::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)             # Suppress output in automatic tests.
            sage: K.<f> = ParametricRealField([0], big_cells=True, allow_refinement=False)
            sage: f >= 0
            True
            sage: K._le
            {-f}
            sage: K.get_le_factor()
            {-f}
            sage: K.get_eq_factor()
            set()
            sage: K.get_lt_factor()
            set()

        Examples for big_cells=True, allow_refinement=True::

            sage: K.<f> = ParametricRealField([1], big_cells=True, allow_refinement=True)
            sage: f >= 0
            True
            sage: K._le
            {-f}
            sage: K.get_le_factor()
            {-f}
            sage: K.get_eq_factor()
            set()
            sage: K.get_lt_factor()
            set()

        """
        if not left.parent() is right.parent():
            # shouldn't really happen, within coercion
            raise TypeError("comparing elements from different fields")
        if left.parent()._big_cells:
            result = richcmp(left.val(), right.val(), op)
            if result:
                true_op = op
            else:
                true_op = richcmp_op_negation(op)
            if true_op == op_LT:
                # left.sym() - right.sym() may cancel denominators, but that is
                # OK because _div_ makes sure that denominators are nonzero.
                left.parent().assume_comparison(left - right, operator.lt)
            elif true_op == op_GT:
                left.parent().assume_comparison(left - right, operator.gt)
            elif true_op == op_EQ:
                left.parent().assume_comparison(left - right, operator.eq)
            elif true_op == op_LE:
                left.parent().assume_comparison(left - right, operator.le)
            elif true_op == op_GE:
                left.parent().assume_comparison(left - right, operator.ge)
            elif true_op == op_NE:
                left.parent().assume_comparison(left - right, operator.ne)
            else:
                raise ValueError("{} is not a valid richcmp operator".format(op))
            return result
        else:
            # Traditional cmp semantics.
            if (left.val() == right.val()):
                left.parent().assume_comparison(left, operator.eq, right)
            elif (left.val() < right.val()):
                left.parent().assume_comparison(left, operator.lt, right)
            else:
                left.parent().assume_comparison(right, operator.lt, left)
            return richcmp(left.val(), right.val(), op)

    def __abs__(self):
        """
        Examples for traditional cmp semantics::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)             # Suppress output in automatic tests.
            sage: K.<f> = ParametricRealField([-1], big_cells=False, allow_refinement=True)
            sage: abs(f) + abs(-f)
            (-2*f)~
            sage: K._lt
            {f}

        Examples for big_cells semantics::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)             # Suppress output in automatic tests.
            sage: K.<f> = ParametricRealField([-1], big_cells=True, allow_refinement=True)
            sage: abs(f) + abs(-f)
            (-2*f)~
            sage: K._lt
            set()
            sage: K._le
            {f}

        """
        preferred_sign = 1
        if self.parent()._big_cells:
            with self.parent().off_the_record():
                if self >= 0:
                    preferred_sign = 1
                else:
                    preferred_sign = -1
        if preferred_sign == 1:
            if self >= 0:
                return self
            else:
                return -self
        else:
            if self <= 0:
                return -self
            else:
                return self

    def sign(self):
        """
        Examples for traditional cmp semantics::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)             # Suppress output in automatic tests.
            sage: K.<f, z> = ParametricRealField([-1, 0], big_cells=False, allow_refinement=True)
            sage: sign(f)
            -1
            sage: sign(z)
            0
            sage: K._lt
            {f}
            sage: K._le
            set()
            sage: K._eq
            {z}

        Test that the same result is obtained in big_cells, allow_refinement=True semantics::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)             # Suppress output in automatic tests.
            sage: K.<f, z> = ParametricRealField([-1, 0], big_cells=True, allow_refinement=True)
            sage: sign(f)
            -1
            sage: sign(z)
            0
            sage: K._lt
            {f}
            sage: K._le
            set()
            sage: K._eq
            {z}

        Test that the same result is obtained for big_cells, allow_refinement=False semantics::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)             # Suppress output in automatic tests.
            sage: K.<f, z> = ParametricRealField([-1, 0], big_cells=True, allow_refinement=False)
            sage: sign(f)
            -1
            sage: sign(z)
            0
            sage: K._lt
            {f}
            sage: K._le
            set()
            sage: K._eq
            {z}
        """
        if self.parent()._big_cells:
            preferred_sign = sign(self.val())    # off the record
        else:
            preferred_sign = 1
        if preferred_sign == 1:
            if self > 0:
                return 1
        elif preferred_sign == -1:
            if self < 0:
                return -1
        else:
            if self == 0:
                return 0
        if self > 0:
            return 1
        elif self < 0:
            return -1
        else:
            return 0

    def floor(self):
        result = floor(self.val())
        result <= self < result + 1
        return result

    def ceil(self):
        result = ceil(self.val())
        result - 1 < self <= result
        return result

    def __float__(self):
        if self.parent().allow_coercion_to_float:
            return float(self.val())
        else:
            raise ValueError("Conversion to float is not allowed")

    def _repr_(self):
        s = self._sym
        r = repr(s)
        if s in RR:
            return r
        if len(r) > 1:
            return '('+r+')~'
        else:
            return r+'~'

    def _latex_(self):
        return "%s" % (latex(self._sym))

    def _add_(self, other):
        if not isinstance(other, ParametricRealFieldElement):
            other = ParametricRealFieldElement(other, parent=self.parent())
        try:
            val = self._val + other._val
        except AttributeError:
            val = None
        return ParametricRealFieldElement(val, self._sym + other._sym, parent=self.parent())

    def _sub_(self, other):
        if not isinstance(other, ParametricRealFieldElement):
            other = ParametricRealFieldElement(other, parent=self.parent())
        try:
            val = self._val - other._val
        except AttributeError:
            val = None
        return ParametricRealFieldElement(val, self._sym - other._sym, parent=self.parent())

    def __neg__(self):
        try:
            val = -self.val()
        except AttributeError:
            val = None
        return ParametricRealFieldElement(val, -self._sym, parent=self.parent())

    def _mul_(self, other):
        if not isinstance(other, ParametricRealFieldElement):
            try:
                other = ParametricRealFieldElement(other, parent=self.parent())
            except TypeError:
                # For example when other is a vector
                return other * self
        try:
            val = self.val() * other.val()
        except AttributeError:
            val = None
        return ParametricRealFieldElement(val, self._sym * other._sym, parent=self.parent())

    def _div_(self, other):
        r"""
        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)             # Suppress output in automatic tests.
            sage: K.<f> = ParametricRealField([0])
            sage: 1 / f
            Traceback (most recent call last):
            ...
            ZeroDivisionError: Division by 0 in ParametricRealField
            sage: f / f
            Traceback (most recent call last):
            ...
            ZeroDivisionError: Division by 0 in ParametricRealField
        """
        if not isinstance(other, ParametricRealFieldElement):
            other = ParametricRealFieldElement(other, parent=self.parent())
        if other == 0:
            raise ZeroDivisionError("Division by 0 in ParametricRealField")
        try:
            val = self.val() / other.val()
        except AttributeError:
            val = None
        return ParametricRealFieldElement(val, self._sym / other._sym, parent=self.parent())

    def __hash__(self):
        r"""
        The hash function of these elements must be so that 
        elements that would compare equal have the same hash value. 

        The constant hash function would do the job.  Instead we use the
        hash of the .val() (because equality implies equality of _val).
        It is not correct to use the hash of the ._sym, or to compare
        the __repr__, because then the user could check for equality
        (for example, by testing the cardinality of a set, as in the
        tests below) without the equality being recorded in the field.

        The correctness of this implementation depends on the guarantee
        of equal _val elements having the same hash value.  If in
        doubt, make sure that the _val elements all come from the same
        field, by ``nice_field_values``.

        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)             # Suppress output in automatic tests.
            sage: K.<f> = ParametricRealField([1])
            sage: s = {f, K(1)}
            sage: len(s)
            1
            sage: K._eq
            {f - 1}
            sage: K.<f> = ParametricRealField([1])
            sage: s = {f, K(2)}
            sage: len(s)
            2
        """
        return hash(self.val())

def is_parametric_element(x):
    # We avoid using isinstance here so that this is robust even if parametric.sage is reloaded.
    # For example, apparently in the test suite.
    return hasattr(x, '_sym')

from sage.rings.ring import Field
import sage.rings.number_field.number_field_base as number_field_base
from sage.structure.coerce_maps import CallableConvertMap


class ParametricRealFieldFrozenError(ValueError):
    pass

class ParametricRealFieldInconsistencyError(ValueError):
    pass

class ParametricRealFieldRefinementError(ValueError):
    pass

from contextlib import contextmanager

class FactorUndetermined(Exception):
    pass

allow_refinement_default = True
big_cells_default = 'if_not_allow_refinement'
mutable_values_default = False

class ParametricRealField(Field):
    r"""
    A Metaprogramming trick for parameter space analysis.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: logging.disable(logging.INFO)             # Suppress output in automatic tests.
        sage: K.<f> = ParametricRealField([4/5])
        sage: h = gmic(f, field=K)
        sage: I_list = J_list = h.intervals()
        sage: K_list = I_list + [ (a+1, b+1) for (a, b) in h.intervals() ]
        sage: _ = [ verts(I, J, KK) for I in I_list for J in J_list for KK in K_list ]
        sage: K.get_eq()
        set()
        sage: R = f._sym.parent().ring()
        sage: sorted([ p for p in K.get_lt() if p in R ])   # filter out the rational function 1/(f^2 - f), which is normalized differently starting Sage 8.4b2
        [-2*f, -2*f + 1, -f - 1, -f, f - 2, f - 1, 2*f - 2]
        sage: K.get_eq_factor()
        set()
        sage: K.get_lt_factor()
        {-f, -f + 1/2, f - 1}

        sage: K.<f, lam> = ParametricRealField([4/5, 1/6])
        sage: h = gj_2_slope(f, lam, field=K)
        sage: K.get_lt()
        {(-1/2)/(-1/2*f^2*lam - 1/2*f^2 + f*lam + 1/2*f - 1/2*lam),
         (-f*lam - f + lam)/(-f + 1),
         -lam,
         lam - 1,
         -f,
         f - 1,
         -1/2*f*lam - 1/2*f + 1/2*lam,
         f*lam - lam}
        sage: K.get_lt_factor()
        {-lam, lam - 1, -f, f - 1, -f*lam - f + lam}

        sage: K.<f,alpha> = ParametricRealField([4/5, 3/10])
        sage: h=dg_2_step_mir(f, alpha, field=K, conditioncheck=False)
        sage: extremality_test(h)
        True

        sage: K.<f,a1,a2,a3> = ParametricRealField([4/5, 1, 3/10, 2/25])
        sage: h = kf_n_step_mir(f, (a1, a2, a3), conditioncheck=False)
        sage: extremality_test(h)
        True

        sage: K.<f> = ParametricRealField([1/5])
        sage: h = drlm_3_slope_limit(f, conditioncheck=False)
        sage: extremality_test(h)
        True
        sage: K.get_lt_factor()
        {-f, f - 1, f - 1/2, f - 1/3}

    Elements coerce to RDF, RR, float to enable plotting of functions::

        sage: K.<f> = ParametricRealField([4/5])
        sage: RDF(f)
        0.8
        sage: RR(f)
        0.800000000000000
        sage: float(f)
        0.8
        sage: 0.2 - f
        -0.600000000000000

    Plotting will show symbolic labels on the axes::

        sage: plot_with_colored_slopes(gmic(f))
        Graphics object...

    But they do not coerce or convert into any exact fields::

        sage: QQ(f)
        Traceback (most recent call last):
        ...
        TypeError: unable to convert f~ to a rational
        sage: AA(f)
        Traceback (most recent call last):
        ...
        TypeError: Illegal initializer for algebraic number

    Test that values can also be initialized by vectors (internally we make it tuples)::

        sage: f = vector(QQ, [1, 2])
        sage: K.<f0, f1> = ParametricRealField(f)
        sage: f = vector(f0.parent(), [f0, f1]); f
        ((f0)~, (f1)~)
        sage: f.parent()
        Vector space of dimension 2 over ParametricRealField(names = ['f0', 'f1'], values = [1, 2])
        sage: f[0]*f[1] <= 4
        True

    Test-point free mode (limited functionality and MUCH slower because of many more polynoial
    evaluations via libsingular)::

        sage: K.<a, b> = ParametricRealField(None, mutable_values=True)
        sage: a <= 2
        Traceback (most recent call last):
        ...
        FactorUndetermined: a cannot be evaluated because the test point is not complete
        sage: K.assume_comparison(a.sym(), operator.le, 3)

    Partial test point mode::

        sage: K.<a, b> = ParametricRealField([None, 1], mutable_values=True)
        sage: a <= 2
        Traceback (most recent call last):
        ...
        FactorUndetermined: a cannot be evaluated because the test point is not complete
        sage: b <= 11
        True

    """
    Element = ParametricRealFieldElement

    def __init__(self, values=None, names=(), allow_coercion_to_float=True,
                 mutable_values=None, allow_refinement=None, big_cells=None, base_ring=QQ):
        Field.__init__(self, self)

        if mutable_values is None:
            mutable_values = mutable_values_default
        if allow_refinement is None:
            allow_refinement = allow_refinement_default
        if big_cells is None:
            big_cells = big_cells_default

        if big_cells == 'if_not_allow_refinement':
            big_cells = not allow_refinement
        if mutable_values == 'if_big_cells':
            mutable_values = big_cells

        assert isinstance(allow_refinement, bool)
        assert isinstance(mutable_values, bool)
        assert isinstance(big_cells, bool)

        if not allow_refinement and not big_cells:
            raise ValueError("if allow_refinement=False, must have big_cells=True")

        self._allow_refinement = allow_refinement
        self._mutable_values = mutable_values
        self._big_cells = big_cells

        self._zero_element = ParametricRealFieldElement(0, parent=self)
        self._one_element =  ParametricRealFieldElement(1, parent=self)
        ## REFACTOR: Maybe replace this by an instance of BasicSemialgebraicSet_eq_lt_le_sets - but careful - this class right now assumes polynomials
        self._eq = set([])
        self._lt = set([])
        self._le = set([])
        #sym_ring = PolynomialRing(base_ring, names, implementation='generic')
        sym_ring = PolynomialRing(base_ring, names)
        self._factor_bsa = BasicSemialgebraicSet_eq_lt_le_sets(poly_ring=sym_ring)
        self._sym_field = sym_ring.fraction_field()
        if values is None:
            values = [ None for n in names ]
        else:
            assert len(values) == len(names)
        vnames = self._sym_field.gens()
        self._gens = [ ParametricRealFieldElement(value, name, parent=self) for (value, name) in zip(values, vnames) ]
        self._names = tuple(names)
        if mutable_values:
            self._values = list(values)
        else:
            self._values = tuple(values)

        self._frozen = False
        self._record = True

        # do the computation of the polyhedron incrementally,
        # rather than first building a huge list and then in a second step processing it.
        # the upstairs polyhedron defined by all constraints in self._eq/lt_factor
        self._polyhedron = BasicSemialgebraicSet_polyhedral_ppl_NNC_Polyhedron(0)
        # monomial_list records the monomials that appear in self._eq/lt_factor.
        # v_dict is a dictionary that maps each monomial to the index of its corresponding Variable in self._polyhedron
        self._bsa = BasicSemialgebraicSet_veronese(self._polyhedron, monomial_list=[], v_dict={})

        self.allow_coercion_to_float = allow_coercion_to_float
        if allow_coercion_to_float:
            RDF.register_coercion(sage.structure.coerce_maps.CallableConvertMap(self, RDF, lambda x: RDF(x.val()), parent_as_first_arg=False))
            RR.register_coercion(sage.structure.coerce_maps.CallableConvertMap(self, RR, lambda x: RR(x.val()), parent_as_first_arg=False))
        logging.info("Initialized {}".format(self))

    def __copy__(self):
        logging.warning("copy(%s) is invoked" % self)
        Kcopy = self.__class__(self._values, self._names)
        Kcopy._eq.update(self._eq)
        Kcopy._lt.update(self._lt)
        Kcopy._le.update(self._le)
        Kcopy._factor_bsa = copy(self._factor_bsa)
        return Kcopy

    def ppl_polyhedron(self):
        return self._polyhedron._polyhedron

    def monomial_list(self):
        return self._bsa.monomial_list()

    def v_dict(self):
        return self._bsa.v_dict()

    def _first_ngens(self, n):
        for i in range(n):
            yield self._gens[i]
    def ngens(self):
        return len(self._gens)
    def _an_element_impl(self):
        return ParametricRealFieldElement(1, parent=self)
    def _coerce_map_from_(self, S):
        """
        TESTS:

        Test that elements of different ``ParametricRealField``s have no coercion.

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)             # Suppress output in automatic tests.
            sage: K.<a> = ParametricRealField([0])
            sage: L.<b> = ParametricRealField([1])
            sage: a + b
            Traceback (most recent call last):
            ...
            TypeError: unsupported operand parent(s)...

        Test that real number field elements can be upgraded to ``ParametricRealFieldElement``s.
        Note that this requires setting up the ParametricRealField with a specific base ring, 
        because there is no common parent of QQ(x) and a RealNumberField``::

            sage: sqrt2, = nice_field_values([sqrt(2)])
            sage: K.<f> = ParametricRealField([0], base_ring=sqrt2.parent())
            sage: f + sqrt2
            (f + 1.414213562373095?)~

        This currently does not work for Sage's built-in embedded number field elements...
        """
        if isinstance(S, ParametricRealField) and self is not S:
            return None
        if  S is sage.interfaces.mathematica.MathematicaElement or isinstance(S, RealNumberField_absolute) or isinstance(S, RealNumberField_quadratic) or AA.has_coerce_map_from(S):
            # Does the test with MathematicaElement actually work?
            # We test whether S coerces into AA. This rules out inexact fields such as RDF.
            return CallableConvertMap(S, self, lambda s: ParametricRealFieldElement(s, parent=self), parent_as_first_arg=False)
    def __repr__(self):
        return 'ParametricRealField(names = {}, values = {})'.format(list(self._names), list(self._values))
    def _element_constructor_(self, elt):
        if parent(elt) == self:
            return elt
        try: 
            QQ_elt = QQ(elt)
            return ParametricRealFieldElement(QQ_elt, parent=self)
            #return self.element_class(self, QQ_elt)
        except ValueError:
            raise TypeError("ParametricRealField called with element %s" % elt)

    def _coerce_impl(self, x):
        return self._element_constructor_(x)

    def freeze(self):
        self._frozen = True

    def unfreeze(self):
        self._frozen = False

    @contextmanager
    def frozen(self):
        was_frozen = self._frozen
        self._frozen = True
        try:
            yield True
        finally:
            self._frozen = was_frozen

    @contextmanager
    def unfrozen(self):
        was_frozen = self._frozen
        self._frozen = False
        try:
            yield True
        finally:
            self._frozen = was_frozen

    ## def wallcross_to_lt(self, comparison):
    ##     record_to_lt(self, comparison)
    ##     ..... compute new testpoint, error if fail.

    def is_point_consistent(self, new_values):
        """
        Check whether ``new_values`` satisfies all recorded assumptions.
        """
        if new_values is None:
            return True
        if any(x is None for x in new_values):
            if all(x is None for x in new_values):
                return True
            logging.warning("Consistency checking not implemented if some test point coordinates are None")
            return True
        ### Check that values satisfy all constraints.
        return [ m(new_values) for m in self.monomial_list() ] in self._polyhedron

    def change_values(self, **values):
        if not self._mutable_values:
            raise ValueError("ParametricRealField is set up with mutable_values=False")
        new_values = copy(self._values)
        for key, value in values.items():
            new_values[self._names.index(key)] = value
        ### Check that values satisfy all constraints.
        if not self.is_point_consistent(new_values):
            raise ParametricRealFieldInconsistencyError("New test point {} does not satisfy the recorded constraints".format(new_values))
        self._values = new_values

    def remove_test_point(self):
        """
        Switch ``self`` to test-point free mode.

        This requires a ParametricRealField set up with ``mutable_values=True``.

        Not many things are implemented in this mode::

        EXAMPLE::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)             # Suppress output in automatic tests.
            sage: K.<a,b> = ParametricRealField([4, 1], big_cells=True, mutable_values=True, allow_refinement=False)
            sage: with K.changed_values():
            ....:     K.remove_test_point()
            ....:     with K.temporary_assumptions():
            ....:         K.assume_comparison(a.sym(), operator.le, 3)
            ....:         a <= 4
            Traceback (most recent call last):
            ...
            FactorUndetermined: a cannot be evaluated because the test point is not complete...
        """
        self._values = [ None for n in self._names ]

    @contextmanager
    def removed_test_point(self):
        """
        Context manager for temporarily switching to test-point free mode.

        This requires a ParametricRealField set up with ``mutable_values=True``.

        EXAMPLE::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)             # Suppress output in automatic tests.
            sage: K.<a> = ParametricRealField([4], big_cells=True, mutable_values=True, allow_refinement=False)
            sage: with K.removed_test_point():
            ....:     with K.temporary_assumptions():
            ....:         K.assume_comparison(a.sym(), operator.le, 3)
            ....:         K.find_test_point()
            ....:         with K.frozen():
            ....:             a <= 4
            True
        """
        with self.changed_values():
            self.remove_test_point()
            yield True

    def find_test_point(self):
        """
        Sets a new test point that is consistent with the recorded constraints.

        This can fail with ``NotImplementedError'' or ``ParametricRealFieldInconsistencyError''.

        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)             # Suppress output in automatic tests.
            sage: K.<x,y,z> = ParametricRealField([1, 2, 3], mutable_values=True, big_cells=True, allow_refinement=False)
            sage: assert 0 <= x <= y <= z <= 6
            sage: K.remove_test_point()
            sage: K.find_test_point()
            sage: x.val(), y.val(), z.val()
            (3/2, 3, 9/2)

            sage: K.<x,y,z> = ParametricRealField(mutable_values=True, big_cells=True, allow_refinement=False)
            sage: K.assume_comparison(0, operator.le, x.sym())
            sage: K.assume_comparison(x.sym(), operator.le, y.sym())
            sage: K.assume_comparison(y.sym(), operator.le, z.sym())
            sage: K.assume_comparison(z.sym(), operator.le, 4)
            sage: K.find_test_point()
            sage: x.val(), y.val(), z.val()
            (1, 2, 3)
        """
        p = self._polyhedron.find_point()
        self.change_values(**{str(m): x for m, x in zip(self.monomial_list(), p) })

    @contextmanager
    def changed_values(self, **values):
        """
        Context manager for temporarily switching to another consistent test point.

        This requires setting up the field with ``mutable_values=True``.

        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)             # Suppress output in automatic tests.
            sage: K.<f> = ParametricRealField([4/5], mutable_values=True)
            sage: 0 <= f <= 1
            True
            sage: with K.changed_values(f=1/5):
            ....:     assert f <= 1/2
            Traceback (most recent call last):
            ...
            ParametricRealFieldInconsistencyError: Old test point... does not satisfy the recorded constraints
        """
        save_values = self._values
        try:
            self.change_values(**values)
            yield True
        finally:
            self._values = save_values
            if not self.is_point_consistent(save_values):
                raise ParametricRealFieldInconsistencyError("Old test point {} does not satisfy the recorded constraints".format(save_values))

    @contextmanager
    def off_the_record(self):
        was_recording = self._record
        self._record = False
        try:
            yield True
        finally:
            self._record = was_recording

    @contextmanager
    def temporary_assumptions(self, case_id=None):
        if case_id is not None:
            logging.info("Entering case {}.".format(case_id))
        save_eq = self._eq
        self._eq = copy(save_eq)
        save_lt = self._lt
        self._lt = copy(save_lt)
        save_le = self._le
        self._le = copy(save_le)
        save_factor_bsa = self._factor_bsa
        self._factor_bsa = copy(save_factor_bsa)
        save_polyhedron = self._polyhedron
        self._polyhedron = copy(save_polyhedron)
        save_bsa = self._bsa
        self._bsa = copy(self._bsa)
        try:
            yield True
        finally:
            self._eq = save_eq
            self._lt = save_lt
            self._le = save_le
            self._factor_bsa = save_factor_bsa
            self._polyhedron = save_polyhedron
            self._bsa = save_bsa
            if case_id is not None:
                logging.info("Finished case {}.".format(case_id))

    def get_eq(self):
        return self._eq
    def get_lt(self):
        return self._lt
    def get_le(self):
        return self._le

    def get_eq_factor(self):
        return self._factor_bsa.eq_poly()
    def get_lt_factor(self):
        return self._factor_bsa.lt_poly()
    def get_le_factor(self):
        return self._factor_bsa.le_poly()

    def _eval_factor(self, fac):
        """
        Evaluate ``fac`` on the test point.

        If there is no test point or the test point has some ``None`` coordinates
        that are needed for the evaluation, raise ``FactorUndetermined``.
        """
        base_ring = self._sym_field.base_ring()
        if fac in base_ring:
            return base_ring(fac)
        if self._values is not None and not all(x is None for x in self._values):
            try:
                return fac(self._values)
            except TypeError:             # 'None' components
                pass
        raise FactorUndetermined("{} cannot be evaluated because the test point is not complete".format(fac))

    def _factor_sign(self, fac):
        """
        Determine the sign of ``fac`` evaluated on the test point.

        If there is no test point or the test point has some ``None`` coordinates
        that are needed for the evaluation, raise ``FactorUndetermined``.
        """
        return sign(self._eval_factor(fac))

    def assume_comparison(self, lhs, op, rhs=0):
        r"""
        Record the assumption ``lhs op rhs``.

        If this assumption is not satisfied by the current test point,
        a ``ParametricRealFieldInconsistencyError`` is raised.

        ``lhs`` and ``rhs`` should be elements of ``self._sym_field``
        or be parametric elements (elements of ``self``).

        TESTS for consistency checks::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)
            sage: K.<f> = ParametricRealField([4/5])
            sage: K.assume_comparison(f.sym(), operator.gt, 1)
            Traceback (most recent call last):
            ...
            ParametricRealFieldInconsistencyError: New constraint...
            sage: K.assume_comparison(K(0).sym(), operator.gt, 1)
            Traceback (most recent call last):
            ...
            ParametricRealFieldInconsistencyError: New constant constraint...

        TESTS for consistency checks when testpoint values is None::

            sage: K.<a,b> = ParametricRealField([2, 1], big_cells=True, mutable_values=True, allow_refinement=False)
            sage: assert b>0
            sage: K.remove_test_point()
            sage: K.assume_comparison(b.sym(), operator.lt, 0)
            Traceback (most recent call last):
            ...
            ParametricRealFieldInconsistencyError...

        User code should not rely on whether assumptions regarding
        the nonvanishing of denominators are recorded::

            sage: K.<f> = ParametricRealField([4/5])
            sage: assert f < 1
            sage: K.freeze()
            sage: K.assume_comparison(1/f.sym(), operator.gt, 1)   # not tested

        Therefore, also the implicit cancellation in the field of rational
        functions does not change semantics when we transform lhs op rhs
        to lhs - rhs op 0::

            sage: K.<f> = ParametricRealField([4/5])
            sage: K.freeze()
            sage: K.assume_comparison(1/f.sym(), operator.eq, 1/f.sym())

        User code should call assume_comparison only for operands that do
        not have vanishing denominators.

            sage: K.<f> = ParametricRealField([4/5])
            sage: assert 0 < f < 1
            sage: K.freeze()
            sage: K.assume_comparison(1/f.sym(), operator.gt, 1)

        TEST that parametric elements are allowed::

            sage: K.<f> = ParametricRealField([4/5])
            sage: K.assume_comparison(f, operator.le, 1)
            sage: K.get_le_factor()
            {f - 1}

        TESTS for allow_refinement=True:

        Strict inequalities - even-multiplicity factors do matter::

            sage: K.<f> = ParametricRealField([4/5])
            sage: K.freeze()
            sage: f^2 > 0
            Traceback (most recent call last):
            ...
            ParametricRealFieldFrozenError...

        Weak inequalities::

            sage: K.<f> = ParametricRealField([4/5], big_cells=True)
            sage: f >= 4/5
            True
            sage: K.freeze()
            sage: f == 4/5
            Traceback (most recent call last):
            ...
            ParametricRealFieldFrozenError...

            sage: K.<f> = ParametricRealField([4/5], big_cells=True)
            sage: f <= 4/5
            True
            sage: K.freeze()
            sage: f == 4/5
            Traceback (most recent call last):
            ...
            ParametricRealFieldFrozenError...

        TESTS for allow_refinement=False:

        Strict inequalities::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)
            sage: K.<f> = ParametricRealField([4/5], allow_refinement=False)
            sage: f * (1 - f) > 0
            Traceback (most recent call last):
            ...
            ParametricRealFieldRefinementError...
            sage: K.<f> = ParametricRealField([4/5], allow_refinement=False)
            sage: f > 0
            True
            sage: 1 - f > 0
            True

        Strict inequalities - even-multiplicity factors do matter::

            sage: K.<f> = ParametricRealField([4/5], allow_refinement=False)
            sage: f^2 > 0
            Traceback (most recent call last):
            ...
            ParametricRealFieldRefinementError...


        Equalities::

            sage: K.<f> = ParametricRealField([4/5], allow_refinement=False)
            sage: f * (f - 4/5) == 0
            Traceback (most recent call last):
            ...
            ParametricRealFieldRefinementError...
            sage: f == 4/5
            True
            sage: f * (f - 4/5) == 0
            True

            sage: K.<f> = ParametricRealField([4], allow_refinement=False)
            sage: f >= 3
            True
            sage: f * (f - 1) * (f - 2) * (f - 4) == 0
            True

        Weak inequalities::

            sage: K.<f> = ParametricRealField([4/5], allow_refinement=False)
            sage: f * (f - 4/5) >= 0
            Traceback (most recent call last):
            ...
            ParametricRealFieldRefinementError...
            sage: f == 4/5
            True
            sage: f * (f - 4/5) >= 0
            True

            sage: K.<x,y> = ParametricRealField([2, 3], allow_refinement=False)
            sage: x >= 2
            True
            sage: x^2 * (x - 1) * y >= 0
            True

        Weak inequalities - Even-multiplicity factors do matter::

            sage: K.<o> = ParametricRealField([0], allow_refinement=False)
            sage: o^2 <= 0
            True
            sage: K.freeze()
            sage: o == 0
            True

            sage: K.<x> = ParametricRealField([0], allow_refinement=False)
            sage: x^2 >= 0
            True
            sage: K.freeze()
            sage: x == 0
            Traceback (most recent call last):
            ...
            ParametricRealFieldFrozenError...

            sage: K.<f> = ParametricRealField([2], allow_refinement=False)
            sage: f^2 * (1 - f) <= 0    # disjunction 0 union [1, oo).
            Traceback (most recent call last):
            ...
            ParametricRealFieldRefinementError...

        Not-equal::

            sage: K.<x> = ParametricRealField([1], allow_refinement=False)
            sage: x != 0
            Traceback (most recent call last):
            ...
            ParametricRealFieldRefinementError...
            sage: x >= 0
            True
            sage: x != 0
            True

            sage: K.<x> = ParametricRealField([-1], allow_refinement=False)
            sage: x <= 0
            True
            sage: x != 0
            True
        """
        if not self._record:
            return
        if op == operator.gt:
            op = operator.lt
            lhs, rhs = rhs, lhs
        elif op == operator.ge:
            op = operator.le
            lhs, rhs = rhs, lhs
        elif op == operator.ne:
            op = operator.lt
            lhs = - (lhs - rhs) ** 2
            rhs = 0
        comparison = lhs - rhs
        # FIXME: The line above may cancel denominators.  If assume_comparison is called from _richcmp_, that's fine because
        # _div_ records denominators.
        ### Caching via self._eq, _lt, _le
        if is_parametric_element(comparison):
            comparison_sym = comparison.sym()
        else:
            comparison_sym = comparison
        if op == operator.eq:
            if (comparison_sym in self._eq) or (-comparison_sym in self._eq):
                return
        elif op == operator.lt:
            if comparison_sym in self._lt:
                return
        elif op == operator.le:
            if comparison_sym in self._le:
                return
        ### Test consistency with test point
        base_ring = self._sym_field.base_ring()
        if is_parametric_element(comparison):
            # Fast path: Use the precomputed val
            try:
                comparison_val = comparison.val()
            except FactorUndetermined:
                comparison_val = None
            comparison = comparison.sym()
        else:
            comparison = self._sym_field(comparison)
            try:
                comparison_val = self._eval_factor(comparison)
            except FactorUndetermined:
                comparison_val = None
        if comparison_val is not None:
            if not op(comparison_val, 0):
                if comparison in base_ring:
                    raise ParametricRealFieldInconsistencyError("New constant constraint {} {} {} is not satisfied".format(lhs, op, rhs))
                else:
                    raise ParametricRealFieldInconsistencyError("New constraint {} {}  {} is not satisfied by the test point".format(lhs, op, rhs))
        if comparison in base_ring:
            return
        if comparison.denominator() == 1 and comparison.numerator().degree() == 1:
            # Fast path for linear
            numerator = comparison.numerator()
            # We use two different normalizations for the univariate and the multivariate case,
            # just to match the behavior of factor() for the doctests.
            if self.ngens() == 1:
                unit = abs(comparison.numerator().lc())
            else:
                the_lcm = lcm([coeff.denominator() for coeff in numerator.coefficients()])
                numerator *= the_lcm
                unit = 1
            factors = Factorization([(numerator / unit, 1)], unit=unit)
            #import pdb;  pdb.set_trace()
        else:
            factors = comparison.factor()
        if op in (operator.eq, operator.le):
            for (fac, d) in factors:
                if d > 0:
                    if self.is_factor_known(fac, operator.eq):
                    # Comparison is already known true, nothing to record.
                        return
        if len(factors) == 1 and comparison_val is not None:
            the_fac, d = factors[0]
            the_sign = sign(factors.unit() * comparison_val) 
            def factor_sign(fac):
                if fac == the_fac:
                    return the_sign
                else:
                    return self._factor_sign(fac)
        else:
            factor_sign = self._factor_sign
        unit_sign = base_ring(factors.unit()).sign()
        if op == operator.eq:
            eq_factors = []
            ne_factors = []
            unknown_factors = []
            # Record all factors for which testpoint gives zero.
            for (fac, d) in factors: #only one of -fac and fac is in the factorization.
                if d > 0:
                    if self.is_factor_known(fac, operator.lt) or self.is_factor_known(-fac, operator.lt):
                        pass
                    else:
                        try:
                            fac_sign = factor_sign(fac)
                            if fac_sign == 0:
                                eq_factors.append(fac) # cannot happen that -fac was in.
                            else:
                                ne_factors.append(fac)
                        except FactorUndetermined:
                            unknown_factors.append(fac)
            assert len(eq_factors + unknown_factors) > 0
            if self._allow_refinement:
                # Record all factors for which testpoint gives zero.
                for fac in eq_factors:
                    self.record_factor(fac, operator.eq)
            else:
                all_factors = eq_factors + ne_factors + unknown_factors
                if len(all_factors) > 1:
                    raise ParametricRealFieldRefinementError("{} == 0 has several new factors: {}".format(comparison, all_factors))
                self.record_factor(all_factors[0], op)
            logging.debug("New element in %s._eq: %s" % (repr(self), comparison))
            self._eq.add(comparison)
        elif op == operator.lt:
            lt_factors = []
            even_factors = []
            unknown_factors = []
            for (fac, d) in factors: #only one of -fac and fac is in the factorization.
                if self.is_factor_known(fac, operator.eq):
                    raise ParametricRealFieldInconsistencyError("New constraint {} {} {} is not satisfied".format(lhs, op, rhs))
                if d % 2 == 1:
                    if self.is_factor_known(fac, operator.lt):
                        unit_sign = -unit_sign
                    elif self.is_factor_known(-fac, operator.lt):
                        pass
                    else:
                        try:
                            fac_sign = factor_sign(fac)
                            if fac_sign == -1:
                                lt_factors.append(fac)
                                unit_sign = -unit_sign
                            elif fac_sign == +1:
                                lt_factors.append(-fac)
                            else:
                                # assert fac_sign == 0
                                raise ParametricRealFieldInconsistencyError("New constraint {} {} {} is not satisfied".format(lhs, op, rhs))
                        except FactorUndetermined:
                            unknown_factors.append(fac)
                else:
                    if not self.is_factor_known(fac, operator.lt) and not self.is_factor_known(-fac, operator.lt):
                        even_factors.append(fac)
            if (unit_sign == 1) and (not even_factors) and (not unknown_factors):
                raise ParametricRealFieldInconsistencyError("New constraint {} {} {} is not satisfied".format(lhs, op, rhs))
            if not self._allow_refinement:
                if len(lt_factors) + len(unknown_factors) > 1:
                    # or just record the product
                    raise ParametricRealFieldRefinementError("{} < 0 has several new factors: {}".format(comparison, lt_factors))
            for new_fac in lt_factors:
                self.record_factor(new_fac, op)
            if len(unknown_factors) > 1:
                raise NotImplementedError()
            if unknown_factors:
                if unit_sign > 0:
                    self.record_factor(unknown_factors[0], op)
                elif unit_sign < 0:
                    self.record_factor(-unknown_factors[0], op)
            for new_fac in even_factors:
                if not self._allow_refinement:
                    if self.is_factor_known(new_fac, operator.le):
                        self.record_factor(new_fac, operator.lt)
                    elif self.is_factor_known(-new_fac, operator.le):
                        self.record_factor(-new_fac, operator.lt)
                    else:
                        raise ParametricRealFieldRefinementError("{} < 0 has factor {} != 0".format(comparison, new_fac))
                else:
                    try:
                        fac_sign = factor_sign(new_fac)
                        if fac_sign == -1:
                            self.record_factor(new_fac, operator.lt)
                        elif fac_sign == 1:
                            self.record_factor(-new_fac, operator.lt)
                        else:
                            #assert fac_sign == 0
                            raise ParametricRealFieldInconsistencyError("New constraint {} {} {} is not satisfied".format(lhs, op, rhs))
                    except FactorUndetermined:
                        # break the cell ? raise NotImplementedError()?
                        self.record_factor(new_fac, operator.lt)
            logging.debug("New element in %s._lt: %s" % (repr(self), comparison))
            self._lt.add(comparison)
        elif op == operator.le:
            lt_factors = []
            eq_factors = []
            even_factors = []
            unknown_factors = []
            for (fac, d) in factors: #only one of -fac and fac is in the factorization.
                # self.is_factor_known(fac, operator.eq) or self.is_factor_known(-fac, operator.eq) were treated above already.
                if d % 2 == 1:
                    if self.is_factor_known(fac, operator.lt):
                        unit_sign = -unit_sign
                    elif self.is_factor_known(-fac, operator.lt):
                        pass
                    else:
                        try:
                            fac_sign = factor_sign(fac)
                            if fac_sign == 0:
                                eq_factors.append(fac) # cannot happen that -fac was in.
                            elif fac_sign == -1:
                                lt_factors.append(fac)
                                unit_sign = -unit_sign
                            else:
                                assert fac_sign == +1
                                lt_factors.append(-fac)
                        except FactorUndetermined:
                            unknown_factors.append(fac)
                else:
                    if not self.is_factor_known(fac, operator.lt) and not self.is_factor_known(-fac, operator.lt):
                        even_factors.append(fac)
            if (unit_sign == 1) and (not even_factors) and (not eq_factors) and (not unknown_factors):
                raise ParametricRealFieldInconsistencyError("New constraint {} {} {} is not satisfied".format(lhs, op, rhs))
            if not self._allow_refinement:
                if len(even_factors) + len(lt_factors) + len(eq_factors) + len(unknown_factors) > 1:
                    raise ParametricRealFieldRefinementError("{} <= 0 has several new factors: {}".format(comparison, even_factors+lt_factors+eq_factors))
                if even_factors:
                    if unit_sign > 0:
                        try:
                            assert factor_sign(even_factors[0]) == 0
                        except FactorUndetermined:
                            pass
                        self.record_factor(even_factors[0], operator.eq)
                if lt_factors:
                    self.record_factor(lt_factors[0], op)
                if eq_factors:
                    if unit_sign > 0:
                        self.record_factor(eq_factors[0], op)
                    elif unit_sign < 0:
                        self.record_factor(-eq_factors[0], op)
                if unknown_factors:
                    if unit_sign > 0:
                        self.record_factor(unknown_factors[0], op)
                    elif unit_sign < 0:
                        self.record_factor(-unknown_factors[0], op)
            else:
                if len(unknown_factors) > 1:
                    raise NotImplementedError()
                for new_fac in even_factors:
                    try:
                        if factor_sign(new_fac) == 0:
                            eq_factors.append(new_fac)
                    except FactorUndetermined:
                        eq_factors.append(new_fac) #??? or pass?
                        #This doesn't matter for now because under this branch  self._allow_refinement=True, and testpoint value is not removed, so  the exception FactorUndetermined should not happen.  In the future if the code in big_cells_impl changes and this exception happens, it is still safer to eq_factors.append(new_fac). This could result in smaller cell (which is allowed). With "pass" it may raise error in corner cases, such as when the removed testpoint value was the only eq factor without which there would be a sign contradiction.
                for new_fac in lt_factors:
                    self.record_factor(new_fac, operator.le)
                if not self._big_cells:
                    for new_fac in eq_factors:
                        self.record_factor(new_fac, operator.eq)
                else: #self._big_cells is True, self._allow_refinement is True.
                    undecided_eq = []
                    for new_fac in eq_factors:
                        if self.is_factor_known(new_fac, operator.le):
                            unit_sign = -unit_sign
                        elif not self.is_factor_known(-new_fac, operator.le):
                            undecided_eq.append(new_fac) #potentially record new_fac >=0, keep the sign
                    if not undecided_eq:
                        if unit_sign > 0:
                            self.record_factor(new_fac, operator.eq) #overwrite last le factor to eq
                    else:
                        if unit_sign < 0:
                            self.record_factor(-undecided_eq[0], operator.le)
                        else:
                            self.record_factor(undecided_eq[0], operator.le)
                        for new_fac in undecided_eq[1::]:
                            self.record_factor(-new_fac, operator.le)
            logging.debug("New element in %s._le: %s" % (repr(self), comparison))
            self._le.add(comparison)
        else:
            raise NotImplementedError("Not implemented operator: {}".format(op))

    def _linexpr_spacedim_to_add(self, fac):
        space_dim_old = len(self.monomial_list())
        linexpr = polynomial_to_linexpr(fac, self.monomial_list(), self.v_dict())
        space_dim_to_add = len(self.monomial_list()) - space_dim_old
        lhs = vector(QQ, linexpr.coefficients())
        cst = QQ(linexpr.inhomogeneous_term())
        return lhs, cst, space_dim_to_add

    def is_factor_known(self, fac, op):
        if op == operator.lt:
            if fac in self.get_lt_factor():
                return True
        elif op == operator.eq:
            if (fac in self.get_eq_factor()) or (-fac in self.get_eq_factor()):
                return True
        elif op == operator.le:
            if fac in self.get_le_factor():
                return True
        else:
            raise ValueError("{} is not a supported operator".format(op))
        lhs, cst, space_dim_to_add = self._linexpr_spacedim_to_add(fac)
        #print "constraint_to_add = %s" % constraint_to_add
        if space_dim_to_add:
            self._polyhedron.add_space_dimensions_and_embed(space_dim_to_add)
            return False
        else:
            return self._polyhedron.is_linear_constraint_valid(lhs, cst, op)

    def record_factor(self, fac, op):
        #print "add %s, %s to %s" % (fac, op, self.polyhedron.constraints())
        if not self.is_factor_known(fac, op):
            lhs, cst,  _ = self._linexpr_spacedim_to_add(fac)
            if op == operator.lt:
                formatted_constraint = "%s < 0" % fac
            elif op == operator.eq:
                formatted_constraint = "%s == 0" % fac
            elif op == operator.le:
                formatted_constraint = "%s <= 0" % fac
            else:
                raise ValueError("{} is not a supported operator".format(op))
            if self._frozen:
                raise ParametricRealFieldFrozenError("Cannot prove that constraint is implied: {} ".format(formatted_constraint))
            self._polyhedron.add_linear_constraint(lhs, cst, op)
            #print " add new constraint, %s" %self.polyhedron.constraints()
            logging.info("New constraint: {}".format(formatted_constraint))
            self._factor_bsa.add_polynomial_constraint(fac, op)
            if debug_new_factors:
                import pdb
                pdb.set_trace()

    def make_proof_cell(self, **opt):
        r"""
        Make a :class:`SemialgebraicComplexComponent` from a :class:`ParametricRealField`.
        
        In **opt, one can provide: region_type, complex (parent of the cell), function, max_iter, find_region_type, default_var_bound, bddbsa, kwds_dict.

        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)

            sage: def foo(x,y):
            ....:     return (x+y < 2) and (y^2 < x)
            sage: K.<x,y> = ParametricRealField([1,1/2])
            sage: region_type = foo(*K.gens())
            sage: c = K.make_proof_cell(region_type=region_type)
            sage: c.bsa._lt
            {x + y - 2, y^2 - x}
            sage: c.plot()    #not tested

            sage: complex = SemialgebraicComplex(drlm_backward_3_slope, ['f','bkpt'])
            sage: K.<f,bkpt> = ParametricRealField([1/5,3/7])
            sage: h = drlm_backward_3_slope(f, bkpt)
            sage: region_type = find_region_type_igp(K, h)
            sage: c1 = K.make_proof_cell(complex=complex,region_type=region_type)
            sage: c1.plot()  # not tested
            sage: c1.bsa._lt
            {-2*f + 3*bkpt - 1, f - 3*bkpt + 1, 2*f - bkpt}
            sage: c2 = K.make_proof_cell(region_type=region_type, function=h, find_region_type=None)
        """
        complex = opt.pop('complex', None)
        function = opt.pop('function', None)
        find_region_type = opt.pop('find_region_type', return_result)
        region_type = opt.pop('region_type', True)
        if not complex:
            complex = SemialgebraicComplex(function, self._names, find_region_type=find_region_type, **opt)
        component = SemialgebraicComplexComponent(complex, self, self._values, region_type)
        return component

    def add_initial_space_dim(self):
        if self._bsa.monomial_list():
            # the ParametricRealField already has monomials recorded. Not brand-new.
            return
        n = len(self._names)
        P = PolynomialRing(QQ, self._names)
        monomial_list = list(P.gens())
        v_dict = {P.gens()[i]:i for i in range(n)}
        self._polyhedron = BasicSemialgebraicSet_polyhedral_ppl_NNC_Polyhedron(ambient_dim=n)
        self._bsa = BasicSemialgebraicSet_veronese(self._polyhedron, ambient_dim=n,
                                                   monomial_list=monomial_list, v_dict=v_dict)

###############################
# Simplify polynomials
###############################

def polynomial_to_linexpr(t, monomial_list, v_dict):
    r"""
    Reformulation-linearization: Expand the polynomial in the standard monomial basis and replace each monomial by a new variable. Record monomials in monomial_list and their corresponding variables in v_dict. The resulting linear expression in the extended space will be provided as inequality or equation in the linear system that describes a PPL not-necessarily-closed polyLhedron.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: P.<x,y,z> = QQ[]
        sage: monomial_list = []; v_dict = {};
        sage: t = 27/113 * x^2 + y*z + 1/2
        sage: polynomial_to_linexpr(t, monomial_list, v_dict)
        54*x0+226*x1+113
        sage: monomial_list
        [x^2, y*z]
        sage: v_dict
        {y*z: 1, x^2: 0}

        sage: tt = x + 1/3 * y*z
        sage: polynomial_to_linexpr(tt, monomial_list, v_dict)
        x1+3*x2
        sage: monomial_list
        [x^2, y*z, x]
        sage: v_dict
        {x: 2, y*z: 1, x^2: 0}
    """
    # coefficients in ppl constraint must be integers.
    lcd = lcm([x.denominator() for x in t.coefficients()])
    linexpr = Linear_Expression(0)
    if len(t.args()) <= 1:
        # sage.rings.polynomial.polynomial_rational_flint object has no attribute 'monomials'
        for (k, c) in t.dict().items():
            m = (t.args()[0])^k
            if k == 0:
                # constant term, don't construct a new Variable for it.
                v = 1
            else:
                nv = v_dict.get(m, None)
                if nv is None:
                    nv = len(monomial_list)
                    v_dict[m] = nv
                    monomial_list.append(m)
                v = Variable(nv)
            linexpr += (lcd * c) * v
    else:
        for m in t.monomials():
            if m == 1:
                v = 1
            else:
                nv = v_dict.get(m, None)
                if nv is None:
                    nv = len(monomial_list)
                    v_dict[m] = nv
                    monomial_list.append(m)
                v = Variable(nv)
            coeffv = t.monomial_coefficient(m)
            linexpr += (lcd * coeffv) * v
    return linexpr

def cs_of_eq_lt_le_poly(bsa):
    r"""
    Input bsa is an instance of BasicSemialgebraicSet_eq_lt_le_sets.
    Reformulation-linearization: Expand the polynomials in the standard monomial basis and replace each monomial by a new variable. Construct a linear constraint system in the extended space, which describes a PPL not-necessarily-closed polyhedron. Record monomials in monomial_list and their corresponding variables in v_dict.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: P.<f>=QQ[]
        sage: lt_poly = [2*f - 2, f - 2, f^2 - f, -2*f, f - 1, -f - 1, -f, -2*f + 1]
        sage: bsa = BasicSemialgebraicSet_eq_lt_le_sets(eq=[], lt=lt_poly, le=[])
        sage: cs, monomial_list, v_dict = cs_of_eq_lt_le_poly(bsa)
        sage: cs
        Constraint_System {-x0+1>0, -x0+1>0, x0-x1>0, x0>0, -x0+2>0, x0+1>0, x0>0, 2*x0-1>0}
        sage: monomial_list
        [f, f^2]
        sage: v_dict
        {f: 0, f^2: 1}
        sage: le_poly = [2*f - 2, f - 2, f^2 - f, -2*f, f - 1, -f - 1, -f, -2*f + 1]
        sage: bsa = BasicSemialgebraicSet_eq_lt_le_sets(eq=[], lt=[], le=le_poly)
        sage: cs, monomial_list, v_dict = cs_of_eq_lt_le_poly(bsa)
        sage: cs
        Constraint_System {-x0+1>=0, -x0+1>=0, x0-x1>=0, x0>=0, -x0+2>=0, x0+1>=0, x0>=0, 2*x0-1>=0}
    """
    monomial_list = []
    v_dict ={}
    cs = Constraint_System()
    for t in bsa.eq_poly():
        linexpr = polynomial_to_linexpr(t, monomial_list, v_dict)
        cs.insert( linexpr == 0 )
    for t in bsa.lt_poly():
        linexpr = polynomial_to_linexpr(t, monomial_list, v_dict)
        cs.insert( linexpr < 0 )
    for t in bsa.le_poly():
        linexpr = polynomial_to_linexpr(t, monomial_list, v_dict)
        cs.insert( linexpr <= 0 )
    return cs, monomial_list, v_dict

def simplify_eq_lt_le_poly_via_ppl(bsa):
    r"""
    Given bsa as an instance of BasicSemialgebraicSet_eq_lt_le_sets,
    Treat each monomial in bsa.eq_poly()/lt/le as a new variable.
    This gives a linear inequality system.
    Remove redundant inequalities using PPL.
    Return an instance of BasicSemialgebraicSet_eq_lt_le_sets.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: logging.disable(logging.INFO)             # Suppress output in automatic tests.
        sage: K.<f> = ParametricRealField([4/5])
        sage: h = gmic(f, field=K)
        sage: _ = extremality_test(h)
        sage: eq_factor = K.get_eq_factor()
        sage: lt_factor = K.get_lt_factor()
        sage: le_factor = K.get_le_factor()
        sage: (eq_factor, lt_factor, le_factor)
        (set(), {-f, -f + 1/2, f - 1}, set())
        sage: bsa_K = BasicSemialgebraicSet_eq_lt_le_sets(eq=eq_factor, lt=lt_factor, le=le_factor)
        sage: simplify_eq_lt_le_poly_via_ppl(bsa_K)     
        BasicSemialgebraicSet_eq_lt_le_sets(eq = [], lt = [f - 1, -2*f + 1], le = [])

        sage: K.<f, lam> = ParametricRealField([4/5, 1/6])
        sage: h = gj_2_slope(f, lam, field=K, conditioncheck=False)
        sage: bsa = simplify_eq_lt_le_poly_via_ppl(BasicSemialgebraicSet_eq_lt_le_sets(eq=K.get_eq_factor(), lt=K.get_lt_factor(), le=K.get_le_factor()))
        sage: bsa.lt_poly()
        {-lam, -f, f - 1, -f*lam - f + lam}

        sage: R = f._sym.parent().ring()
        sage: f, lam = R(f._sym), R(lam._sym)
        sage: eq_poly, lt_poly = {}, {-lam, -1/2*lam, -1/2*lam - 1/2, 1/4*lam - 1/4, 1/2*lam - 1/2, -2*f, -2*f + 1, -f, -f - 1, f - 2, f - 1, 2*f - 2, -2*f*lam + f + 2*lam - 1, -3/2*f*lam - 1/2*f + 3/2*lam, -3/2*f*lam + 1/2*f + 3/2*lam - 1, -f*lam + lam - 1, -f*lam - f + lam, -f*lam + f + lam - 2, -f*lam + f + lam - 1, -1/2*f*lam - 3/2*f + 1/2*lam, -1/2*f*lam - 3/2*f + 1/2*lam + 1, -1/2*f*lam - 1/2*f + 1/2*lam, -1/2*f*lam - 1/2*f + 1/2*lam - 1, -1/2*f*lam + 1/2*f + 1/2*lam - 2, -1/2*f*lam + 1/2*f + 1/2*lam - 1, -1/2*f*lam + 3/2*f + 1/2*lam - 2, -1/4*f*lam - 1/4*f + 1/4*lam, 1/2*f*lam - 3/2*f - 1/2*lam, 1/2*f*lam - 3/2*f - 1/2*lam + 1, 1/2*f*lam - 1/2*f - 1/2*lam, 1/2*f*lam - 1/2*f - 1/2*lam - 1, 1/2*f*lam + 1/2*f - 1/2*lam - 2, 1/2*f*lam + 1/2*f - 1/2*lam - 1, 1/2*f*lam + 3/2*f - 1/2*lam - 2, f*lam - lam, f*lam - lam - 1, f*lam - f - lam, f*lam + f - lam - 2, f*lam + f - lam - 1, 3/2*f*lam - 1/2*f - 3/2*lam, 3/2*f*lam + 1/2*f - 3/2*lam - 1, 1/2*f^2*lam + 1/2*f^2 - f*lam - 1/2*f + 1/2*lam}
        sage: bsa = simplify_eq_lt_le_poly_via_ppl(BasicSemialgebraicSet_eq_lt_le_sets(eq=eq_poly, lt=lt_poly))
        sage: bsa.lt_poly()
        {-lam,
         lam - 1,
         -2*f*lam + f + 2*lam - 1,
         -f*lam - 3*f + lam + 2,
         f*lam - lam,
         f^2*lam + f^2 - 2*f*lam - f + lam}
        sage: # eq_factor, lt_factor = K.get_eq_factor(), K.get_lt_factor()
        sage: eq_factor, lt_factor = {}, {-lam, lam - 1, 2*lam - 1, -f, f - 1, -3*f*lam - f + 3*lam, -f*lam - 3*f + lam + 2, -f*lam - f + lam, f*lam - 3*f - lam + 2, f*lam - f - lam, 3*f*lam - f - 3*lam, 3*f*lam + f - 3*lam - 2}
        sage: bsa = simplify_eq_lt_le_poly_via_ppl(BasicSemialgebraicSet_eq_lt_le_sets(eq=eq_factor, lt=lt_factor))
        sage: bsa.lt_poly()
        {-lam,
         2*lam - 1,
         f - 1,
         -3*f*lam - f + 3*lam,
         -f*lam - 3*f + lam + 2,
         f*lam - 3*f - lam + 2,
         3*f*lam - f - 3*lam}

        sage: K.<f,alpha> = ParametricRealField([4/5, 3/10])             # Bad example! parameter region = {given point}.
        sage: h=dg_2_step_mir(f, alpha, field=K, conditioncheck=False)
        sage: _ = extremality_test(h)
        sage: bsa = simplify_eq_lt_le_poly_via_ppl(BasicSemialgebraicSet_eq_lt_le_sets(eq=K.get_eq_factor(), lt=K.get_lt_factor()))
        sage: (bsa.eq_poly(), bsa.lt_poly())
        ({-10*alpha + 3, -5*f + 4}, set())

        sage: K.<f> = ParametricRealField([1/5])
        sage: h = drlm_3_slope_limit(f, conditioncheck=False)
        sage: _ = extremality_test(h)
        sage: bsa = simplify_eq_lt_le_poly_via_ppl(BasicSemialgebraicSet_eq_lt_le_sets(eq=K.get_eq_factor(), lt=K.get_lt_factor()))
        sage: (bsa.eq_poly(), bsa.lt_poly())
        (set(), {-f, 3*f - 1})
    """
    cs, monomial_list, v_dict = cs_of_eq_lt_le_poly(bsa)
    p = NNC_Polyhedron(cs)
    return read_bsa_from_polyhedron(p, bsa.poly_ring(), monomial_list, v_dict)


def read_bsa_from_polyhedron(p, poly_ring, monomial_list, v_dict, tightened_mip=None):
    r"""
    Given a PPL polyhedron p, map the minimal constraints system of p back to polynomial equations and inequalities in the orginal space. If a constraint in the minimal constraint system of p is not tight for the tightened_mip, then this constraint is discarded. Return an instance of BasicSemialgebraicSet_eq_lt_le_set;

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: P.<f>=QQ[]
        sage: eq_poly =[]; lt_poly = [2*f - 2, f - 2, f^2 - f, -2*f, f - 1, -f - 1, -f, -2*f + 1]
        sage: cs, monomial_list, v_dict = cs_of_eq_lt_le_poly(BasicSemialgebraicSet_eq_lt_le_sets(eq=eq_poly, lt=lt_poly))
        sage: p = NNC_Polyhedron(cs)
        sage: read_bsa_from_polyhedron(p, P, monomial_list, v_dict)
        BasicSemialgebraicSet_eq_lt_le_sets(eq = [], lt = [f - 1, f^2 - f, -2*f + 1], le = [])
    """
    mineq = []
    minlt = []
    minle = []
    mincs = p.minimized_constraints()
    for c in mincs:
        if tightened_mip is not None and is_not_a_downstairs_wall(c, tightened_mip):
            # McCormick trash, don't put in minlt.
            continue
        coeff = c.coefficients()
        # observe: coeffients in a constraint of NNC_Polyhedron could have gcd != 1.
        # take care of this.
        gcd_c = gcd(gcd(coeff), c.inhomogeneous_term())
        # constraint is written with '>', while lt_poly records '<' relation
        t = sum([-QQ(x)/gcd_c*y for x, y in zip(coeff, monomial_list)]) - QQ(c.inhomogeneous_term())/gcd_c
        if c.is_equality():
            mineq.append(t)
        elif c.is_strict_inequality():
            minlt.append(t)
        else:
            #logging.warning("Non-strict inequality in NNC polyhedron, recording strict inequality instead")
            #assert c.is_nonstrict_inequality()
            minle.append(t)
    # note that polynomials in mineq and minlt can have leading coefficient != 1
    
    return BasicSemialgebraicSet_eq_lt_le_sets(poly_ring=poly_ring, eq=mineq, lt=minlt, le=minle)

def read_simplified_leq_llt_lle(K, level="factor"):
    r"""
    Use the reformulation-linearization techinque to remove redundant inequalties and equations recorded in :class:`ParametricRealField` K. Return an instance of BasicSemialgebraicSet_eq_lt_le_set;


    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: K.<f> = ParametricRealField([4/5])
        sage: h = gmic(f, field=K)
        sage: _ = extremality_test(h)
        sage: read_simplified_leq_llt_lle(K)
        BasicSemialgebraicSet_eq_lt_le_sets(eq = [], lt = [f - 1, -2*f + 1], le = [])

        sage: K.<f> = ParametricRealField([1/5])
        sage: h = drlm_3_slope_limit(f, conditioncheck=False)
        sage: _ = extremality_test(h)
        sage: read_simplified_leq_llt_lle(K)
        BasicSemialgebraicSet_eq_lt_le_sets(eq = [], lt = [3*f - 1, -f], le = [])
    """
    if level == "factor":
        #leq, lin = simplify_eq_lt_le_poly_via_ppl(K.get_eq_factor(), K.get_lt_factor())
        # Since we update K.polyhedron incrementally,
        # just read leq and lin from its minimized constraint system.
        #### to REFACTOR
        bsa = read_bsa_from_polyhedron(K.ppl_polyhedron(), K._factor_bsa.poly_ring(), K.monomial_list(), K.v_dict())
    else:
        bsa = BasicSemialgebraicSet_eq_lt_le_sets(base_ring=QQ, eq=K.get_eq(), lt=K.get_lt(), le=K.get_le())
    if bsa.eq_poly():
        logging.warning("equation list %s is not empty!" % bsa.eq_poly())
    return bsa

def find_variable_mapping(leqs):
    r"""
    Return the list of equations after variables elimination and return the map.
    Assume that leqs is the result bsa._eq from ``read_bsa_from_polyhedron()``,
    so that gaussian elimination has been performed by PPL on the list of equations. 
    If an equation has a linear variable, then eliminate it.

    FIXME: This function is bad; it assumes too many things.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: logging.disable(logging.WARN)
        sage: P.<a,b,c>=QQ[]
        sage: find_variable_mapping([a+2*b+1])
        ([a + 2*b + 1], {c: c, b: b, a: -2*b - 1})
        sage: find_variable_mapping([2*a+b, b+c-1/2])
        ([2*a - c + 1/2, b + c - 1/2], {c: c, b: -c + 1/2, a: 1/2*c - 1/4})
        sage: find_variable_mapping([a*a-b, b*b-c*c])
        ([a^2 - b, a^4 - c^2], {c: c, b: a^2, a: a})
        sage: find_variable_mapping([a^2+4*a+1])
        ([a^2 + 4*a + 1], {c: c, b: b, a: a})
        sage: P.<d>=QQ[]
        sage: find_variable_mapping([1-d^3])
        ([-d^3 + 1], {d: d})
        sage: P.<f,a,b> = QQ[]
        sage: find_variable_mapping([-f*a + 3*a^2 + 3*f*b - 9*a*b, -11*b + 2, -11*f + 3, -11*a + 1])
        ([-11*b + 2, -11*f + 3, -11*a + 1], {b: 2/11, a: 1/11, f: 3/11})

    """
    if not leqs:
        raise ValueError("equations are not provided.")
    variables = leqs[0].args()
    var_map = {}
    for v in variables:
        var_map[v] = v
    n = len(leqs)
    if len(variables) == 1: # workaround for single variable 'Polynomial_rational_flint'
        # FIXME: R.<x>=PolynomialRing(QQ,1,order="lex") is considered as Multivariate Polynomial Ring.
        v = variables[0]
        for i in range(n):
            if leqs[i].degree() == 1:
                var_map[v] = -leqs[i].list()[0]/leqs[i].list()[1]
                for j in range(n):
                    if j != i:
                        leqs[j] = leqs[j].subs(var_map)
                break
        #logging.warning("Can't solve for %s in the system %s == 0, %s < 0. Heurist wall crossing may fail." % (v, leqs, lins))
        return [l for l in leqs if l != 0], var_map
    for i in range(n): #range(n-1, -1, -1):
        for v in variables:     
            if (leqs[i]//v).degree() == 0: # v is a linear variable in leqs[i].
                coef = leqs[i].monomial_coefficient(v) # type is rational
                v_mapped_to = v - leqs[i] / coef # eliminate v
                var_map[v] = v_mapped_to
                for w in variables:
                    if w != v:
                        var_map[w] = var_map[w].subs({v:v_mapped_to})
                for j in range(n):
                    if j != i:
                        leqs[j] = leqs[j].subs({v:v_mapped_to})
                break
    return [l for l in leqs if l != 0], var_map

def substitute_llt_lle(llt, lle, var_map, var_name, var_value):
    r"""
    Return a list of strict inequalities and a list of non-strict inequalities
    after substitution using var_map and simplification using the Reformulation-linearization trick.

    Used in ``SemialgebraicComplexComponent.__init__``

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: logging.disable(logging.INFO)
        sage: P.<x,y>=QQ[]
        sage: var_map = {y: y, x: 75/19*y}
        sage: llt = [21*x - 8, -x, 950*x^2 - 3700*x*y - 225*y^2 - 133*x]
        sage: substitute_llt_lle(llt, [], var_map, ['x','y'], [38/100, 96/1000])
        ([1575*y - 152, -y], [])
    """
    # Shall we factorize ineq in lins after substitution using var_map?
    # Yes, otherwise, got -525/19*lam2^2 - 525*lam2 in chen's 4 slope
    # at (lam1, lam2) = [20015786415699825/52611587391975857, 5070665891977289/52611587391975857]
    K = ParametricRealField(var_value, var_name)
    K.add_initial_space_dim() # needed?
    for l in llt:
        ineq = l.parent()(l.subs(var_map))
        ineq(K.gens())< 0 #always True
    for l in lle:
        ineq = l.parent()(l.subs(var_map))
        ineq(K.gens())<= 0 #always True
    bsa = read_simplified_leq_llt_lle(K)
    return list(bsa.lt_poly()), list(bsa.le_poly())

######################################
# Functions with ParametricRealField K
######################################

from sage.misc.sageinspect import sage_getargspec, sage_getvariablename

def read_default_args(function, **opt_non_default):
    r"""
    Return the default values of arguments of the function.

    Override the default values if opt_non_default is given.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: read_default_args(gmic)
        {'conditioncheck': True, 'f': 4/5, 'field': None}
        sage: read_default_args(drlm_backward_3_slope, **{'bkpt': 1/5})
        {'bkpt': 1/5, 'conditioncheck': True, 'f': 1/12, 'field': None}
    """
    if function is None:
        return {}
    args, varargs, keywords, defaults = sage_getargspec(function)
    default_args = {}
    if defaults is not None:
        for i in range(len(defaults)):
            default_args[args[-i-1]]=defaults[-i-1]
    for (opt_name, opt_value) in opt_non_default.items():
        if opt_name in default_args:
            default_args[opt_name] = opt_value
    return default_args

def construct_field_and_test_point(function, var_name, var_value, default_args):
    r"""
    Construct a :class:`ParametricRealField` K using var_name and var_value.

    var_name and var_value are two parallel lists.
    Construct a test_point of type dictionary, which maps each parameter of the function to the corresponding :class:`ParametricRealFieldElement` if this is a parameter of K, otherwise maps to the default argument value.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: function=gmic; var_name=['f']; var_value=[1/2];
        sage: default_args = read_default_args(function)
        sage: K, test_point = construct_field_and_test_point(function, var_name, var_value, default_args)
        sage: K
        ParametricRealField(names = ['f'], values = [1/2])
        sage: test_point
        {'conditioncheck': False,
             'f': f~,
             'field': ParametricRealField(names = ['f'], values = [1/2])}
    """
    K = ParametricRealField(var_value, var_name)
    test_point = copy(default_args)
    if isinstance(function, CPLFunctionsFactory):
        # Remark: special case. Parameters are f and z=(z1, z2, ... z(n-1))
        # group variables into f and z-tuple.
        # The constructor of cpl will call function._theta to get o-tuple,
        # when o is set to None (default value).
        param_name = ['f', 'z']
        param_value = [K.gens()[0], tuple(K.gens()[1::])]
    else:
        param_name = var_name
        param_value = K.gens()
    for i in range(len(param_name)):
        test_point[param_name[i]] = param_value[i]
    args_set = set(sage_getargspec(function)[0])
    if 'field' in args_set:
        test_point['field'] = K
    if 'conditioncheck' in args_set:
        test_point['conditioncheck'] = False
    if 'merge' in args_set:
        test_point['merge'] = False
    return K, test_point

###########################################
# Proof cells and proof complex:
# the super class SemialgebraicComplex
###########################################
class SemialgebraicComplexComponent(SageObject):
    r"""
    A proof cell for parameter space analysis.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: logging.disable(logging.WARN)
        sage: def foo(x,y):
        ....:     return (x+y < 2) and (y^2 < x)

        sage: complex = SemialgebraicComplex(foo, ['x','y'], max_iter=2, find_region_type=lambda r:r, default_var_bound=(-5,5))
        sage: K.<x,y> = ParametricRealField([1,1/2])
        sage: region_type = foo(*K.gens())
        sage: component = SemialgebraicComplexComponent(complex, K, [1,1/2], region_type)
        sage: component.bsa
        BasicSemialgebraicSet_eq_lt_le_sets(eq = [], lt = [y^2 - x, x + y - 2], le = [])
        sage: component.plot()                                  # not tested
        sage: component.find_walls_and_new_points(1/4, 'heuristic', goto_lower_dim=False)
        ([y^2 - x, x + y - 2],
         {(19959383/28510088, 24590405/28510088): [], (11/8, 7/8): []})
        sage: component.find_walls_and_new_points(1/4, 'mathematica', goto_lower_dim=True)  # optional - mathematica
        ([x + y - 2, y^2 - x],
         {(0, 0): [y^2 - x],
          (2, 0): [x + y - 2],
          (17/8, 0): [],
          (2065/512, -33/16): []})

    Test variable elimination::

        sage: from cutgeneratingfunctionology.igp import *
        sage: complex = SemialgebraicComplex(foo, ['x','y'], max_iter=2, find_region_type=lambda r:r, default_var_bound=(-5,5))
        sage: K.<x,y> = ParametricRealField([1,1/2])
        sage: region_type = foo(*K.gens())
        sage: x == 2*y
        True
        sage: component = SemialgebraicComplexComponent(complex, K, [1,1/2], region_type)
        sage: component.bsa
        BasicSemialgebraicSet_eq_lt_le_sets(eq = [-x + 2*y], lt = [3*y - 2, -y], le = [])
    """

    def __init__(self, parent, K, var_value, region_type):
        self.parent = parent
        self.var_value = var_value
        self.region_type = region_type
        self.monomial_list = K.monomial_list()
        self.v_dict = K.v_dict()
        #self.polyhedron = K.polyhedron
        #space_dim_old = len(self.monomial_list)
        ## to REFACTOR:
        self.bounds, tightened_mip = self.bounds_propagation(K.ppl_polyhedron(), self.parent.max_iter)
        # Unimplemented
        # dim_to_add =  len(self.monomial_list) - space_dim_old:
        # if dim_to_add > 0:
        #     # this could happen if we allow McCormicks to add new monomials.
        #     K.polyhedron.add_space_dimensions_and_embed(dim_to_add)
        if self.parent.max_iter == 0:
            tightened_mip = None
        ## to REFACTOR:
        bsa = read_bsa_from_polyhedron(K.ppl_polyhedron(), K._factor_bsa.poly_ring(), K.monomial_list(), K.v_dict(), tightened_mip)
        if not bsa.eq_poly():
            P = PolynomialRing(QQ, parent.var_name)
            self.var_map = {g:g for g in P.gens()}
            self.bsa = bsa
        else:
            leq, self.var_map = find_variable_mapping(list(bsa.eq_poly()))
            llt, lle = substitute_llt_lle(bsa.lt_poly(), bsa.le_poly(), self.var_map, self.parent.var_name, self.var_value)
            self.bsa = BasicSemialgebraicSet_eq_lt_le_sets(eq=leq, lt=llt, le=lle)
        self.neighbor_points = []

    def __repr__(self):
        s = "SemialgebraicComplexComponent(var_value={}, region_type={}".format(self.var_value, self.region_type)
        if self.is_polyhedral():
            s += ", polyhedral"
        if self.bsa.eq_poly():
            s += ", {} eqs".format(len(self.bsa.eq_poly()))
        if self.bsa.lt_poly():
            s += ", {} strict-ins".format(len(self.bsa.lt_poly()))
        if self.bsa.le_poly():
            s += ", {} nonstrict-ins".format(len(self.bsa.le_poly()))
        s += ")"
        return s

    def bounds_propagation(self, polyhedron, max_iter):
        r"""
        Compute LP bounds for variables and then do upward and downward bounds propagation until
        max_iter is attained or no more changes of bounds occur.
        See examples in ``update_mccormicks_for_monomial()``.

        The following example comes from ``chen_4_slope``. It shows that the non-linear inequality is discarded from the description of the (polyhedral) cell after max_iter=2 rounds of bounds_propagation.

        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.INFO)
            sage: K.<lam1,lam2>=ParametricRealField([3/10, 45/101])
            sage: h = chen_4_slope(K(7/10), K(2), K(-4), lam1, lam2)
            sage: region_type = find_region_type_igp(K, h)
            sage: bsa = read_bsa_from_polyhedron(K.ppl_polyhedron(), K._factor_bsa.poly_ring(), K.monomial_list(), K.v_dict())
            sage: bsa.lt_poly()
            {2*lam2 - 1, -2*lam1 + lam2, 19*lam1 - 75*lam2, 21*lam1 - 8}
            sage: c = K.make_proof_cell(region_type=region_type, function=h, find_region_type=None)
            sage: c.bsa.lt_poly()
            {2*lam2 - 1, -2*lam1 + lam2, 19*lam1 - 75*lam2, 21*lam1 - 8}
        """
        tightened_mip = construct_mip_of_nnc_polyhedron(polyhedron)
        # Compute LP bounds first
        bounds = [find_bounds_of_variable(tightened_mip, i) for i in range(len(self.monomial_list))]

        bounds_propagation_iter = 0
        # TODO: single parameter polynomial_rational_flint object needs special treatment. ignore bounds propagation in this case for now.  #tightened = True
        tightened = bool(len(self.var_value) > 1)

        while bounds_propagation_iter < max_iter and tightened:
            tightened = False
            # upward bounds propagation
            for m in self.monomial_list:
                if update_mccormicks_for_monomial(m, tightened_mip, self.monomial_list, self.v_dict, bounds, new_monomials_allowed=False):
                    # If we allow update_mccormicks_for_monomial to create new monomials and
                    # hence lift the extended space, try with optional argument
                    # new_monomials_allowed=True
                    tightened = True
            if tightened:
                tightened = False
                # downward bounds propagation
                for i in range(len(self.monomial_list)):
                    (lb, ub) = bounds[i]
                    bounds[i] = find_bounds_of_variable(tightened_mip, i)
                    if (bounds[i][0] is not None) and ((lb is None) or (bounds[i][0] - lb > 0.001)) or \
                       (bounds[i][1] is not None) and ((ub is None) or (ub - bounds[i][1] > 0.001)):
                        tightened = True
            if max_iter != 0 and bounds_propagation_iter >= max_iter:
                logging.warning("max number %s of bounds propagation iterations has attained." % max_iter)
            bounds_propagation_iter += 1
        #print bounds_propagation_iter
        return bounds, tightened_mip

    def plot(self, alpha=0.5, plot_points=300, slice_value=None, show_testpoints=True, **kwds):
        r"""
        Plot the cell.

        - If slice_value is given, plot the slice of the cell according to the parameter values in slice_value that are not None. See examples in ``SemialgebraicComplex.plot()``.
        - show_testpoints controls whether to plot the testpoint in this cell.
        - plot_points controls the quality of the plotting.
        """
        g = Graphics()
        if 'xmin' in kwds:
            g.xmin(kwds['xmin'])
        if 'xmax' in kwds:
            g.xmax(kwds['xmax'])
        if 'ymin' in kwds:
            g.ymin(kwds['ymin'])
        if 'ymax' in kwds:
            g.ymax(kwds['ymax'])
        x, y = var('x, y')
        var_bounds = []
        P = PolynomialRing(QQ, self.parent.var_name)
        for m in P.gens():
            i = self.v_dict.get(m, None)
            if i is None:
                var_bounds.append((None, None))
            else:
                var_bounds.append(self.bounds[i])
        bounds_y = (y, -0.01, 0.01)
        Q = QQ['xx, yy']
        xx, yy = Q._first_ngens(2)
        if not slice_value:
            d = len(self.var_value)
            if d == 1:
                var_pt = xx
                if not is_value_in_interval(None, var_bounds[0]):
                     return g
                bounds_x = bounds_for_plotting(x, var_bounds[0], self.parent.default_var_bound)
            elif d == 2:
                var_pt = [xx, yy]
                if not (is_value_in_interval(None, var_bounds[0]) and is_value_in_interval(None, var_bounds[1])):
                    return g
                bounds_x = bounds_for_plotting(x, var_bounds[0], self.parent.default_var_bound)
                bounds_y = bounds_for_plotting(y, var_bounds[1], self.parent.default_var_bound)
            else:
                raise NotImplementedError("Plotting region with dimension > 2 is not implemented. Provide `slice_value` to plot a slice of the region.")
        else:
            d = 0
            var_pt = []
            for (i, z) in enumerate(slice_value):
                if z is None:
                    d += 1
                    if d == 1:
                        var_pt.append(xx)
                        bounds_x = bounds_for_plotting(x, var_bounds[i], self.parent.default_var_bound)
                    elif d == 2:
                        var_pt.append(yy)
                        bounds_y = bounds_for_plotting(y, var_bounds[i], self.parent.default_var_bound)
                    else:
                        raise NotImplementedError("Plotting region with dimension > 2 is not implemented. Provide `slice_value` to plot a slice of the region.")
                else:
                    if not is_value_in_interval(z, var_bounds[i]):
                        return g
                    var_pt.append(z)
        leqs = []
        for leq in self.bsa.eq_poly():
            l = leq(var_pt)
            if l in QQ:
                if l != 0:
                    return g
            else:
                leqs.append(l)
        llts = []
        for llt in (self.bsa.lt_poly()).union(self.parent.bddbsa.lt_poly()):
            l = llt(var_pt)
            if l in QQ:
                if l >= 0:
                    return g
            else:
                llts.append(l)
        lles = []
        for lle in (self.bsa.le_poly()).union(self.parent.bddbsa.le_poly()):
            l = lle(var_pt)
            if l in QQ:
                if l > 0:
                    return g
            else:
                lles.append(l)
        bsa = BasicSemialgebraicSet_eq_lt_le_sets(eq=leqs, lt=llts, le=lles)
        if slice_value:
            bsa = simplify_eq_lt_le_poly_via_ppl(bsa)
        constraints = [l(x, y) == 0 for l in bsa.eq_poly()] + [l(x, y) < 0 for l in bsa.lt_poly()] + [l(x, y) <= 0 for l in bsa.le_poly()]
        if (not constraints) or (constraints == [False]):
            # empty polytope
            return g
        if ('xmin' in kwds) and ('xmax' in kwds):
            bounds_x = (x, kwds['xmin'], kwds['xmax'])
        if ('ymin' in kwds) and ('ymax' in kwds):
            bounds_y = (y, kwds['ymin'], kwds['ymax'])
        if 'color'  in kwds:
            innercolor = kwds['color']
        else:
            innercolor = find_region_color(self.region_type)
        bordercolor = innercolor
        if innercolor == 'white':
            ptcolor = 'black'
        else:
            ptcolor = 'white'
            g += region_plot(constraints, bounds_x, bounds_y, \
                             incol=innercolor, alpha=alpha, plot_points=plot_points, bordercol=bordercolor)
        if show_testpoints and not slice_value:
            if d == 1:
                pt = (self.var_value[0], 0)
            else:
                pt = self.var_value
            if (bounds_x[1] <= pt[0] <= bounds_x[2] and \
                bounds_y[1] <= pt[1] <= bounds_y[2]):
                g += point(pt, color = ptcolor, size = 2, zorder=10)
        return g

    def plot2dslice(self, slice_value, alpha=0.5, plot_points=300, **kwds):
        r"""
        slice_value is a list of symbolic expressions in var('x, y'). 
        slice_value has the same length as self.var_value.
        """
        g = Graphics()
        if 'xmin' in kwds:
            g.xmin(kwds['xmin'])
        if 'xmax' in kwds:
            g.xmax(kwds['xmax'])
        if 'ymin' in kwds:
            g.ymin(kwds['ymin'])
        if 'ymax' in kwds:
            g.ymax(kwds['ymax'])
        constraints = []
        for leq in self.bsa.eq_poly():
            l = leq(slice_value)
            if l in QQ:
                if l != 0:
                    return g
            else:
                constraints.append(l == 0)
        for llt in self.bsa.lt_poly() + self.parent.bddbsa.lt_poly():
            l = llt(slice_value)
            if l in QQ:
                if l >= 0:
                    return g
            else:
                constraints.append(l < 0)
        for lle in self.bsa._lle + self.parent.bddbsa._lle:
            l = lle(slice_value)
            if l in QQ:
                if l > 0:
                    return g
            else:
                constraints.append(l <= 0)
        if ('xmin' in kwds) and ('xmax' in kwds):
            bounds_x = (kwds['xmin'], kwds['xmax'])
        else:
            bounds_x = self.parent.default_var_bound
        if ('ymin' in kwds) and ('ymax' in kwds):
            bounds_y = (y, kwds['ymin'], kwds['ymax'])
        else:
            bounds_y = self.parent.default_var_bound
        if 'color' in kwds:
            innercolor = kwds['color']
        else:
            innercolor = find_region_color(self.region_type)
        bordercolor = innercolor
        x, y = var('x, y')
        if innercolor != 'white':
            g += region_plot(constraints, (x, bounds_x[0], bounds_x[1]), (y, bounds_y[0], bounds_y[1]), incol=innercolor, alpha=alpha, plot_points=plot_points, bordercol=bordercolor)
        return g

    def find_walls_and_new_points(self, flip_ineq_step, wall_crossing_method, goto_lower_dim=False):
        r"""
        Try flipping exactly one inequality at one time, to reach a new textpoint in a neighbour cell.

        Discard the wall if it is impossible to do so, as the wall is redundant.

        - flip_ineq_step defines the step length
        - wall_crossing_method is 'heuristic' or 'mathematica' or 'heuristic_with_check'
        - goto_lower_dim tells whether it also finds new testpoints on the walls.
        """
        walls = []
        new_points = {}
        if self.bsa.eq_poly():
            bddllt, bddlle = substitute_llt_lle(self.parent.bddbsa.lt_poly(), self.parent.bddbsa.le_poly(), self.var_map, self.parent.var_name, self.var_value)
            bddlin = bddllt+bddlle
        else:
            bddlin = list(self.parent.bddbsa.lt_poly())+list(self.parent.bddbsa.le_poly())
        selflin = list(self.bsa.lt_poly())+list(self.bsa.le_poly())
        # decide which inequalities among self.lin are walls (irredundant).
        for i in range(len(selflin)):
            ineq = selflin[i]
            ineqs = selflin[i+1::] + bddlin
            if ineq in ineqs:
                continue
            if wall_crossing_method == 'mathematica':
                ineqs = walls + ineqs
                condstr_others = write_mathematica_constraints(self.bsa.eq_poly(), ineqs)
                # maybe shouldn't put self.bsa.eq_poly() into FindInstance, but solve using var_map later.
                condstr_ineq = '0<'+str(ineq)+'<'+str(flip_ineq_step)
                pt_across_wall = find_instance_mathematica(condstr_others + condstr_ineq, self.parent.var_name)
            else:
                if wall_crossing_method == 'heuristic_with_check':
                    ineqs = walls + ineqs
                else:
                    #less clever, more careful, for 'heuristic'
                    ineqs = selflin[:i] + ineqs
                pt = find_point_flip_ineq_heuristic(self.var_value, ineq, ineqs, flip_ineq_step)
                if pt is None:
                    if wall_crossing_method == 'heuristic_with_check':
                        condstr = write_mathematica_constraints(self.bsa.eq_poly(), ineqs) + \
                                  '0<'+str(ineq)+'<'+str(flip_ineq_step) # Need the last inequality? see hyperbole ex.
                        pt_across_wall = find_instance_mathematica(condstr, self.parent.var_name)
                    else:
                        pt_across_wall = None
                else:
                    if self.bsa.eq_poly():
                        pt_across_wall = tuple(self.var_map[v](pt) for v in ineq.args())
                    else:
                        pt_across_wall = pt
            if pt_across_wall is None:
                # ineq is not an wall
                continue
            walls.append(ineq)
            if not ((wall_crossing_method == 'heuristic_with_check') and (pt is None)):
                # Hope that the new pt_across_wall is in a general position, so that running the function on it does not generate new equations. Otherwise bfs got stuck in low dimension. Two solutions: take smaller flip_ineq_step, or do bfs with check_completion=True.
                new_points[pt_across_wall] = list(self.bsa.eq_poly())
            if goto_lower_dim is True:
                pt_on_wall = None
                if wall_crossing_method == 'mathematica':
                    # wall could be non-linear, contrasting the assumption above. 
                    condstr_ineq = str(ineq) + '==0'
                    pt_on_wall = find_instance_mathematica(condstr_others + condstr_ineq, self.parent.var_name)
                elif ineq.degree() == 1:
                    # is linear wall. try to find a point on the wall using heuristic gradient descent method.
                    pt = find_point_on_ineq_heuristic(pt_across_wall, ineq, ineqs, flip_ineq_step)
                    if pt is None:
                        pt_on_wall = None
                    elif self.bsa.eq_poly():
                        pt_on_wall = tuple(self.var_map[v](pt) for v in ineq.args())
                    else:
                        pt_on_wall = pt
                if not pt_on_wall is None:
                    new_points[pt_on_wall] = list(self.bsa.eq_poly()) + [ineq]
        return walls, new_points

    def discard_redundant_inequalities(self, flip_ineq_step=0):
        r"""
        Use Mathematica's ``FindInstance`` to discard redundant inequalities in the cell description.
        TO UPDATE with bsa
        """
        walls = []
        bddlin = []
        if self.leq:
            bddlin = substitute_llt_lle(self.parent.bddlin, self.var_map, self.parent.var_name, self.var_value)
        else:
            bddlin = copy(self.parent.bddlin)
        # decide which inequalities among self.lin are walls (irredundant).
        for i in range(len(self.lin)):
            ineq = self.lin[i]
            ineqs = self.lin[i+1::] + bddlin
            if ineq in ineqs:
                continue
            ineqs = walls + ineqs
            pt_across_wall = None
            for pt in self.neighbor_points:
                if (ineq(pt) > 0) and all(l(pt) < 0 for l in ineqs):
                    pt_across_wall = pt
                    break
            if pt_across_wall is None:
                condstr_others = write_mathematica_constraints(self.leq, ineqs)
                # maybe shouldn't put self.leq into FindInstance, but solve using var_map later.
                condstr_ineq = '0<'+str(ineq)
                if flip_ineq_step > 0:  # experimental. see hyperbole example where wall x=1/2 is not unique; discard it in this case.
                    condstr_ineq += '<'+str(flip_ineq_step)
                pt_across_wall = find_instance_mathematica(condstr_others + condstr_ineq, self.parent.var_name)
            if not (pt_across_wall is None):
                walls.append(ineq)
        self.lin = walls

    def is_polyhedral(self):
        for l in list(self.bsa.eq_poly()) + list(self.bsa.lt_poly()) + list(self.bsa.le_poly()):
            if l.degree() > 1:
                return False
        return True

    def sage_polyhedron(self):
        if not self.is_polyhedral():
            raise NotImplementedError("The cell is not polyhedral. Construct the polyhedron in the lifted space.")
        ieqs = [ [-l.constant_coefficient()]+[-l.monomial_coefficient(m) for m in l.args()] for l in list(self.bsa.lt_poly()) + list(self.bsa.le_poly()) ]
        eqns = [ [-l.constant_coefficient()]+[-l.monomial_coefficient(m) for m in l.args()] for l in self.bsa.eq_poly() ]
        return Polyhedron(ieqs=ieqs, eqns=eqns)

class SemialgebraicComplex(SageObject):
    r"""
    A proof complex for parameter space analysis.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: logging.disable(logging.WARN)

        sage: def vol(a,b):
        ....:     P = Polyhedron(ieqs=[(0,0,1),(0,1,0),(1,-1,0),(1,0,-1),(a,-1,0),(b,0,-1)])
        ....:     return P.volume()
        sage: complex = SemialgebraicComplex(vol, ['a','b'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-1,3))

    Breadth-first-search to complete the complex, starting at the point (a,b)=(2,1/2), using heuristic wall-crossing, considering full-dimensional cells only::

        sage: complex.bfs_completion(var_value=[2, 1/2], flip_ineq_step=1/1000, check_completion=False, wall_crossing_method='heuristic', goto_lower_dim=False)
        sage: len(complex.components)
        9
        sage: complex.components[0].region_type
        (b,)
        sage: complex.components[1].region_type
        (a*b,)
        sage: complex.plot()                                  # not tested

    Instead of heuristic method, we can use Mathematica's ``FindInstance`` to look for uncovered points in wall-crossing::

        sage: complex = SemialgebraicComplex(vol, ['a','b'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-1,3))                         # optional - mathematica
        sage: complex.bfs_completion(var_value=[2, 1/2], flip_ineq_step=1/1000, check_completion=False, wall_crossing_method='mathematica', goto_lower_dim=True)        # optional - mathematica
        sage: len(complex.components)                         # optional - mathematica
        25

    The entire parameter space is covered by cells::

        sage: complex.is_complete(strict=True)                # optional - mathematica
        True
        
    Example with non-linear wall::

        sage: complex = SemialgebraicComplex(lambda x,y: max(x,y^2), ['x','y'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-3,3))  # optional - mathematica
        sage: complex.bfs_completion(var_value=[1,1/2], check_completion=True, wall_crossing_method='mathematica', goto_lower_dim=True)                             # optional - mathematica
        sage: len(complex.components)                         # optional - mathematica
        3
        sage: complex.components[0].region_type               # optional - mathematica
        (x,)
        sage: complex.components[1].region_type               # optional - mathematica
        (y^2,)
        sage: complex.plot()                                  # not tested


    Analyse the extreme/minimal/valid regions of a function in the Gomory-Johnson infinite group problem.

    Use random shooting method to complete the complex. See more options in the method ``shoot_random_points``::

        sage: complex = SemialgebraicComplex(drlm_backward_3_slope, ['f','bkpt'])
        sage: complex.shoot_random_points(50)

    Use breadth-first-search to complete the complex. See more options in the method ``bfs_completion``::

        sage: complex = SemialgebraicComplex(drlm_backward_3_slope, ['f','bkpt'])
        sage: complex.bfs_completion(var_value=[4/5,1/2])
        sage: len(complex.components)
        17
        sage: complex.is_polyhedral()
        True
        sage: complex.is_face_to_face()
        False
        sage: complex2 = complex.subcomplex_of_cells_with_given_region_types({'is_extreme','not_extreme','not_minimal'})
        sage: complex2.is_face_to_face()
        True
        sage: extc = complex.subcomplex_of_cells_with_given_region_types()
        sage: len(extc.components)
        2
        sage: extc.is_polyhedral()
        True
        sage: extc.is_face_to_face()
        True
        sage: boundary = extc.guess_boundary()
        sage: sorted(boundary, key=str)
        [-f, -f + 4*bkpt - 1, f - bkpt]
        sage: extc.is_complete(bddlin=boundary,strict=True) # optional - mathematica
        False
        sage: extc.is_complete(bddlin=boundary,strict=False) # optional - mathematica
        True
        sage: pc = extc.polyhedral_complex()
        sage: list(sorted( sorted(pol.vertices_list()) for pol in pc.cells_list() ))
        [[[0, 0]],
         [[0, 0], [0, 1/4]],
         [[0, 0], [0, 1/4], [1/7, 2/7]],
         [[0, 0], [1/7, 2/7]],
         [[0, 0], [1/7, 2/7], [1/3, 1/3]],
         [[0, 0], [1/3, 1/3]],
         [[0, 1/4]],
         [[0, 1/4], [1/7, 2/7]],
         [[1/7, 2/7]],
         [[1/7, 2/7], [1/3, 1/3]],
         [[1/3, 1/3]]]

    Consider low-dimensional cells in the polyhedral case::

        sage: complex = SemialgebraicComplex(drlm_backward_3_slope, ['f','bkpt'])   #long time
        sage: complex.bfs_completion(var_value=[4/5,1/2],goto_lower_dim=True)       #long time
        sage: len(complex.components)                                               #long time
        46
        sage: extc = complex.subcomplex_of_cells_with_given_region_types()          #long time
        sage: len(extc.components)                                                  #long time
        6
        sage: boundary = extc.guess_boundary()                                      #long time
        sage: boundary                                                              #long time
        [f - bkpt, -f, -f + 4*bkpt - 1]
        sage: extc.is_complete(bddlin=boundary,strict=True)                         #long time, optional - mathematica
        True
    """
    def __init__(self, function, var_name, max_iter=2, find_region_type=None, default_var_bound=(-0.1,1.1), bddbsa=None, kwds_dict={}, **opt_non_default):
        r"""
        Construct a SemialgebraicComplex.

        - function: we are interested in analysing how the output of this function varies with its parameters
        - var_name: a subset of the parameters of the function that we study
        - max_iter: the max number of iterations in updating McCormick inequalites
        - find_region_type: maps the output of function to a type of the parameter region;
            - set to ``None`` for functions in Gomory-Johnson model; 
            - often set to ``result_symbolic_expression`` or ``result_concrete_value`` for other functions;
        - default_var_bound: need if we use random shooting method to complete the complex; If given, the bound is also used in plotting

        The following two arguments are used to define the boundary of the SemialgebraicComplex, so that bfs won't go beyond the region. They might be useful in the CPL3 examples.

        - bddbsa: a BasicSemialgebraicSet_eq_lt_le_sets that contains the points in the complex;
        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.WARN)
            sage: complex = SemialgebraicComplex(lambda x,y: max(x,y), ['x','y'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-10,10))
        """
        #self.num_components = 0
        self.components = []

        self.function = function
        self.d = len(var_name)
        self.var_name = var_name
        self.default_args = read_default_args(function, **opt_non_default)
        self.default_args.update(kwds_dict)
        self.graph = Graphics()
        self.num_plotted_components = 0
        self.points_to_test = {} # a dictionary of the form {testpoint: bddleq}
        # we record bddleq for each testpoiont, since we want to restrict to lower dimensional cells when  goto_lower_dim is set to True.
        self.max_iter = max_iter
        if find_region_type is None:
            self.find_region_type = find_region_type_igp
        else:
            self.find_region_type = find_region_type
        self.default_var_bound = default_var_bound
        if bddbsa is None:
            self.bddbsa =  BasicSemialgebraicSet_eq_lt_le_sets(QQ, self.d)
        else:
            self.bddbsa = bddbsa

    def __repr__(self):
        return "SemialgebraicComplex with {} components".format(len(self.components))

    def generate_random_var_value(self, var_bounds=None):
        r"""
        Return a random point that satisfies var_bounds and is in self.bsa.

        - If var_bounds is not specified, self.default_var_bound is taken. 
        - var_bounds can be a list of 2-tuples whose length equals to the number of parameters, or lambda functions.
        - It is used in random shooting method for functions like ``dg_2_step_mir``, which involve floor/ceil operations. We try to plot one layer for each n = floor(...) and superimpose the layers at the end to get the whole picture.

        Notice that if self.bddbsa.eq_poly() is not empty, it never ends.

        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.WARN)
            sage: complex = SemialgebraicComplex(lambda x,y: max(x,y), ['x','y'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-10,10))
            sage: random_point = complex.generate_random_var_value()
            sage: all(complex.default_var_bound[0] < random_point[i] < complex.default_var_bound[1] for i in [0,1])
            True
            sage: var_bounds=[(0,1),((lambda x: x/2), (lambda x: x))]
            sage: random_point = complex.generate_random_var_value(var_bounds=var_bounds)
            sage: (0 < random_point[0] < 1) and (random_point[0]/2 < random_point[1] < random_point[0])
            True
        """
        while True:
            var_value = []
            for i in range(self.d):
                if not var_bounds:
                    x = QQ(uniform(self.default_var_bound[0], self.default_var_bound[1]))
                else:
                    if hasattr(var_bounds[i][0], '__call__'):
                        l =  var_bounds[i][0](*var_value)
                    else:
                        l = var_bounds[i][0]
                    if hasattr(var_bounds[i][1], '__call__'):
                        u =  var_bounds[i][1](*var_value)
                    else:
                        u = var_bounds[i][1]
                    if l > u:
                        x = None
                    else:
                        x = QQ(uniform(l, u))
                if x is None:
                    break
                var_value.append(x)
            # if random point is not in self.bddbsa, continue while.
            if (x is not None) and (x in self.bddbsa): #point_satisfies_bddleq_bddlin(var_value, self.bddleq, self.bddlin, strict=False):
                return var_value

    def is_point_covered(self, var_value):
        r"""
        Return whether the given point var_value is contained in any cell of the complex.

        Inequalities are considered strict.

        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.WARN)
            sage: complex = SemialgebraicComplex(lambda x,y: max(x,y), ['x','y'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-10,10))
            sage: complex.add_new_component([1,2], bddleq=[], flip_ineq_step=0, wall_crossing_method=None, goto_lower_dim=False) # the cell {(x,y): x<y}
            sage: complex.is_point_covered([2,3])
            True
            sage: complex.is_point_covered([3,2])
            False
            sage: complex.is_point_covered([2,2])
            False
            sage: complex.is_point_covered([sqrt(2), sqrt(3)])
            True
        """
        for c in self.cells_containing_point(var_value):
            return True
        return False

    def cells_containing_point(self, var_value):
        r"""
        Yield the cells of the complex that contain the given point var_value.

        Inequalities are considered strict.

        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.WARN)
            sage: complex = SemialgebraicComplex(lambda x,y: max(x,y), ['x','y'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-10,10))
            sage: complex.add_new_component([1,2], bddleq=[], flip_ineq_step=0, wall_crossing_method=None, goto_lower_dim=False) # the cell {(x,y): x<y}
            sage: cell = next(complex.cells_containing_point([2,3]))
            sage: cell.var_value
            [1, 2]
            sage: cell = next(complex.cells_containing_point([sqrt(2), sqrt(3)]))
            sage: cell.var_value
            [1, 2]
        """
        for c in self.components:
            if var_value in c.bsa: #point_satisfies_bddleq_bddlin(var_value, c.leq, c.lin, strict=True):
                yield c
        
    def find_uncovered_random_point(self, var_bounds=None, max_failings=10000):
        r"""
        Return a random point that satisfies the bounds and is uncovered by any cells in the complex.
        Return ``None`` if the number of attemps > max_failings.
 
        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.WARN)
            sage: complex = SemialgebraicComplex(lambda x,y: max(x,y), ['x','y'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-10,10))
            sage: complex.add_new_component([1,2], bddleq=[], flip_ineq_step=0, wall_crossing_method=None, goto_lower_dim=False) # the cell {(x,y): x<y}
            sage: var_value = complex.find_uncovered_random_point(max_failings=100)
            sage: complex.is_point_covered(var_value)
            False
        """
        num_failings = 0
        while not max_failings or num_failings < max_failings:
            if self.points_to_test:
                var_value = list(self.points_to_test.popitem()[0])
            else:
                var_value = self.generate_random_var_value(var_bounds=var_bounds)
            # This point is not already covered.
            if self.is_point_covered(var_value):
                num_failings += 1
            else:
                return var_value
        logging.warning("The complex has %s cells. Cannot find one more uncovered point by shooting %s random points" % (len(self.components), max_failings))
        return None

    def find_uncovered_point_mathematica(self, strict=True, bddleq=[], bddlin=[], bddstrict=True):
        r"""
        Call Mathematica's ``FindInstance`` to get a point that satisfies the bddleq and bddlin
        and is uncovered by any cells in the complex.

        The argument strict controles whehter inequalities are treated as <= 0 or as < 0.
        If such point does not exist, return ``None``.
 
        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.WARN)
            sage: complex = SemialgebraicComplex(lambda x,y: max(x,y), ['x','y'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-10,10))            # optional - mathematica
            sage: complex.add_new_component([1,2], bddleq=[], flip_ineq_step=0, wall_crossing_method=None, goto_lower_dim=False) # the cell {(x,y): x<y}                          # optional - mathematica
            sage: var_value = complex.find_uncovered_point_mathematica(strict=False)  # optional - mathematica
            sage: complex.is_point_covered(var_value)                   # optional - mathematica
            False
        """
        if not bddleq and not bddlin:
            condstr = write_mathematica_constraints(self.bddleq, self.bddlin, strict=True) #why strict = strict doesn't work when goto_lower_dim=False?
        else:
            condstr = write_mathematica_constraints(bddleq, bddlin, strict=bddstrict)
        for c in self.components:
            condstr_c = write_mathematica_constraints(c.bsa.eq_poly(), (c.bsa.lt_poly()).union(c.bsa.le_poly()), strict=strict)
            if condstr_c:
                condstr += '!(' + condstr_c[:-4] + ') && '
            else:
                # c.lin == [] and c.leq == [], cell covers the whole space.
                return None
        if not condstr:
            return tuple([0]*len(self.var_name))
        return find_instance_mathematica(condstr[:-4], self.var_name)

    def construct_field_and_test_point(self, var_value, bddleq=[]):
        K, test_point = construct_field_and_test_point(self.function, self.var_name, var_value, self.default_args)
        K.add_initial_space_dim() #so that the parameters self.var_name are the first ones in the monomial list. Needed for variable elimination.
        for l in bddleq:
            # need to put these equations in K, so call comparaison.
            if not l(*K.gens()) == 0:
                logging.warning("Test point %s doesn't satisfy %s == 0." % (var_value, l))
        return K, test_point

    def add_new_component(self, var_value, bddleq=[], flip_ineq_step=0, wall_crossing_method=None, goto_lower_dim=False, allow_dim_degeneracy=False):
        r"""
        Compute one proof cell around var_value. Append this cell to the complex.

        - bddleq defines the boundary equalities satisfied by the cell.
        - If flip_ineq_step = 0, do not search for neighbour testpoints. Used in ``shoot_random_points()``. wall_crossing_method = ``None`` in this case.
        - If flip_ineq_step > 0, search for neighbour testpoints using wall_crossing_method = 'mathematica' or 'heuristic' or 'heuristic_with_check'. Used in bfs. If goto_lower_dim is ``False`` or (goto_lower_dim is ``True`` and wall_crossing method = 'heuristic' but wall is non-linear), then find new testpoints across the wall only.

        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.WARN)
            sage: complex = SemialgebraicComplex(lambda x,y: max(x,y), ['x','y'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-10,10))
            sage: complex.add_new_component([1,2], bddleq=[], flip_ineq_step=1/10, wall_crossing_method='heuristic', goto_lower_dim=True) # the cell {(x,y): x<y}
            sage: complex.components[0].bsa.lt_poly()
            {x - y}
            sage: complex.points_to_test
            {(3/2, 3/2): [x - y], (31/20, 29/20): []}

            sage: complex = SemialgebraicComplex(lambda x,y: max(x,y^2), ['x','y'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-10,10))        # optional - mathematica
            sage: complex.add_new_component([1,1/2], bddleq=[], flip_ineq_step=1/10, wall_crossing_method='mathematica', goto_lower_dim=False) # the cell {(x,y): x > y^2}      # optional - mathematica
            sage: complex.components[0].lin                           # optional - mathematica
            [y^2 - x]
            sage: complex.points_to_test                              # optional - mathematica
            {(19/20, 1): []}
        """
        K, test_point = self.construct_field_and_test_point(var_value, bddleq)
        try:
            h = self.function(**test_point)
        except Exception: # Dangerous!!
            # Function is non-contructible at this random point.
            if debug_cell_exceptions:
                import pdb; pdb.post_mortem()
            h = None
        region_type = self.find_region_type(K, h)
        new_component = SemialgebraicComplexComponent(self, K, var_value, region_type)
        if not allow_dim_degeneracy and len(new_component.bsa.eq_poly()) != len(bddleq):
            for l in new_component.bsa.eq_poly():
                if not l in bddleq:
                    pert_value = tuple(var_value[i] + gradient(l)[i](var_value) / 1000 for i in range(len(var_value)))
                    if not pert_value in self.points_to_test:
                        self.points_to_test[pert_value] = copy(bddleq)
                    pert_value = tuple(var_value[i] - gradient(l)[i](var_value) / 1000 for i in range(len(var_value)))
                    if not pert_value in self.points_to_test:
                        self.points_to_test[pert_value] = copy(bddleq)
            logging.warning("The cell around %s defined by %s ==0 and %s <0 and %s <= 0 has more equations than bddleq %s" %(new_component.var_value, new_component.bsa.eq_poly(), new_component.bsa.lt_poly(),new_component.bsa.le_poly(), bddleq))
            return
        if (flip_ineq_step != 0) and (region_type != 'stop'):
            # when using random shooting, don't generate neighbour points; don't remove redundant walls.
            walls, new_points = new_component.find_walls_and_new_points(flip_ineq_step, wall_crossing_method, goto_lower_dim)
            if (wall_crossing_method == 'mathematica') or \
                (wall_crossing_method == 'heuristic_with_check'):
                new_component.bsa._lt = walls     # FIXME: Breaks abstraction
            self.points_to_test.update(new_points)
            new_component.neighbor_points = list(new_points.keys())
        self.components.append(new_component)

    def shoot_random_points(self, num, var_bounds=None, max_failings=1000):
        r"""
        Complete the complex by randomly shooting points.

        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.WARN)                   # not tested
            sage: complex = SemialgebraicComplex(lambda x,y: max(x,y), ['x','y'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-10,10))      # not tested
            sage: complex.shoot_random_points(100)                # not tested
            sage: complex.plot()                                  # not tested

            sage: complex = SemialgebraicComplex(lambda x,y: max(x,y^2), ['x','y'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-10,10))
            sage: complex.shoot_random_points(100)                # not tested
        """
        for i in range(num):
            var_value = self.find_uncovered_random_point(var_bounds=var_bounds, max_failings=max_failings)
            if var_value is None:
                return
            else:
                self.add_new_component(var_value, bddleq=[], flip_ineq_step=0, goto_lower_dim=False)

    def plot(self, alpha=0.5, plot_points=300, slice_value=None, restart=True, **kwds):
        r"""
        Plot the complex and store the graph.

        - If restart is ``False``, plot the newly added cells on top of the last graph; otherwise, start a new graph.
        - If slice_value is given, plot the slice of the complex according to the parameter values in slice_value that are not ``None``.
        - plot_points controls the quality of the plotting.

        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.WARN)
            sage: complex = SemialgebraicComplex(lambda x,y,z: min(x^2,y^2,z), ['x','y','z'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-10,10))    # not tested
            sage: complex.bfs_completion()                           # not tested

        Plot the slice in (x,y)-space with z=4::

            sage: complex.plot(slice_value=[None, None, 4])          # not tested

        Plot the slice in (y,z)-space with x=4::

            sage: complex.plot(slice_value=[4, None, None])          # not tested
        """
        if restart:
            self.graph = Graphics()
            self.num_plotted_components = 0
        self.graph.set_aspect_ratio(1)
        if 'xmin' in kwds:
            self.graph.xmin(kwds['xmin'])
        if 'xmax' in kwds:
            self.graph.xmax(kwds['xmax'])
        if 'ymin' in kwds:
            self.graph.ymin(kwds['ymin'])
        if 'ymax' in kwds:
            self.graph.ymax(kwds['ymax'])
        for c in self.components[self.num_plotted_components::]:
            gc = c.plot(alpha=alpha, plot_points=plot_points, slice_value=slice_value, **kwds)
            if gc: # need this because (empty g + empty gc) forgets about xmin xmax ymin ymax.
                self.graph += gc
        self.num_plotted_components = len(self.components)
        return self.graph

    def plot2dslice(self, slice_value, alpha=0.5, plot_points=300, **kwds):
        r"""
        slice_value is a list of symbolic expressions in var('x, y'). slice_value has the same length as self.var_value.

        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.WARN)
            sage: complex = SemialgebraicComplex(lambda x,y,z: min(x^2,y^2,z), ['x','y','z'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-10,10))    # not tested
            sage: complex.bfs_completion(goto_lower_dim=True)        # not tested
            sage: x, y = var('x, y')                                 # not tested

        Plot the slice in (x,y)-space with z=4::

            sage: complex.plot2dslice(slice_value=[x, y, 4])         # not tested

        Plot the slice in (y,z)-space with x=4::

            sage: complex.plot2dslice(slice_value=[4, x, y])         # not tested

        Plot the slice in (x,y)-space with z=y::

            sage: complex.plot2dslice(slice_value=[x, y, y])         # not tested

        Plot the slice in (x,z)-space with y=x/2::

            sage: complex.plot2dslice(slice_value=[x, x/2, y])       # not tested
        """
        g = Graphics()
        g.set_aspect_ratio(1)
        if 'xmin' in kwds:
            g.xmin(kwds['xmin'])
        if 'xmax' in kwds:
            g.xmax(kwds['xmax'])
        if 'ymin' in kwds:
            g.ymin(kwds['ymin'])
        if 'ymax' in kwds:
            g.ymax(kwds['ymax'])
        x, y = var('x, y')
        for c in self.components:
            gc = c.plot2dslice(slice_value, alpha=alpha, plot_points=plot_points, **kwds)
            if gc: # need this because (empty g + empty gc) forgets about xmin xmax ymin ymax.
                g += gc
        return g

    def plot_bfs_tree(self, **kwds):
        r"""
        Plot the bfs tree provided that the complex is 2-dimensional.

        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.WARN)
            sage: complex = SemialgebraicComplex(drlm_backward_3_slope, ['f','bkpt'])
            sage: complex.bfs_completion(var_value=[4/5,1/2],flip_ineq_step=1/20)    #long time
            sage: g = complex.plot_bfs_tree()
        """
        g = self.plot(**kwds)
        for i in range(len(self.components)):
            c = self.components[i]
            var_value = c.var_value
            for pt in c.neighbor_points:
                g += line([var_value, pt],color='black',linestyle=":")
                g += point([pt], color='black', size=5)
            for j in range(i):
                if tuple(var_value) in self.components[j].neighbor_points:
                    g += line([var_value, self.components[j].var_value],color='red',linestyle="-")
                    break
            g += point([var_value], color='red', size=15, zorder=20)
        return g

    def bfs_completion(self, var_value=None, flip_ineq_step=1/100, check_completion=False, wall_crossing_method='heuristic', goto_lower_dim=False, allow_dim_degeneracy=False, max_failings=0):
        r"""
        Breadth-first-search to complete the complex.

        - var_value: the starting point. If not given, start with a random point.
        - flip_ineq_step: a small positive number that controls the step length in wall-crossing.
        - check_completion: When check_completion is ``True``, after bfs terminates, check whether the entire parameter space is covered by cells, using Mathematica's ``FindInstance`` (if max_failings=0) or random shooting (if max_failings>0). If an uncovered point has been found, restart the bfs from this point.
        - wall_crossing_method: 'mathematica' or 'heuristic' or 'heuristic_with_check' 
              - wall_crossing_method='heuristic_with_check': if heuristic wall-crossing does not find a new testpoint, then use Mathematica to check if the ineq is not a wall).
        - goto_lower_dim: whether lower dimensional cells are considered. If goto_lower_dim is ``False`` or if goto_lower_dim is ``True`` and wall_crossing method is 'heuristic' but the wall is non-linear, then find new testpoint across the wall only.

        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.WARN)
            sage: complex = SemialgebraicComplex(lambda x,y: min(x^2+ 4*y^2, 4), ['x','y'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-3,3))    # optional - mathematica
            sage: complex.bfs_completion(check_completion=True, wall_crossing_method='mathematica', goto_lower_dim=True)                                                          # optional - mathematica
            sage: len(complex.components)                               # optional - mathematica
            3
            sage: complex.plot()                                        # not tested

            sage: complex = SemialgebraicComplex(lambda x,y: min(x+ 4*y, 4), ['x','y'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-5,5))
            sage: complex.bfs_completion(var_value=[1,1])
            sage: len(complex.components)
            2
            sage: complex.plot()                                        # not tested

        See more examples in the docstring of the class :class:`SemialgebraicComplex`.
        """
        if not self.points_to_test and not var_value:
            var_value = self.find_uncovered_random_point()
        if var_value:
            self.points_to_test[tuple(var_value)] = list(self.bddbsa.eq_poly())
        while self.points_to_test: # and len(self.components)<10: #FIXME
            var_value, bddleq = self.points_to_test.popitem()
            var_value = list(var_value)
            if not self.is_point_covered(var_value):
                self.add_new_component(var_value, bddleq=bddleq, flip_ineq_step=flip_ineq_step, wall_crossing_method=wall_crossing_method, goto_lower_dim=goto_lower_dim, allow_dim_degeneracy=allow_dim_degeneracy)
        if check_completion:
            if max_failings == 0:
                uncovered_pt = self.find_uncovered_point_mathematica(strict=goto_lower_dim)
            else: # assume that check_completion is an integer.
                uncovered_pt = self.find_uncovered_random_point(max_failings=max_failings)
            if uncovered_pt is not None:
                logging.warning("After bfs, the complex has uncovered point %s." % (uncovered_pt,))
                allow_dim_degeneracy = allow_dim_degeneracy and goto_lower_dim
                self.bfs_completion(var_value=uncovered_pt, \
                                    flip_ineq_step=flip_ineq_step, \
                                    check_completion=check_completion, \
                                    wall_crossing_method=wall_crossing_method, \
                                    goto_lower_dim=goto_lower_dim, \
                                    allow_dim_degeneracy=allow_dim_degeneracy)

    def is_complete(self, strict=False, bddleq=[], bddlin=[], bddstrict=True):
        r"""
        Return whether the entire parameter space satisfying bddleq and bddlin is covered by cells.

        EXAMPLES::

            sage: from cutgeneratingfunctionology.igp import *
            sage: logging.disable(logging.WARN)
            sage: complex = SemialgebraicComplex(lambda x,y: min(x+ 4*y, 4), ['x','y'], max_iter=0, find_region_type=result_symbolic_expression, default_var_bound=(-5,5))    # optional - mathematica
            sage: complex.bfs_completion(var_value=[1,1])           # optional - mathematica
            sage: complex.is_complete()                             # optional - mathematica
            True
            sage: complex.is_complete(strict=True)                  # optional - mathematica
            False
        """
        if self.find_uncovered_point_mathematica(strict=strict, bddleq=bddleq, bddlin=bddlin, bddstrict=bddstrict) is None:
            return True
        else:
            return False

    def is_polyhedral(self):
        for c in self.components:
            if not c.is_polyhedral():
                return False
        return True

    def subcomplex_of_cells_with_given_region_types(self, given_region_types={'is_extreme'}):
        subcomplex = copy(self)
        subset_components = [c for c in self.components if bool(c.region_type in given_region_types)]
        subcomplex.components = subset_components
        subcomplex.graph = Graphics()
        subcomplex.num_plotted_components = 0
        return subcomplex

    def subcomplexes_of_cells_with_given_region_types(self):
        """
        Return a dictionary mapping region types to subcomplexes.
        """
        region_types = set(c.region_type for c in self.components)
        return { region_type:
                 self.subcomplex_of_cells_with_given_region_types({region_type})
                 for region_type in region_types }

    def guess_boundary(self):
        extlin = [l for c in self.components if not c.bsa.eq_poly() for l in list(c.bsa.lt_poly()) + list(c.bsa.le_poly())]
        boundaries = set(extlin).difference(set([-l for l in extlin]))
        return list(boundaries)

    def is_face_to_face(self):
        sagepolyhedra = []
        for c in self.components:
            #p1 = construct_sage_polyhedron_from_nnc_polyhedron(c.polyhedron)
            p1 = c.sage_polyhedron()
            for p2 in sagepolyhedra:
                p = p1.intersection(p2)
                d = p.dimension()
                if d == -1: # empty
                    continue
                is_a_face = False
                for f in p1.faces(d):
                    if p == f.as_polyhedron():
                        is_a_face = True
                        break
                if not is_a_face:
                    return False
                is_a_face = False
                for f in p2.faces(d):
                    if p == f.as_polyhedron():
                        is_a_face = True
                        break
                if not is_a_face:
                    return False
            sagepolyhedra.append(p1)
        return True

    def discard_redundant_inequalities(self, flip_ineq_step=0):
        # TO UPDATE with bsa
        for c in self.components:
            c.discard_redundant_inequalities(flip_ineq_step=flip_ineq_step)

    def polyhedral_complex(self):
        r"""
        Assume that the cells in the :class:`SemialgebraicComplex` are polyhedral and face-to-face.
        Return the :class:`PolyhedralComplex`.
        """
        return PolyhedralComplex([c.sage_polyhedron() for c in self.components])

###########################################
# Helper functions for SemialgebraicComplex
###########################################
def gradient(ineq):
    r"""
    Return the gradient of the polynomial ineq.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: P.<x,y>=QQ[]
        sage: gradient(2*x^2*y+x^3+4*y+5)
        [3*x^2 + 4*x*y, 2*x^2 + 4]
        sage: P.<z>=QQ[]
        sage: gradient(z^3+3*z^2+1)
        [3*z^2 + 6*z]
    """
    if hasattr(ineq, 'gradient'):
       return ineq.gradient()
    else:
       return [ineq.derivative()]

def point_satisfies_bddleq_bddlin(var_value, bddleq, bddlin, strict=True):
    r"""
    Return whether var_value satisfies bddleq and bddlin.

    Strict inequalities are considered if strict is set to ``True``.

    Not used any more. Can delete
    """
    for l in bddleq:
        if not l(var_value) == 0:
            return False
    for l in bddlin:
        if l(var_value) > 0 or (strict and l(var_value)==0):
            return False
    return True

def is_value_in_interval(v, lb_ub):
    r"""
    Return whether lb <= v <= ub.

    ``None`` is considered as -Infinity and +Infinity for lb and ub, respectively. 
    """
    (lb, ub) = lb_ub
    if v is None:
        return (lb is None) or (ub is None) or (lb <= ub)
    return ((lb is None) or (lb <= v)) and ((ub is None) or (v <= ub))

def bounds_for_plotting(v, lb_ub, default_var_bound):
    r"""
    If lower and upper exist, then return them; otherwise return default variable bounds.
    """
    (lb, ub) = lb_ub
    if not lb is None:
        l = lb - 0.01
    else:
        l = default_var_bound[0]
    if not ub is None:
        u = ub + 0.01
    else:
        u = default_var_bound[1]
    if l >= u:
        return (v, default_var_bound[0], default_var_bound[1])
    return (v, l, u)

def construct_mip_of_nnc_polyhedron(nncp):
    r"""
    Construct a PPL's :class:`MIP_Problem` with non-strict inequalities from the :class:`NNC_Polyhedron`.
    """
    min_cs = nncp.minimized_constraints()
    cs = Constraint_System()
    for c in min_cs:
        if c.is_equality():
            cs.insert(Linear_Expression(c.coefficients(), c.inhomogeneous_term()) == 0)
        else:
            cs.insert(Linear_Expression(c.coefficients(), c.inhomogeneous_term()) >= 0)
    mip = MIP_Problem(nncp.space_dimension())
    mip.add_constraints(cs)
    mip.set_optimization_mode('minimization')
    return mip

def construct_sage_polyhedron_from_nnc_polyhedron(nncp):
    r"""
    Construct a Sage's (closed) Polyhedron from PPL's :class:`NNC_Polyhedron`.
    Not used. Can delete
    """
    min_cs = nncp.minimized_constraints()
    ieqs = [ ([c.inhomogeneous_term()]+list(c.coefficients())) for c in min_cs if not c.is_equality()]
    eqns = [ ([c.inhomogeneous_term()]+list(c.coefficients())) for c in min_cs if c.is_equality()]
    return Polyhedron(ieqs=ieqs, eqns=eqns)

def find_bounds_of_variable(mip, i):
    r"""
    Return the lower and upper bounds of the i-th variable in the MIP.

    ``None`` stands for unbounded.
    """
    linexpr = Linear_Expression(Variable(i))
    lb = find_lower_bound_of_linexpr(mip, linexpr)
    ub = find_upper_bound_of_linexpr(mip, linexpr)
    return (lb, ub)

def find_lower_bound_of_linexpr(mip, linexpr):
    r"""
    Return the minimal value of linexpr subject to mip.

    Return ``None`` if unbounded.
    Assume that ``mip.set_optimization_mode('minimization')`` was called
    """
    mip.set_objective_function(linexpr)
    try:
        lb = QQ(mip.optimal_value())
    except ValueError:
        # unbounded
        lb = None
    return lb

def find_upper_bound_of_linexpr(mip, linexpr):
    r"""
    Return the maximal value of linexpr subject to mip.
 
    Return ``None`` if unbounded.
    Assume that ``mip.set_optimization_mode('minimization')`` was called
    """
    mip.set_objective_function(-linexpr)
    try:
        ub = -QQ(mip.optimal_value())
    except ValueError:
        # unbounded
        ub = None
    return ub

def is_not_a_downstairs_wall(c, mip):
    r"""
    Return whether a PPL constraint c is always strictly positive in mip.
    """
    linexpr = Linear_Expression(c.coefficients(), c.inhomogeneous_term())
    # we know lb exists and is >= 0
    lb = find_lower_bound_of_linexpr(mip, linexpr)
    return bool(lb >  0)

def add_mccormick_bound(mip, x3, x1, x2, c1, c2, is_lowerbound):
    r"""
    Try adding x3 > c1*x1 + c2*x2 - c1*c2 (if is_lowerbound, else x3 < c1*x1 + c2*x2 - c1*c2) to mip.
    Return True this new constraint is not redundnant.
    """
    if c1 is None or c2 is None:
        # unbounded
        return False
    d = c1.denominator() * c2.denominator() #linear expression needs integer coefficients
    linexpr = Linear_Expression(d*x3 - d*c1*x1 - d*c2*x2 + d*c1*c2)
    if is_lowerbound:
        lb = find_lower_bound_of_linexpr(mip, linexpr)
        if (lb is not None) and (lb >= 0):
            return False
        else:
            mip.add_constraint(linexpr >= 0)
            return True
    else:
        ub = find_upper_bound_of_linexpr(mip, linexpr)
        if (ub is not None) and (ub <=0):
            return False
        else:
            mip.add_constraint(linexpr <= 0)
            return True

def update_mccormicks_for_monomial(m, tightened_mip, monomial_list, v_dict, bounds, new_monomials_allowed=False):
    r"""
    Do recursive McCormicks on the monomial m.

    If bounds is modified, update tightened_mip of the cell and return ``True``, otherwise return ``False``.

    If lift_polyhedron is ``None``, recursive McCormicks is not allowed to create new monomials,
    otherwise, lift the dimension of the polyhedron and tightened_mip, etc. of the cell when new monomials are created.

    Expect that the monomials in monomial_list have non-decreasing degrees.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: mip = MIP_Problem(3)
        sage: vx = Variable(0); vy = Variable(1); vxy = Variable(2)
        sage: mip.add_constraint(vx >= 0); mip.add_constraint(vx <= 1)
        sage: mip.add_constraint(vy >= 1); mip.add_constraint(vy <= 2)
        sage: mip.set_optimization_mode('minimization')
        sage: P.<x,y> = QQ[]
        sage: monomial_list = [x, y, x*y]; v_dict = {x:0, y:1, x*y:2}
        sage: bounds = [(0, 1), (1, 2), (None, None)]

    Upward bounds propagation::

        sage: update_mccormicks_for_monomial(x*y, mip, monomial_list, v_dict, bounds)
        True
        sage: bounds
        [(0, 1), (1, 2), (0, 2)]
        sage: update_mccormicks_for_monomial(x*y, mip, monomial_list, v_dict, bounds)
        False

        sage: mip.add_space_dimensions_and_embed(1); mip.add_constraint(2*Variable(3) >= 1);
        sage: monomial_list.append(x*y^2); v_dict[x*y^2]=3; bounds.append((1/2, None));
        sage: monomial_list
        [x, y, x*y, x*y^2]
        sage: bounds
        [(0, 1), (1, 2), (0, 2), (1/2, None)]

        sage: update_mccormicks_for_monomial(x*y*y, mip, monomial_list, v_dict, bounds)
        True
        sage: bounds
        [(0, 1), (1, 2), (0, 2), (1/2, 4)]

    Downward bounds propagation::

        sage: bounds = [find_bounds_of_variable(mip,i) for i in range(4)]
        sage: bounds
        [(1/8, 1), (1, 2), (1/4, 2), (1/2, 4)]
    """
    if m.degree() < 2:
        return False
    i = v_dict[m]
    v = Variable(i)
    tightened = False
    for v1 in monomial_list:
        (v2, rem) = m.quo_rem(v1)
        if rem != 0 or v1 > v2:
            # don't want the recursive McCormicks to create a new monomial.
            # v1, v2 symmetric
            continue
        i_1 = v_dict[v1]
        i_2 = v_dict.get(v2, None)
        if (i_2 is None):
            continue
        v_1 = Variable(i_1)
        v_2 = Variable(i_2)
        lb_1, ub_1 = bounds[i_1]
        lb_2, ub_2 = bounds[i_2]
        if add_mccormick_bound(tightened_mip, v, v_1, v_2, lb_2, lb_1, True):
            tightened = True
        if add_mccormick_bound(tightened_mip, v, v_1, v_2, ub_2, ub_1, True):
            tightened = True
        if add_mccormick_bound(tightened_mip, v, v_1, v_2, lb_2, ub_1, False):
            tightened = True
        if add_mccormick_bound(tightened_mip, v, v_1, v_2, ub_2, lb_1, False):
            tightened = True
    if tightened:
        bounds[i] = find_bounds_of_variable(tightened_mip, i)
    return tightened

####################################
# Find region type and region color
####################################

def find_region_type_igp(K, h, region_level='extreme', is_minimal=None):
    r"""
    Find the type of a igp function h in the :class:`ParametricRealField` K;
    (is it constructible? is it minimal? is it extreme?)
    Record the comparisons in K.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: logging.disable(logging.INFO)
        sage: K.<f> = ParametricRealField([4/5])
        sage: h = gmic(f, field=K)
        sage: find_region_type_igp(K, h)
        'is_extreme'
        sage: K.get_lt_factor()
        {-f, -f + 1/2, f - 1}

        sage: K.<f,bkpt>=ParametricRealField([1/7,3/7])
        sage: h = drlm_backward_3_slope(f, bkpt, field=K)
        sage: find_region_type_igp(K, h)
        'not_extreme'
        sage: K.get_lt_factor()
        {2*bkpt - 1,
         -f,
         -f + 2*bkpt - 1,
         f - 4*bkpt + 1,
         f - 3*bkpt + 1,
         f - bkpt,
         2*f - 1,
         2*f - bkpt}
    """
    ## Note: region_level = 'constructible' / 'minimal'/ 'extreme'. test cases see find_parameter_region()
    #if hasattr(K, '_big_cells') and K._big_cells:
    #    return find_region_type_igp_extreme_big_cells(K, h)
    if h is None:
        return 'not_constructible'
    if region_level == 'constructible':
        return 'is_constructible'
    if is_minimal is None:
        is_minimal = minimality_test(h, full_certificates=False)
    if is_minimal:
        if region_level == 'minimal':
            return 'is_minimal'
        generator = generate_perturbations(h, full_certificates=False)
        for perturbation in generator:
            return 'not_extreme'
        return 'is_extreme'
    else:
        return 'not_minimal'

def find_region_type_igp_extreme(K, h):
    if find_region_type_igp(K, h) == 'is_extreme':
        return 'is_extreme'
    else:
        return 'stop'

def find_region_type_igp_extreme_big_cells(K, h):
    hcopy = copy(h)
    if h is None:
        return 'not_constructible'
    is_extreme = True
    with K.off_the_record():
        for x in h.values_at_end_points():
            if (x < 0) or (x > 1):
                is_extreme  = False
                break
    if not is_extreme:
        assert (x < 0) or (x > 1)
        return False
    f = find_f(h, no_error_if_not_minimal_anyway=True)
    if f is None:
        return False
    bkpt = h.end_points()
    # if not h.is_continuous():
    #     with K.off_the_record():
    #         limits = h.limits_at_end_points()
    #         for x in limits:
    #             if not ((x[-1] is None or 0 <= x[-1] <=1) and (x[1] is None or 0 <= x[1] <=1)):
    #                 is_extreme = False
    #                 break
    #     if not is_extreme:
    #         assert (not ((x[-1] is None or 0 <= x[-1] <=1) and (x[1] is None or 0 <= x[1] <=1))):
    #         return False
    with K.off_the_record():
        for (x, y, z, xeps, yeps, zeps) in generate_nonsubadditive_vertices(h, reduced=True):
            is_extreme = False
            break
    if not is_extreme:
        assert delta_pi_general(h, x, y, (xeps, yeps, zeps)) < 0
        return False
    with K.off_the_record():
        if h(f) != 1:
            is_extreme = False
    if not is_extreme:
        assert h(f) != 1
        return False
    with K.off_the_record():
        for (x, y, xeps, yeps) in generate_nonsymmetric_vertices(h, f):
            is_extreme = False
            break
    if not is_extreme:
        #assert h.limit(x,xeps)+h.limit(y,yeps) != 1
        assert h(x)+h(y) != 1
        return False
    # function is minimal.
    with K.off_the_record():
        num_slope = number_of_slopes(h)
    if h.is_continuous() and num_slope == 2:
        # is_extreme  #record #shortcut?
        minimality_test(h, full_certificates=False)
        return True
    with K.off_the_record():
        generator = generate_perturbations(h)
        for perturbation in generator:
            # epsilon_interval = find_epsilon_interval(h, perturbation)
            # epsilon = min(abs(epsilon_interval[0]), abs(epsilon_interval[1]))
            # hplus = h + perturbation * epsilon/2
            # hminus = h - perturbation * epsilon/2
            # # alternatively, should record (x,y) in refined complex for which Delta perturbation(x,y) > 0, then later assert Delta h (x,y)>0
            strictsubaddxy = [(x,y) for (x,y,z,xeps,yeps,zeps) in generate_nonsubadditive_vertices(perturbation)+generate_nonsubadditive_vertices(-perturbation)]
            is_extreme = False
            break
    if not is_extreme:  # ignore discontinuous case for now
        # for hh in [hplus, hminus]:
        #     bkpt = hh.end_points()
        #     bkpt2 = bkpt[:-1] + [ x+1 for x in bkpt ]
        #     num = len(bkpt)
        #     for j in range(num):
        #         for i in range(j):
        #             x = bkpt[i]
        #             y = bkpt[j]
        #             assert (delta_pi(hh,x,y) >= 0)
        #     for i in range(num):
        #         for j in range(i+1, i+num-1):
        #             x = bkpt[i]
        #             z = bkpt2[j]
        #             assert (delta_pi(hh, x, z-x) >= 0)
        h = copy(hcopy)
        for (x,y) in strictsubaddxy:
            assert(delta_pi(h, x, y) > 0)  # record
        return False
    # is_extreme
    is_minimal = minimality_test(h, full_certificates=False)
    assert is_minimal
    # # BUG: why it does not record??? Too many cached things?
    # if hasattr(h,'_perturbations'):
    #     delattr(h, '_perturbations')
    # if hasattr(h,'_completion'):
    #     delattr(h, '_completion')
    # if hasattr(h, '_stability_orbits'):
    #     delattr(h, '_stability_orbits')
    # if hasattr(h, '_maximal_additive_faces'):
    #     delattr(h, '_maximal_additive_faces')
    # if hasattr(h, '_directly_covered_components'):
    #     delattr(h, '_directly_covered_components')
    # if hasattr(h, '_strategical_covered_components'):
    #     delattr(h, '_strategical_covered_components')
    h = copy(hcopy)
    generator = generate_perturbations(h, full_certificates=False)
    for perb in generator:
        raise ValueError
    return True
    

def coarse_regions_from_arrangement_of_bkpts(K, h):
    if h is None:
        return 'not_constructible'
    comparison = lambda a, b: True
    grid_vertices = unique_list(itertools.chain(generate_type_1_vertices(h, comparison), generate_type_2_vertices(h, comparison)))
    for (x, y, z, xeps, yeps, zeps) in grid_vertices:
        d = delta_pi_general(h, x, y, (xeps, yeps, zeps))
    return 'is_constructible'

def claimed_region_type(igp_function=gmic, condition_according_to_literature=True, **kwds):
    r"""
    Return if igp_function is 'not_constructible' or 'constructible' or 'extreme' for the values of parameters given by kwds (use default values if kwds is not provided).

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: logging.disable(logging.INFO)
        sage: claimed_region_type(igp_function=chen_4_slope)
        'extreme'
        sage: claimed_region_type(igp_function=chen_4_slope, condition_according_to_literature=True, f=1/2, s_pos=5, s_neg=-5, lam1=1/5, lam2=1/5)
        'constructible'
        sage: claimed_region_type(igp_function=chen_4_slope, condition_according_to_literature=True, f=7/10, s_pos=2, s_neg=-4, lam1=1/100, lam2=49/100)
        'extreme'
        sage: claimed_region_type(igp_function=chen_4_slope, condition_according_to_literature=False, f=7/10, s_pos=2, s_neg=-4, lam1=1/100, lam2=49/100)
        'constructible'

    The following examples show how claimed_region_type can be used in computing the complex of igp_function. The cells of the complex represent the regions where igp_function is 'extreme', 'constructible' or 'not_constructible' according to the claimed extremality conditions for igp_function::

        sage: complex = SemialgebraicComplex(claimed_region_type, ['f','bkpt'], find_region_type=return_result, igp_function=drlm_backward_3_slope)
        sage: complex.bfs_completion(var_value=[4/5,1/2])
        sage: [c.region_type for c in complex.cells_containing_point([1/12,1/6])]
        ['extreme']

        sage: complex = SemialgebraicComplex(claimed_region_type, ['lam1', 'lam2'], find_region_type=return_result, igp_function=chen_4_slope, condition_according_to_literature=True)
        sage: complex.bfs_completion(var_value=[3/10, 45/101])
        sage: [c.region_type for c in complex.cells_containing_point([1/100,49/100])]
        ['extreme']

        sage: complex = SemialgebraicComplex(claimed_region_type, ['lam1', 'lam2'], find_region_type=return_result, igp_function=chen_4_slope, condition_according_to_literature=False)
        sage: complex.bfs_completion(var_value=[3/10, 45/101])
        sage: [c.region_type for c in complex.cells_containing_point([1/100,49/100])]
        ['constructible']

        sage: complex = SemialgebraicComplex(claimed_region_type, ['lam1', 'lam2'], find_region_type=return_result, igp_function=chen_4_slope, condition_according_to_literature=False, kwds_dict={'f':1/2, 's_pos':5, 's_neg':-5})
        sage: complex.bfs_completion(var_value=[1/5, 1/4])
        sage: [c.region_type for c in complex.cells_containing_point([1/5,1/5])]
        ['extreme']

        sage: complex = SemialgebraicComplex(claimed_region_type,['f','alpha'],find_region_type=return_result, igp_function=dg_2_step_mir)
        sage: complex.bfs_completion(var_value=[4/5,3/10]) #not tested #infinite many cells.
    """
    test_point = read_default_args(igp_function)
    test_point.update(kwds)
    # make condition_according_to_literature a keyword argument of the function claimed_region_type,
    # update its value in test_point.
    # in particular, use condition_according_to_literature=True to obtain the (false) claimed region of chen_4_slope according to literature.
    if 'condition_according_to_literature' in test_point:
        test_point['condition_according_to_literature'] = condition_according_to_literature
    if not isinstance(igp_function, ExtremeFunctionsFactory):
        try:
            h = igp_function(**test_point)
            return h._claimed_parameter_attribute
        except: # Dangerous!!
            # Function is non-contructible at this random point.
            return 'not_constructible'
    else:
        claimed_parameter_attribute = igp_function.claimed_parameter_attributes
        parameter_values = read_default_args(claimed_parameter_attribute, **test_point)
        return claimed_parameter_attribute(**parameter_values)

def return_result(field, result):
    return result

def result_concrete_value(field, result):
    r"""
    Return the concrete values in result as a tuple. See also ``result_symbolic_expression()``.
 
    This function can provided to ``find_region_type`` when setting up a :class:`SemialgebraicComplex`. 
    In this way, one can compare result of type :class:`ParametricRealFieldElement` or list of :class:`ParametricRealFieldElement`
    with the previous elements in ``region_type_color_map`` which do not necessarily have the same parent.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: logging.disable(logging.WARN)
        sage: def vol(a,b):
        ....:     P = Polyhedron(ieqs=[(1,0,-1),(0,0,1),(1,-1,0),(0,1,0),(1,-a,-b)])
        ....:     return P.volume()
        sage: K.<a,b>=ParametricRealField([2,3])
        sage: result = vol(a,b)
        sage: result_concrete_value(K, result)
        (1/12,)
    """
    concrete_value = tuple(elt.val() if hasattr(elt, 'val') else elt for elt in flatten([result]))
    return concrete_value

def result_symbolic_expression(field, result):
    r"""
    Return the symbolic expressions in result as a tuple
 
    This function can provided to ``find_region_type`` when setting up a :class:`SemialgebraicComplex`. 
    In this way, one can compare result of type :class:`ParametricRealFieldElement` or list of :class:`ParametricRealFieldElement`
    with the previous elements in ``region_type_color_map`` which do not necessarily have the same parent.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: logging.disable(logging.WARN)
        sage: def vol(a,b):
        ....:     P = Polyhedron(ieqs=[(1,0,-1),(0,0,1),(1,-1,0),(0,1,0),(1,-a,-b)])
        ....:     return P.volume()
        sage: K1.<a,b>=ParametricRealField([2,3])
        sage: vol1 = vol(a,b)
        sage: sym_exp1 = result_symbolic_expression(K1, vol1)
        sage: sym_exp1
        (1/(2*a*b),)
        sage: K2.<a,b>=ParametricRealField([5,4])
        sage: vol2 = vol(a,b)
        sage: sym_exp2 = result_symbolic_expression(K2, vol2)
        sage: sym_exp2
        (1/(2*a*b),)
        sage: vol1 == vol2
        False
        sage: sym_exp1 == sym_exp2
        True    
    """
    symbolic_expression = tuple(elt._sym if hasattr(elt, '_sym') else elt for elt in flatten([result]))
    return symbolic_expression

region_type_color_map = [('not_constructible', 'white'), ('is_constructible', 'black'), ('not_minimal', 'orange'), ('is_minimal', 'darkgrey'),('not_extreme', 'green'), ('is_extreme', 'blue'), ('stop', 'grey'), (True, 'blue'), (False, 'red'), ('constructible', 'darkgrey'), ('extreme', 'red')]

def find_region_color(region_type):
    r"""
    Return the color of the region according to the global dictionary ``region_type_color_map``.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: find_region_color('is_extreme')
        'blue'
        sage: find_region_color(False)
        'red'
    """
    # if region_type is a color, return directly.
    if region_type in colors:
        return region_type
    # Assume that there will be at most 7 different types other than the ones like 'is_extreme' that were in region_type_color_map.
    global region_type_color_map
    n = len(region_type_color_map)
    i = 0
    while (i < n) and (region_type != region_type_color_map[i][0]):
        i += 1
    if i == n:
        region_color = color_of_ith_region_type(n - 9)  # the initial map includes 9 igp region types.
        region_type_color_map.append((region_type, region_color))
    else:
        region_color = region_type_color_map[i][1]
    return region_color

def color_of_ith_region_type(i):
    r"""
    Return a color in the rainbow.
    """
    j = (4 * i) % 7
    c = rainbow(7)[j]
    return c


##########################
# wall crossing heuristic
##########################

def find_point_flip_ineq_heuristic(current_var_value, ineq, ineqs, flip_ineq_step):
    r"""
    The current_var_value satisfies that l(current_var_value)<0 for l=ineq or l in ineqs,
    where ineq is a polynomial and ineqs is a list of polynomials.

    Use heuristic method (gradient descent method with given small positive step length flip_ineq_step)
    to find a new_point (type is tuple) such that 
    ineq(new_point) > 0 and l(new_point) < 0 for all l in ineqs.
    Return new_point, or ``None`` if it fails to find one.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: P.<a,b>=QQ[]
        sage: find_point_flip_ineq_heuristic([1,1/2], a+b-2, [-a+b^2], 1/4)
        (11/8, 7/8)

    After walking towards ineq==0, ineqs < 0 is violated. Need to adjust::

        sage: find_point_flip_ineq_heuristic([1,9/10], a+b-2, [-a+b^2], 1/2)
        (123/85, 179/170)
        sage: find_point_flip_ineq_heuristic([11/40,1/2], a+b-2, [-a+b^2], 1/4)
        (39295901/31739294, 125037049/123564610)

    Ineq is a redundant inequality, it's impossible to cross it without crossing any other ineqs.
    Thus, return ``None``::

        sage: find_point_flip_ineq_heuristic([1,1/2], a+b-2, [-a+b^2, a-1], 1/4)
    """
    # heuristic method.
    ineq_gradient = gradient(ineq)
    current_point = vector(RR(x) for x in current_var_value) # Real numbers, faster than QQ
    ineq_value = ineq(*current_point)
    try_before_fail = 10000 # define maximum number of walks.
    while (ineq_value <= 0) and (try_before_fail > 0):
        ineq_direction = vector(g(*current_point) for g in ineq_gradient)
        if ineq.degree() == 1:
            step_length = (-ineq(*current_point)+flip_ineq_step) / (ineq_direction * ineq_direction)
        else:
            step_length = flip_ineq_step / (ineq_direction * ineq_direction) # ineq_value increases by flip_ineq_step=0.01 roughly
            if step_length > 1:
                step_length = 1  # ensure that distance of move <= sqrt(flip_ineq_step) = 0.1 in each step
        current_point += step_length * ineq_direction
        new_ineq_value = ineq(*current_point)
        if new_ineq_value <= ineq_value:
            return None
        ineq_value = new_ineq_value
        try_before_fail -= 1
        #print current_point, RR(ineq_value)
    if ineq_value <= 0:
        return None
    new_point = adjust_pt_to_satisfy_ineqs(current_point, ineq, ineqs, flip_ineq_step)
    # if new_point is not None and ineq(*new_point) <= 0:
    #     #logging.info("Didn't add %s because it violates %s > 0" % (new_point, ineq))
    #     return None
    return new_point #type is tuple


def find_point_on_ineq_heuristic(current_var_value, ineq, ineqs, flip_ineq_step):
    r"""
    The current_var_value satisfies that l(current_var_value)<0 for l=ineq or l in ineqs,
    where ineq is a polynomial and ineqs is a list of polynomials.

    Assume that ineq is linear.

    Use heuristic method (gradient descent method with given small positive step length flip_ineq_step)
    to find a new_point (type is tuple) such that
    ineq(new_point) == 0 and l(new_point) < 0 for all l in ineqs.
    Return new_point, or ``None`` if it fails to find one.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: P.<a,b>=QQ[]
        sage: find_point_on_ineq_heuristic([1,1/2], a+b-2, [-a+b^2], 1/4)
        (5/4, 3/4)
        sage: find_point_on_ineq_heuristic([11/40,1/2], a+b-2, [-a+b^2], 1/4)
        (171073319/163479120, 155884921/163479120)
    """
    ineq_gradient = gradient(ineq)
    current_point = vector(current_var_value)
    ineq_direction = vector(g(*current_point) for g in ineq_gradient)
    step_length = -ineq(*current_point) / (ineq_direction * ineq_direction)
    current_point += step_length * ineq_direction
    ineq_value = ineq(*current_point)
    if ineq_value != 0:
        return None
    new_point = adjust_pt_to_satisfy_ineqs(current_point, ineq, ineqs, flip_ineq_step)
    if new_point is not None and ineq(*new_point) != 0:
        #logging.info("Didn't add %s because it violates %s == 0" % (new_point, ineq))
        return None
    return new_point #type is tuple

def adjust_pt_to_satisfy_ineqs(current_point, ineq, ineqs, flip_ineq_step):
    r"""
    Walk from current_point (type=vector) in the direction perpendicular to 
    the gradient of ineq with small positive step length flip_ineq_step, 
    while maintaining ineq(*current_point) >= 0
    until get a new point such that l(new point)<0 for any l in ineqs.

    Return new_point, or ``None`` if it fails to find one.

    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: P.<a,b>=QQ[]
        sage: ineq = a+b-2
        sage: adjust_pt_to_satisfy_ineqs(vector([13/10,12/10]), ineq, [-a+b^2], 1/2)
        (123/85, 179/170)
        sage: adjust_pt_to_satisfy_ineqs(vector([71/80, 89/80]), ineq, [-a+b^2], 1/4)
        (171073319/163479120, 155884921/163479120)

    If impossible, return ``None``::

        sage: adjust_pt_to_satisfy_ineqs(vector([11/8, 7/8]), ineq,[-a+b^2, a-1], 1/4)
    """
    #current_point is a vector
    ineq_gradient = gradient(ineq)
    max_walks = min(ceil(2/flip_ineq_step), 1000) # define maximum number of walks.
    for l in ineqs:
        l_gradient = gradient(l)
        l_value = l(*current_point)
        try_before_fail = max_walks
        while (l_value >= 0) and (try_before_fail > 0):
            l_direction = vector(-g(*current_point) for g in l_gradient) #decrease l_value
            ineq_direction = vector(g(*current_point) for g in ineq_gradient)
            s = (ineq_direction * l_direction) / (ineq_direction * ineq_direction)
            projected_direction = l_direction - s * ineq_direction # want that ineq_value remains the same
            if projected_direction == 0:
                return None
            if l.degree() == 1:
                step_length = (l_value+flip_ineq_step) / (projected_direction * l_direction)
            else:
                step_length = flip_ineq_step / (projected_direction * l_direction) # l_value decreases by 0.01 roughly
                # if step_length * norm(projected_direction) >= 1:  # move too far  # is 1 a good value here?? why this if?
                #     return None
            #flip_ineq_step = flip_ineq_step / 2
            current_point += step_length * projected_direction
            l_value = l(*current_point)
            try_before_fail -= 1
            #print current_point, RR(l_value)
        if (l_value >= 0) or (ineq(*current_point) < 0):
            return None
    for l in ineqs:
        if l(*current_point) >= 0:
            return None
    return tuple(QQ(x) for x in current_point)

################################################
#  Is the given function contained in a family?
################################################

def embed_function_into_family(given_function, parametric_family, check_completion=False, **opt):
    r"""
    EXAMPLES::

        sage: from cutgeneratingfunctionology.igp import *
        sage: logging.disable(logging.WARN)
        sage: embed_function_into_family(gmic(3/13), mlr_cpl3_a_2_slope)
        {'r0': 3/13, 'z1': 3/26}
        sage: given_function = drlm_backward_3_slope(1/12-1/100, 1/6+1/100)
        sage: embed_function_into_family(given_function, drlm_backward_3_slope)
        {'bkpt': 53/300, 'f': 11/150}
        sage: embed_function_into_family(gmic(4/13), mlr_cpl3_a_2_slope)
        {'r0': 4/13, 'z1': 3/26}
        sage: embed_function_into_family(gmic(4/13), drlm_backward_3_slope)
        {}
        sage: embed_function_into_family(gmic(4/13), drlm_backward_3_slope, check_completion=True)  # optional - mathematica
        {}

        sage: given_function = mlr_cpl3_b_3_slope(r0=3/26, z1=1/13)
        sage: parametric_family = drlm_backward_3_slope
        sage: param_values = embed_function_into_family(given_function, parametric_family)
        sage: param_values
        {'bkpt': 7/26, 'f': 3/26}
        sage: given_function == parametric_family(**param_values)
        True

        sage: given_function = automorphism(cpl3_8(f=3/5, z1=1/25, z2=1/125))
        sage: parametric_family = gj_forward_3_slope
        sage: embed_function_into_family(given_function, parametric_family, check_completion=True) # optional - mathematica
        {'f': 2/5, 'lambda_1': 6/25, 'lambda_2': 2/75}
    """
    default_args = read_default_args(parametric_family)
    var_name = []
    var_value = []
    for (name, value) in default_args.items():
        if not isinstance(value, bool) and not value is None:
            try:
                RR(value)
                var_name.append(name)
                var_value.append(value)
            except:
                pass
    def frt(K, h):
        if h is None:
            return False
        else:
            return h == given_function
    complex = SemialgebraicComplex(parametric_family, var_name, find_region_type=frt)
    # terminate complex.bfs_completion(var_value=var_value, goto_lower_dim=True) immediately when a cell has region_type == True.
    complex.points_to_test[tuple(var_value)] = []
    flip_ineq_step = opt.pop('flip_ineq_step', 1/1000)
    is_complete = False
    while not is_complete:
        while complex.points_to_test:
            var_value, bddleq = complex.points_to_test.popitem()
            var_value = list(var_value)
            if not complex.is_point_covered(var_value):
                complex.add_new_component(var_value, bddleq=bddleq, goto_lower_dim=True, flip_ineq_step=flip_ineq_step, **opt)
                if complex.components and complex.components[-1].region_type is True:
                    dic = {var_name[i]:var_value[i] for i in range(len(var_name))}
                    return dic
        if check_completion:
            var_value = complex.find_uncovered_point_mathematica(strict=True)
            if not var_value:
                is_complete = True
            else:
                complex.points_to_test[var_value]=[]
                opt[allow_dim_degeneracy] = True
        else:
            is_complete = True
    # plot_cpl_components(complex.components)
    return {}
