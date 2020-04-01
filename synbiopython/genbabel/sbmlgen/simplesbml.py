# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 23:13:42 2015
@author: carolc24, Kyle Medley

added more unit definitions
Reference:
https://github.com/sys-bio/simplesbml/blob/master/simplesbml/__init__.py
"""

import warnings

# try to import tesbml or libsbml
# if both of these fail, libsbml cannot be imported - cannot continue
try:
    import tesbml as libsbml
except ImportError:
    import libsbml

from math import isnan
from re import sub

__version__ = "1.2.2"


class sbmlModel(object):
    def check(self, value, message):
        if value is None:
            raise SystemExit("LibSBML returned a null value trying to " + message + ".")
        elif type(value) is int:
            if value == libsbml.LIBSBML_OPERATION_SUCCESS:
                return
            else:
                err_msg = (
                    "Error trying to "
                    + message
                    + "."
                    + "LibSBML returned error code "
                    + str(value)
                    + ': "'
                    + libsbml.OperationReturnValue_toString(value).strip()
                    + '"'
                )
            raise RuntimeError(err_msg)
        else:
            return

    def __init__(
        self,
        time_units="second",
        extent_units="mole",
        sub_units="mole",
        level=3,
        version=1,
    ):
        if level == 1:
            raise SystemExit("Error: SimpleSBML does not support SBML level 1")
        try:
            self.document = libsbml.SBMLDocument(level, version)
        except ValueError:
            raise SystemExit("Could not create SBMLDocument object")
        self.model = self.document.createModel()
        self.check(self.model, "create model")
        if self.document.getLevel() == 3:
            self.check(self.model.setTimeUnits(time_units), "set model-wide time units")
            self.check(
                self.model.setExtentUnits(extent_units), "set model units of extent"
            )
            self.check(
                self.model.setSubstanceUnits(sub_units), "set model substance units"
            )

        per_second = self.model.createUnitDefinition()
        self.check(per_second, "create unit definition")
        self.check(per_second.setId("per_second"), "set unit definition id")
        unit = per_second.createUnit()
        self.check(unit, "create unit on per_second")
        self.check(unit.setKind(libsbml.UNIT_KIND_SECOND), "set unit kind")
        self.check(unit.setExponent(-1), "set unit exponent")
        self.check(unit.setScale(0), "set unit scale")
        self.check(unit.setMultiplier(1), "set unit multiplier")

        per_min = self.model.createUnitDefinition()
        self.check(per_min, "create unit definition")
        self.check(per_min.setId("per_min"), "set unit definition id")
        unit = per_min.createUnit()
        self.check(unit, "create unit on per_min")
        self.check(unit.setKind(libsbml.UNIT_KIND_SECOND), "set unit kind")
        self.check(unit.setExponent(-1), "set unit exponent")
        self.check(unit.setScale(0), "set unit scale")
        self.check(unit.setMultiplier(60), "set unit multiplier")

        molperLmin = self.model.createUnitDefinition()
        self.check(molperLmin, "create unit definition")
        self.check(molperLmin.setId("molperLmin"), "set unit definition id")
        unit = molperLmin.createUnit()
        self.check(unit, "create unit on per_second")
        self.check(unit.setKind(libsbml.UNIT_KIND_MOLE), "set unit kind")
        self.check(unit.setExponent(1), "set unit exponent")
        self.check(unit.setScale(0), "set unit scale")
        self.check(unit.setMultiplier(1), "set unit multiplier")
        unit = molperLmin.createUnit()
        self.check(unit, "create unit on per_second")
        self.check(unit.setKind(libsbml.UNIT_KIND_LITRE), "set unit kind")
        self.check(unit.setExponent(-1), "set unit exponent")
        self.check(unit.setScale(0), "set unit scale")
        self.check(unit.setMultiplier(1), "set unit multiplier")
        unit = molperLmin.createUnit()
        self.check(unit, "create unit on per_second")
        self.check(unit.setKind(libsbml.UNIT_KIND_SECOND), "set unit kind")
        self.check(unit.setExponent(-1), "set unit exponent")
        self.check(unit.setScale(0), "set unit scale")
        self.check(unit.setMultiplier(60), "set unit multiplier")

        molperL = self.model.createUnitDefinition()
        self.check(molperL, "create unit definition")
        self.check(molperL.setId("molperL"), "set unit definition id")
        unit = molperL.createUnit()
        self.check(unit, "create unit")
        self.check(unit.setKind(libsbml.UNIT_KIND_MOLE), "set unit kind")
        self.check(unit.setExponent(1), "set unit exponent")
        self.check(unit.setScale(0), "set unit scale")
        self.check(unit.setMultiplier(1), "set unit multiplier")
        unit = molperL.createUnit()
        self.check(unit, "create unit")
        self.check(unit.setKind(libsbml.UNIT_KIND_LITRE), "set unit kind")
        self.check(unit.setExponent(-1), "set unit exponent")
        self.check(unit.setScale(0), "set unit scale")
        self.check(unit.setMultiplier(1), "set unit multiplier")

        Dimension_less = self.model.createUnitDefinition()
        self.check(Dimension_less, "create unit definition")
        self.check(Dimension_less.setId("Dimension_less"), "set unit definition id")
        unit = Dimension_less.createUnit()
        self.check(unit, "create unit")
        self.check(unit.setKind(libsbml.UNIT_KIND_DIMENSIONLESS), "set unit kind")
        self.check(unit.setExponent(0), "set unit exponent")
        self.check(unit.setScale(0), "set unit scale")
        self.check(unit.setMultiplier(0), "set unit multiplier")

        self.addCompartment()

    def addCompartment(self, vol=1, comp_id=""):
        c1 = self.model.createCompartment()
        self.check(c1, "create compartment")
        if len(comp_id) == 0:
            comp_id = "c" + str(self.model.getNumCompartments())
        self.check(c1.setId(comp_id), "set compartment id")
        self.check(c1.setConstant(True), 'set compartment "constant"')
        self.check(c1.setSpatialDimensions(3), "set compartment dimensions")

        self.check(c1.setSize(vol), 'set compartment "size"')
        self.check(c1.setUnits("litre"), "set compartment size units")
        return c1

    def addSpecies(self, species_id, amt, comp="c1"):
        s1 = self.model.createSpecies()
        self.check(s1, "create species s1")
        self.check(s1.setCompartment(comp), "set species s1 compartment")
        if species_id[0] == "[" and species_id[len(species_id) - 1] == "]":
            self.check(
                s1.setInitialConcentration(amt), "set initial concentration for s1"
            )
            species_id = species_id[1 : (len(species_id) - 1)]
        else:
            self.check(s1.setInitialAmount(amt), "set initial amount for s1")
        self.check(
            s1.setSubstanceUnits(self.model.getSubstanceUnits()),
            "set substance units for s1",
        )
        if species_id[0] == "$":
            self.check(s1.setBoundaryCondition(True), 'set "boundaryCondition" on s1')
            self.check(s1.setConstant(False), 'set "constant" attribute on s1')
            self.check(s1.setId(species_id[1 : len(species_id)]), "set species s1 id")
        else:
            self.check(s1.setBoundaryCondition(False), 'set "boundaryCondition" on s1')
            self.check(s1.setConstant(False), 'set "constant" attribute on s1')
            self.check(s1.setId(species_id), "set species s1 id")
        self.check(
            s1.setHasOnlySubstanceUnits(False), 'set "hasOnlySubstanceUnits" on s1'
        )
        return s1

    def addParameter(self, param_id, val, units="per_second"):
        k = self.model.createParameter()
        self.check(k, "create parameter k")
        self.check(k.setId(param_id), "set parameter k id")
        self.check(k.setConstant(True), 'set parameter k "not constant"')
        self.check(k.setValue(val), "set parameter k value")
        self.check(k.setUnits(units), "set parameter k units")
        return k

    def addReaction(self, reactants, products, expression, local_params={}, rxn_id=""):
        r1 = self.model.createReaction()
        self.check(r1, "create reaction")
        if len(rxn_id) == 0:
            rxn_id = "v" + str(self.model.getNumReactions())
        self.check(r1.setId(rxn_id), "set reaction id")
        self.check(r1.setReversible(False), "set reaction reversibility flag")
        self.check(r1.setFast(False), 'set reaction "fast" attribute')

        for re in reactants:
            if re is not None and "$" in re:
                re.translate(None, "$")
            re_split = re.split()
            if len(re_split) == 1:
                sto = 1.0
                re_id = re
            elif len(re_split) == 2 and re_split[0].isdigit():
                sto = float(re_split[0])
                re_id = re_split[1]
            else:
                err_msg = (
                    "Error: reactants must be listed in format 'S' or '(float)' S'"
                )
                raise SystemExit(err_msg)
            s1 = self.model.getSpecies(re_id)
            species_ref1 = r1.createReactant()
            self.check(species_ref1, "create reactant")
            self.check(species_ref1.setSpecies(s1.getId()), "assign reactant species")
            self.check(
                species_ref1.setStoichiometry(sto), "assign reactant stoichiometry"
            )
            if self.document.getLevel() == 3:
                self.check(
                    species_ref1.setConstant(True), 'set "constant" on species ref 1'
                )

        for pro in products:
            if pro is not None and "$" in pro:
                pro.translate(None, "$")
            pro_split = pro.split()
            if len(pro_split) == 1:
                sto = 1.0
                pro_id = pro
            elif len(pro_split) == 2:
                sto = float(pro_split[0])
                pro_id = pro_split[1]
            else:
                err_msg = "Error: products must be listed in format 'S' or '(float)' S'"
                raise SystemExit(err_msg)
            s2 = self.model.getSpecies(pro_id)
            species_ref2 = r1.createProduct()
            self.check(species_ref2, "create product")
            self.check(species_ref2.setSpecies(s2.getId()), "assign product species")
            self.check(species_ref2.setStoichiometry(sto), "set product stoichiometry")
            if self.document.getLevel() == 3:
                self.check(
                    species_ref2.setConstant(True), 'set "constant" on species ref 2'
                )

        math_ast = libsbml.parseL3Formula(expression)
        self.check(math_ast, "create AST for rate expression")

        kinetic_law = r1.createKineticLaw()
        self.check(kinetic_law, "create kinetic law")
        self.check(kinetic_law.setMath(math_ast), "set math on kinetic law")
        for param in local_params.keys():
            val = local_params.get(param)
            if self.document.getLevel() == 3:
                p = kinetic_law.createLocalParameter()
            else:
                p = kinetic_law.createParameter()
            self.check(p, "create local parameter")
            self.check(p.setId(param), "set id of local parameter")
            self.check(p.setValue(val), "set value of local parameter")
        return r1

    def addEvent(
        self,
        trigger,
        assignments,
        persistent=True,
        initial_value=False,
        priority=0,
        delay=0,
        event_id="",
    ):
        e1 = self.model.createEvent()
        self.check(e1, "create event")
        if len(event_id) == 0:
            event_id = "e" + str(self.model.getNumEvents())
        self.check(e1.setId(event_id), "add id to event")
        if self.document.getLevel() == 3 or (
            self.document.getLevel() == 2 and self.document.getVersion() == 4
        ):
            self.check(
                e1.setUseValuesFromTriggerTime(True), "set use values from trigger time"
            )

        tri = e1.createTrigger()
        self.check(tri, "add trigger to event")
        tri_ast = libsbml.parseL3Formula(trigger)
        self.check(tri.setMath(tri_ast), "add formula to trigger")
        if self.document.getLevel() == 3:
            self.check(tri.setPersistent(persistent), "set persistence of trigger")
            self.check(
                tri.setInitialValue(initial_value), "set initial value of trigger"
            )

        de = e1.createDelay()
        if self.document.getLevel() == 3:
            k = self.addParameter(event_id + "Delay", delay, self.model.getTimeUnits())
        else:
            k = self.addParameter(event_id + "Delay", delay, "time")
        self.check(de, "add delay to event")
        delay_ast = libsbml.parseL3Formula(k.getId())
        self.check(de.setMath(delay_ast), "set formula for delay")

        for a in assignments.keys():
            assign = e1.createEventAssignment()
            self.check(assign, "add event assignment to event")
            self.check(assign.setVariable(a), "add variable to event assignment")
            val_ast = libsbml.parseL3Formula(assignments.get(a))
            self.check(assign.setMath(val_ast), "add value to event assignment")

        if self.document.getLevel() == 3:
            pri = e1.createPriority()
            pri_ast = libsbml.parseL3Formula(str(priority))
            self.check(pri.setMath(pri_ast), "add priority to event")
        return e1

    def addAssignmentRule(self, var, math):
        r = self.model.createAssignmentRule()
        self.check(r, "create assignment rule r")
        self.check(r.setVariable(var), "set assignment rule variable")
        math_ast = libsbml.parseL3Formula(math)
        self.check(r.setMath(math_ast), "set assignment rule equation")
        return r

    def addRateRule(self, var, math, rr_id=""):
        r = self.model.createRateRule()
        self.check(r, "create rate rule r")
        if len(rr_id) == 0:
            rr_id = "Rate" + str(self.model.getNumRules())
        r.setIdAttribute(rr_id)
        print("rr_id=", r.getIdAttribute())

        # self.check(r.setId(rr_id),           'set rate rule id')
        self.check(r.setVariable(var), "set rate rule variable")
        math_ast = libsbml.parseL3Formula(math)
        self.check(r.setMath(math_ast), "set rate rule equation")
        return r

    def addInitialAssignment(self, symbol, math):
        if self.document.getLevel() == 2 and self.document.getVersion() == 1:
            raise SystemExit(
                "Error: InitialAssignment does not exist for \
                    this level and version."
            )
        a = self.model.createInitialAssignment()
        self.check(a, "create initial assignment a")
        self.check(a.setSymbol(symbol), "set initial assignment a symbol")
        math_ast = libsbml.parseL3Formula(math)
        self.check(a.setMath(math_ast), "set initial assignment a math")
        return a

    def setLevelAndVersion(self, level, version):
        if level == 2 and version == 1:
            self.check(
                self.document.checkL2v1Compatibility(), "convert to level 2 version 1"
            )
        elif level == 2 and version == 2:
            self.check(
                self.document.checkL2v2Compatibility(), "convert to level 2 version 2"
            )
        elif level == 2 and version == 3:
            self.check(
                self.document.checkL2v3Compatibility(), "convert to level 2 version 3"
            )
        elif level == 2 and version == 4:
            self.check(
                self.document.checkL2v4Compatibility(), "convert to level 2 version 4"
            )
        elif level == 3 and version == 1:
            self.check(
                self.document.checkL3v1Compatibility(), "convert to level 3 version 1"
            )
        else:
            raise SystemExit("Invalid level/version combination")

        isSet = self.document.setLevelAndVersion(level, version)
        self.check(isSet, "convert to level " + str(level) + " version " + str(version))

    def getDocument(self):
        return self.document

    def getModel(self):
        return self.model

    def getSpecies(self, species_id):
        return self.model.getSpecies(species_id)

    def getListOfSpecies(self):
        return self.model.getListOfSpecies()

    def getParameter(self, param_id):
        return self.model.getParameter(param_id)

    def getListOfParameters(self):
        return self.model.getListOfParameters()

    def getReaction(self, rxn_id):
        return self.model.getReaction(rxn_id)

    def getListOfReactions(self):
        return self.model.getListOfReactions()

    def getCompartment(self, comp_id):
        return self.model.getCompartment(comp_id)

    def getListOfEvents(self):
        return self.model.getListOfEvents()

    def getEvent(self, event_id):
        return self.model.getEvent(event_id)

    def getListOfCompartments(self):
        return self.model.getListOfCompartments()

    def getRule(self, var):
        return self.model.getRule(var)

    def getListOfRules(self):
        return self.model.getListOfRules()

    def getInitialAssignment(self, var):
        return self.model.getInitialAssignment(var)

    def getListOfInitialAssignments(self):
        return self.model.getListOfInitialAssignments()

    def toSBML(self):
        errors = self.document.checkConsistency()
        if errors > 0:
            for i in range(errors):
                print(
                    self.document.getError(i).getSeverityAsString(),
                    ": ",
                    self.document.getError(i).getMessage(),
                )

        return libsbml.writeSBMLToString(self.document)

    def __repr__(self):
        return self.toSBML()


def writeCode(doc):
    comp_template = "model.addCompartment(vol=%s, comp_id='%s');"
    species_template = "model.addSpecies(species_id='%s', amt=%s, comp='%s');"
    param_template = "model.addParameter(param_id='%s', val=%s, units='%s');"
    rxn_template = "model.addReaction(reactants=%s, products=%s, expression='%s', local_params=%s, rxn_id='%s');"
    event_template = "model.addEvent(trigger='%s', assignments=%s, persistent=%s, initial_value=%s, priority=%s, delay=%s, event_id='%s');"
    event_defaults = [True, False, "0", 0]
    assignrule_template = "model.addAssignmentRule(var='%s', math='%s');"
    raterule_template = "model.addRateRule(var='%s', math='%s', rr_id='%s');"
    initassign_template = "model.addInitialAssignment(symbol='%s', math='%s')"
    init_template = "import simplesbml\nmodel = simplesbml.sbmlModel(time_units='%s', extent_units='%s', sub_units='%s', level=%s, version=%s);"
    init_defaults = ["min", "Molar", "Molar", 3, 1]
    command_list = []

    if doc.getLevel() == 1:
        warnings.warn("Warning: SimpleSBML does not support SBML Level 1.")

    props = libsbml.ConversionProperties()
    props.addOption("flatten comp", True)
    result = doc.convert(props)
    if result != libsbml.LIBSBML_OPERATION_SUCCESS:
        raise SystemExit("Conversion failed: (" + str(result) + ")")

    mod = doc.getModel()
    comps = mod.getListOfCompartments()
    species = mod.getListOfSpecies()
    params = mod.getListOfParameters()
    rxns = mod.getListOfReactions()
    events = mod.getListOfEvents()
    rules = mod.getListOfRules()
    print("rules", rules)
    inits = []
    if doc.getLevel() == 3 or (doc.getLevel() == 2 and doc.getVersion() > 1):
        inits = mod.getListOfInitialAssignments()

    timeUnits = "min"  # second
    substanceUnits = "Molar"  # mole
    extentUnits = "Molar"  # mole
    if doc.getLevel() == 3:
        timeUnits = mod.getTimeUnits()
        extentUnits = mod.getExtentUnits()
        substanceUnits = mod.getSubstanceUnits()
    level = mod.getLevel()
    version = mod.getVersion()
    init_list = [timeUnits, extentUnits, substanceUnits, level, version]
    for i in range(0, 5):
        if init_list[i] == init_defaults[i]:
            init_list[i] = "del"

    command_list.append(
        init_template
        % (init_list[0], init_list[1], init_list[2], init_list[3], init_list[4])
    )

    for comp in comps:
        if comp.getId() != "c1":
            if comp.getId()[0] == "c" and comp.getId()[1 : len(comp.getId())].isdigit():
                if comp.getSize() == 1e-15:
                    command_list.append(comp_template % ("del", "del"))
                else:
                    command_list.append(comp_template % (comp.getSize(), "del"))
            else:
                if comp.getSize() == 1e-15:
                    command_list.append(comp_template % ("del", comp.getId()))
                else:
                    command_list.append(comp_template % (comp.getSize(), comp.getId()))

    for s in species:
        conc = s.getInitialConcentration()
        amt = s.getInitialAmount()
        sid = s.getId()
        if s.getCompartment() == "c1":
            comp = "del"
        else:
            comp = s.getCompartment()
        bc = s.getBoundaryCondition()
        if bc:
            sid = "$" + sid
        if isnan(conc) or amt > conc:
            command_list.append(species_template % (sid, str(amt), comp))
        else:
            command_list.append(species_template % ("[" + sid + "]", str(conc), comp))

    for p in params:
        val = p.getValue()
        pid = p.getId()
        if p.getUnits() == "per_second":
            units = "del"
        else:
            units = p.getUnits()
        isDelay = pid.find("Delay")
        if isDelay == -1:
            command_list.append(param_template % (pid, str(val), str(units)))

    for v in rxns:
        vid = v.getId()
        if vid[0] == "v" and vid[1 : len(vid)].isdigit():
            vid = "del"
        reactants = []
        for r in v.getListOfReactants():
            reactants.append(
                (str(r.getStoichiometry()) + " " + r.getSpecies()).replace("1.0 ", "")
            )
        products = []
        for p in v.getListOfProducts():
            products.append(
                (str(p.getStoichiometry()) + " " + p.getSpecies()).replace("1.0 ", "")
            )
        expr = libsbml.formulaToString(v.getKineticLaw().getMath())
        local_params = {}
        local_ids = []
        local_values = []
        for k in v.getKineticLaw().getListOfParameters():
            local_ids.append(k.getId())
            local_values.append(k.getValue())
        local_params = dict(zip(local_ids, local_values))
        if len(local_params) == 0:
            local_params = "del"
        command_list.append(
            rxn_template % (str(reactants), str(products), expr, str(local_params), vid)
        )

    for e in events:
        persistent = True
        initialValue = False
        priority = "0"
        eid = e.getId()
        if len(eid) == 0 or (eid[0] == "e" and eid[1 : len(eid)].isdigit()):
            eid = "del"
        if doc.getLevel() == 3:
            persistent = e.getTrigger().getPersistent()
            initialValue = e.getTrigger().getInitialValue()
            priority = e.getPriority()
            if type(priority) == libsbml.Priority:
                priority = libsbml.formulaToL3String(priority.getMath())
            else:
                priority = "0"
        tri = libsbml.formulaToL3String(e.getTrigger().getMath())
        did = e.getDelay()
        if type(did) == libsbml.Delay:
            delay = libsbml.formulaToL3String(did.getMath())
        else:
            delay = "0"
        assigns = e.getListOfEventAssignments()
        var = []
        values = []
        for assign in assigns:
            var.append(assign.getVariable())
            values.append(libsbml.formulaToL3String(assign.getMath()))
        assigns = dict(zip(var, values))

        event_list = [persistent, initialValue, priority, delay]
        for i in range(0, 4):
            if event_list[i] == event_defaults[i]:
                event_list[i] = "del"

        command_list.append(
            event_template
            % (
                tri,
                str(assigns),
                event_list[0],
                event_list[1],
                event_list[2],
                event_list[3],
                eid,
            )
        )

    for r in rules:
        rid = r.getId()
        print("rid")
        #        if rid[0] == 'Rate' and rid[1:len(rid)].isdigit():
        #            rid = 'del'
        sym = r.getVariable()
        math = libsbml.formulaToL3String(r.getMath())
        if r.getTypeCode() == libsbml.SBML_ASSIGNMENT_RULE:
            command_list.append(assignrule_template % (sym, math))
        elif r.getTypeCode() == libsbml.SBML_RATE_RULE:
            command_list.append(raterule_template % (sym, math, rid))
        else:
            next

    for i in inits:
        sym = i.getSymbol()
        math = libsbml.formulaToL3String(i.getMath())
        command_list.append(initassign_template % (sym, math))

    commands = "\n".join(command_list)
    commands = sub(r"\w+='?del'?(?=[,)])", "", commands)
    commands = sub(r"\((, )+", "(", commands)
    commands = sub(r"(, )+\)", ")", commands)
    commands = sub("(, )+", ", ", commands)
    return commands


def writeCodeFromFile(filename):
    reader = libsbml.SBMLReader()
    doc = reader.readSBMLFromFile(filename)
    if doc.getNumErrors() > 0:
        raise SystemExit(doc.getError(0))
    return writeCode(doc)


def writeCodeFromString(sbmlstring):
    reader = libsbml.SBMLReader()
    doc = reader.readSBMLFromString(sbmlstring)
    return writeCode(doc)
