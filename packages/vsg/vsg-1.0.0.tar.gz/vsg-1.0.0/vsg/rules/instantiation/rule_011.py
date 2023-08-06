
from vsg import rule
from vsg import fix
from vsg import check
from vsg import utils


class rule_011(rule.rule):
    '''
    Instantiation rule 011 checks the port name is uppercase.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'instantiation'
        self.identifier = '011'
        self.solution = 'Uppercase port name.'
        self.phase = 6

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isInstantiationPortAssignment and not oLine.isInstantiationPortKeyword:
            sWord = utils.remove_parenthesis_from_word(oLine.line.split()[0])
            check.is_uppercase(self, sWord, iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            oLine = oFile.lines[iLineNumber]
            sPortName = oLine.line.split('=>')[0].split('(')[0].lstrip().rstrip()
            fix.upper_case(oLine, sPortName)
