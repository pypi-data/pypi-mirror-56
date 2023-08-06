import logging
import operator
from functools import reduce
import typing

import numpy as np
import pandas as pd
from lark import Lark, Token, Tree

from ._simulator import TimeSeries

LOG = logging.getLogger(__name__)


# todo implement combinations modifier
# todo implement a doseresponse keyword
# todo implement a steady state keyword
# todo implement the qualitative profile stuff

class Parser:
    """
    Defines the grammar of the input language, parses the
    user input using lark and dynamically interprets the language
    by creating all the relevant objects for the comparison.
    """
    grammar = """
    start                  : block+
    ?block                  : timeseries_block  
                            | steadystate_block
                            | observation_block 
    timeseries_block        : "timeseries" NAME "{" ts_arg_list "}" START "," STOP "," STEP
    steadystate_block       : "steadystate" NAME "{" ts_arg_list "}" 
    ?ts_arg_list            : (ts_arg [","])*
    ?ts_arg                 : NAME "=" FLOAT 
                            | NAME "=" DIGIT+
                            
    
    observation_block                   : "observation" statement+
    ?statement                          : comparison_statement | behavioural_statement
    ?comparison_statement               : comparison_statement_with_func 
                                        | comparison_statement_without_func
    ?comparison_statement_with_func     : OBS_NAME ":" function_type1 "("clause1 OPERATOR clause2")"
    ?comparison_statement_without_func  : OBS_NAME ":" clause1 OPERATOR clause2
    behavioural_statement               : OBS_NAME ":" qual_exp 
    
    
    clause1                 : clause_with_func | clause_without_func
    clause2                 : clause_with_func | clause_without_func
    clause_with_func        : function_type2 "(" expression ")"
    clause_without_func     : expression
    
    ?expression             : term ((ADD|SUB) term)*
    ?term                   : factor ((MUL
                                      |DIV 
                                      |MOD
                                      |FLOOR) factor)*
    ?factor                 : ("+"|"-") factor 
                            | atom
                            | power
    ?power                  : atom "**" factor
    ?atom                   : NUMBER 
                            | NAME
                            | model_entity
    
    ?model_entity           : NAME "[" CONDITION "]" [_TIME_SYMBOL (POINT_TIME| INTERVAL_TIME)] 
    ?function_type1         : FUNC_TYPE1
    ?function_type2         : FUNC_TYPE2
    ?qual_exp               : SHAPE [DIRECTION] model_entity
    
    SHAPE                   : "hyperbolic"
                            | "transient"
                            | "sigmoidal"
                            | "oscillation"
    DIRECTION               : "up" 
                            | "down"
    
    OPERATOR                : ">="
                            | "<=" 
                            | "==" 
                            | "!="
                            | "<"
                            | ">"
    FUNC_TYPE1              : "all"|"any"
    FUNC_TYPE2              : "mean"|"min"|"max"|"sum"
    _TIME_SYMBOL            : "@t=" 
    POINT_TIME              :  DIGIT+
    INTERVAL_TIME           : "(" DIGIT+ [WS]* "," [WS]* DIGIT + ")"
    OBS_NAME                : NAME
    CONDITION               : NAME
    NAME                    : /(?!\d+)[A-Za-z0-9_]+/
    START                   : DIGIT+
    STOP                    : DIGIT+
    STEP                    : DIGIT+
    POW                     : "**"
    MUL                     : "*"
    DIV                     : "/"
    ADD                     : "+"
    SUB                     : "-"
    MOD                     : "%"
    FLOOR                   : "//"
    NUMERICAL_OPERATOR      : "+"
                            | "-"
                            | "*"
                            | "/"
                            | "**"
                            | "//"
                            | "%"
    COMMENT                 : /\/\/.*/
    %import common.DIGIT
    %import common.NUMBER
    %import common.FLOAT
    %import common.WORD
    %import common.LETTER
    %import common.WS
    %ignore WS
    %ignore COMMENT
    """

    def __init__(self, model_string: str, observation_string: str) -> None:
        """

        Args:
            model_string: str. An antimony model.
            observation_string: str. An qmf input string.
        """
        self.observation_string = observation_string
        self.model_string = model_string
        self.lark = Lark(self.grammar)
        self.tree = self.parse()
        self.ts_blocks, self.observation_block = self.objectify()

    def parse(self, string: typing.Optional[str] = None):
        """
        Wrapper around lark.parse

        Args:
            string: Optional. String to parse. Default is the observation string.

        Returns:

        """
        if string is None:
            string = self.observation_string
        return self.lark.parse(string)

    def pretty(self, string=None):
        """
        Pretty print function
        Args:
            string:

        Returns:

        """
        if string is None:
            string = self.observation_string
        return self.lark.parse(string).pretty()

    def objectify(self):
        """
        Convert the varioius blocks into objects for later use.
        Returns:

        """
        ts_dct = {}
        for ts_block in self.tree.find_data('timeseries_block'):
            name = str(ts_block.children[0])
            ts_dct[name] = _TimeSeriesBlock(self.model_string, ts_block)

        ss_list = []
        for ss_block in self.tree.find_data('steady_state_block'):
            LOG.warning('steady state functionality is currently a placeholder. '
                        'Not yet implemented')

        observation_block = _ObservationBlock(ts_dct)
        observations = [i for i in self.tree.find_data('observation_block')][0]
        for i in observations.children:
            if i.data in ['comparison_statement_without_func', 'comparison_statement_with_func']:
                observation_block.append(_ComparisonStatement(i, ts_dct))
            elif i.data == 'qualitative_statement':
                pass
            else:
                raise ValueError

        return ts_dct, observation_block


class _TimeSeriesBlock:
    """
    Reads timeseries blocks into python and executes the time series
    simulation using tellurium and roadrunner.
    """
    def __init__(self, model_string, ts_block):
        self.model_string = model_string
        self.ts_block = ts_block
        self.name, self.start, self.stop, self.step = self._get_ts_parameters()

        self.ts_arg_list = _TimeSeriesArgumentList()
        for i in self.ts_block.iter_subtrees():
            if isinstance(i, Tree):
                if i.data == 'ts_arg':
                    self.ts_arg_list.append(_TimeSeriesArgument(i))

            else:
                raise ValueError

    def _get_ts_parameters(self):
        start = None
        stop = None
        step = None
        name = None
        for i in self.ts_block.children:
            if isinstance(i, Tree):
                pass

            elif isinstance(i, Token):
                if i.type == 'START':
                    start = float(str(i))
                elif i.type == 'STOP':
                    stop = float(str(i))
                elif i.type == 'STEP':
                    step = int(str(i))
                elif i.type == 'NAME':
                    name = str(i)
            else:
                raise ValueError
        for i in [name, start, stop, step]:
            if i is None:
                raise SyntaxError(i)
        return name, start, stop, step

    def simulate(self):
        data = TimeSeries(self.model_string, self.ts_arg_list.to_dict(),
                          self.start, self.stop, self.step).simulate()
        return data

    def __str__(self):
        if len(self.ts_arg_list) == 1:
            ts_arg_list = self.ts_arg_list.children[0]
        else:
            ts_arg_list = reduce(lambda x, y: f'{x}, {y}', self.ts_arg_list)
        return f"{self.__class__.__name__}(timeseries {self.name} {{ {ts_arg_list} }} {self.start}, {self.stop}, {self.step})"

    def __repr__(self):
        return self.__str__()


class _TimeSeriesArgumentList(list):
    """
    A data class that holds time series arguments. Inherits
    from list.
    """

    def __init__(self, *args):
        self.args = args
        self._check_all_elements_are_ts_arg()

    def _check_all_elements_are_ts_arg(self):
        for i in self:
            if i.data != 'ts_arg':
                raise ValueError('Was expecting a TimeSeriesArgument but got "{}"'.format(type(i)))

    def to_dict(self):
        dct = {}
        for i in self:
            dct[str(i.name)] = float(str(i.amount))
        return dct


class _TimeSeriesArgument:
    """
    A data class for holding a single time series argument
    """

    def __init__(self, ts_arg):
        self.ts_arg = ts_arg

        if ts_arg.data != 'ts_arg':
            raise ValueError

        if len(ts_arg.children) != 2:
            raise ValueError('was expecting two arguments but got "{}"'.format(len(ts_arg.children)))

    @property
    def name(self):
        return self.ts_arg.children[0]

    @property
    def amount(self):
        return self.ts_arg.children[1]

    def __str__(self):
        return f'{self.name}={self.amount}'

    def __repr__(self):
        return self.__str__()


class _ObservationBase:
    """
    Base class for observation types. Observation types are
    those involved in getting the users observations understood by the
    program.
    """

    def __init__(self):
        pass

    @staticmethod
    def reduce_component(component, ts_dct=None):

        if isinstance(component, Tree):
            if component.data == 'model_entity':
                if ts_dct is None:
                    raise SyntaxError('ts_dct arg is required component is a model_entity')
                return _ModelEntity(component, ts_dct).reduce()
            elif component.data == 'expression':
                return _Expression(component, ts_dct).reduce()
            elif component.data == 'term':
                return _Term(component, ts_dct).reduce()
            # elif component.data in ['clause1', 'clause2']:
            #     return _Clause(component, ts_dct)
            elif component.data == 'clause_without_func':
                return _Clause(component, ts_dct)
            elif component.data == 'clause_with_func':
                func = component.children[0]
                if not func.type == 'FUNC_TYPE2':
                    raise ValueError
                comp = component.children[1]
                if not isinstance(comp, Tree):
                    raise ValueError
                return _ModelEntity(comp, ts_dct, function=func).reduce()

            else:
                raise ValueError(component)
        elif isinstance(component, Token):
            if component.type == 'NUMBER':
                return _ObservationBase.token_to_number(component)

            else:
                return str(component)
                # raise ValueError(f'{component}, {component.type}')
        else:
            raise ValueError

    def reduce_recursive(self, tree, ts_list):
        pass

    @staticmethod
    def token_to_number(token):
        element = float(str(token))
        if element.is_integer():
            return int(element)
        else:
            return element


class _ObservationBlock(list):
    """
    Contain all observations in a list like structure. Inherits
    from list.
    """
    def __init__(self, ts_list, *args):
        self.ts_list = ts_list
        self.args = args
        super(_ObservationBlock, self).__init__(*args)

        for i in self.args:
            if not isinstance(i, _ComparisonStatement):
                raise TypeError(i)


class _ComparisonStatement(_ObservationBase):
    """
    Comparison statements have everything they need in order
    to make instructions for a comparison of type operator
    between clause1 and clause2. Comparison statements also
    have a name and either clause can have functions that modify their
    meaning.
    """
    name = None
    operator = None
    clause1 = None
    clause2 = None
    func = None

    def __init__(self, tree, ts_list):
        super().__init__()
        self.tree = tree
        self.ts_list = ts_list

        if not isinstance(tree, Tree):
            raise TypeError

        if self.tree.data not in ['comparison_statement_with_func',
                                  'comparison_statement_without_func']:
            raise ValueError(self.tree.data)

        for i in self.tree.children:
            if isinstance(i, Token):
                if i.type == 'OBS_NAME':
                    self.name = str(i)
                elif i.type == 'OPERATOR':
                    self.operator = _Operator(str(i))
                elif i.type == 'FUNC_TYPE1':
                    self.func = str(i)
                else:
                    raise ValueError(f'{i}, {i.type}')
            elif isinstance(i, Tree):
                if i.data == 'clause1':
                    if not len(i.children) == 1:
                        raise ValueError
                    self.clause1 = _Clause(i, self.ts_list)
                elif i.data == 'clause2':
                    if not len(i.children) == 1:
                        raise ValueError
                    self.clause2 = _Clause(i, self.ts_list)
                else:
                    raise ValueError
            else:
                raise ValueError

    def __str__(self):
        try:
            clause1 = float(str(self.clause1))
            clause1 = round(clause1, 4)
            if clause1.is_integer():
                clause1 = int(clause1)
        except ValueError:
            clause1 = 'TimeInterval'

        try:
            clause2 = float(str(self.clause2))
            clause2 = round(clause2, 4)
            if clause2.is_integer():
                clause2 = int(clause2)
        except ValueError:
            clause2 = 'TimeInterval'

        if self.func is None:
            return f'{clause1} {str(self.operator)} {clause2}'
        else:
            return f'{self.func}({clause1} {str(self.operator)} {clause2})'

    def __repr__(self):
        return self.__str__()

    def reduce(self):
        """
        reduce a comparison to boolean
        Returns:

        """
        if self.tree.data == 'comparison_statement_with_func':
            if not hasattr(np, self.func):
                raise SyntaxError(self.func)
            func = getattr(np, self.func)

            if isinstance(self.clause1, pd.Series) and isinstance(self.clause2, pd.Series):
                if self.clause1.shape != self.clause2.shape:
                    raise ValueError('Can only make comparisons between model entities '
                                     'that have intervals of the same shape. Clause1={} != Clause2={}'
                                     ''.format(self.clause1.shape, self.clause2.shape))
            if isinstance(self.clause1, pd.Series):
                self.clause1 = self.clause1.values
            if isinstance(self.clause2, pd.Series):
                self.clause2 = self.clause2.values
            return func(self.operator.operator(self.clause1, self.clause2))
        elif self.tree.data == 'comparison_statement_without_func':
            return self.operator.operator(self.clause1.reduce(), self.clause2.reduce())
        else:
            raise ValueError(self.tree)


class _Clause(_ObservationBase):

    def __init__(self, clause, ts_dct):
        self.clause = clause
        self.ts_dct = ts_dct

        if not isinstance(self.clause, Tree):
            raise TypeError(self.clause)
        if self.clause.data not in ['clause_without_func', 'clause_with_func',
                                    'clause1', 'clause2']:
            raise ValueError(self.clause.data)

    def reduce(self):
        reduced = None
        for i in self.clause.children:
            if isinstance(i, Token):
                if i.type == 'NUMBER':
                    reduced = self.token_to_number(i)
                else:
                    reduced = str(i)
            elif isinstance(i, Tree):
                reduced = self.reduce_component(i, self.ts_dct)
            else:
                raise ValueError
        if reduced is None:
            raise ValueError
        return reduced

    def is_time_interval(self):
        r = self.__str__()
        try:
            isint = float(r)
            return False
        except ValueError:
            return True
        raise NotImplementedError

    def __str__(self):
        return self.reduce().__str__()

    def __repr__(self):
        return self.__str__()

    def __gt__(self, other):
        if isinstance(other, _Clause):
            return self.reduce().__gt__(other.reduce())
        else:
            return self.reduce().__gt__(other)

    def __lt__(self, other):

        if isinstance(other, _Clause):
            return self.reduce().__lt__(other.reduce())
        else:
            return self.reduce().__lt__(other)

    def __ge__(self, other):
        if isinstance(other, _Clause):
            return self.reduce().__ge__(other.reduce())
        else:
            return self.reduce().__ge__(other)

    def __le__(self, other):
        if isinstance(other, _Clause):
            return self.reduce().__le__(other.reduce())
        else:
            return self.reduce().__le__(other)

    def __eq__(self, other):
        if isinstance(other, _Clause):
            return self.reduce().__eq__(other.reduce())
        else:
            return self.reduce().__eq__(other)

    def __ne__(self, other):
        if isinstance(other, _Clause):
            return self.reduce().__ne__(other.reduce())
        else:
            return self.reduce().__ne__(other.reduce())


class _Expression(_ObservationBase):

    def __init__(self, exprs, ts_dct):
        self.exprs = exprs
        self.ts_dct = ts_dct

        if not isinstance(self.exprs, Tree):
            raise ValueError
        if self.exprs.data not in ['expression']:
            raise TypeError

    def _reduce_terms(self):
        l = []
        for i in self.exprs.children:
            if isinstance(i, Tree):
                if i.data == 'term':
                    l.append(_Term(i, self.ts_dct).reduce())
                else:
                    l.append(i)
            else:
                l.append(i)
        return l

    def _expression_string(self):
        children = self._reduce_terms()
        reduced = reduce(lambda x, y: f'{str(x)} {str(y)}', children)
        return str(reduced)

    def reduce(self):
        evaluated = eval(self._expression_string())
        if isinstance(evaluated, (float, int)):
            reduced = float(str(evaluated))
            # coerce to int if needed
            if reduced.is_integer():
                return int(reduced)
            else:
                return reduced
        else:
            return str(evaluated)

    def __str__(self):
        return self._expression_string()

    def __repr__(self):
        return self.__str__()


class _ModelEntity(_ObservationBase):
    time_type = None

    def __init__(self, model_entity, ts_dct, function=None):
        self.model_entity = model_entity
        self.ts_dct = ts_dct
        self.function = function

        if self.function is not None:
            if not hasattr(np, self.function):
                raise ValueError
            self.function = getattr(np, self.function)

        if not isinstance(model_entity, Tree):
            raise TypeError

        if not model_entity.data == 'model_entity':
            raise ValueError(model_entity.data)

    @property
    def component_name(self):
        name = self.model_entity.children[0]
        assert name.type == 'NAME'
        return name.value

    @property
    def condition(self):
        cond = self.model_entity.children[1]
        assert cond.type == 'CONDITION'
        return cond.value

    @property
    def time(self):
        time = self.model_entity.children[2]
        if time.type == 'POINT_TIME':
            self.time_type = 'POINT'
        elif time.type == 'INTERVAL_TIME':
            self.time_type = 'INTERVAL'
        else:
            raise SyntaxError
        return time.value

    def __str__(self):
        return f'{self.component_name}[{self.condition}]@t={self.time}'

    def __repr__(self):
        return self.__str__()

    def reduce(self):
        time = eval(self.time)
        if isinstance(time, tuple):
            output = self.ts_dct[self.condition].simulate()[self.component_name].loc[float(time[0]): float(time[1])]
        else:
            output = self.ts_dct[self.condition].simulate()[self.component_name].loc[float(time)]
        if self.function is not None:
            return self.function(output)
        else:
            return output


class _Term(_ObservationBase):

    def __init__(self, term, ts_dct):
        self.term = term
        self.ts_dct = ts_dct

    @property
    def left(self):
        return self.reduce_component(self.term.children[0], self.ts_dct)

    @property
    def right(self):
        return self.reduce_component(self.term.children[2], self.ts_dct)

    @property
    def operator(self):
        return self.reduce_component(self.term.children[1])

    def __str__(self):
        return f"{self.left}{self.operator}{self.right}"
        # return reduce(lambda x, y: f'{str(x)}{str(y)}', self.term.children)

    def __repr__(self):
        return self.__str__()

    def reduce(self):
        return eval(self.__str__())


class _Operator(_ObservationBase):

    def __init__(self, op):
        self.op = op

    @property
    def operator(self):
        if self.op == '>':
            return operator.gt
        elif self.op == '<':
            return operator.lt
        elif self.op == '>=':
            return operator.ge
        elif self.op == '<=':
            return operator.le
        elif self.op == '!=':
            return operator.ne
        elif self.op == '==':
            return operator.eq
        else:
            raise SyntaxError(self.op)

    def __str__(self):
        return self.op

    def __repr__(self):
        return self.__str__()
