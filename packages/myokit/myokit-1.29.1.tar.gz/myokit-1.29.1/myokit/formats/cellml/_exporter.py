#
# Exports to CellML
#
# This file is part of Myokit.
# See http://myokit.org for copyright, sharing, and licensing details.
#
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals

import os
import xml.etree.cElementTree as et

import myokit
import myokit.units
import myokit.formats


# Quoting URI strings in Python2 and Python3
try:
    from urllib.parse import quote
except ImportError:     # pragma: no python 3 cover
    # Python 2
    from urllib import quote


# Namespaces
NS_BQBIOL = 'http://biomodels.net/biology-qualifiers/'
NS_CELLML_1_0 = 'http://www.cellml.org/cellml/1.0#'
NS_CMETA = 'http://www.cellml.org/metadata/1.0#'
NS_MATHML = 'http://www.w3.org/1998/Math/MathML'
NS_OXMETA = 'https://chaste.comlab.ox.ac.uk/cellml/ns/oxford-metadata#'
NS_RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
#NS_RDFS = 'http://www.w3.org/2000/01/rdf-schema#'
NS_TMP_DOC = 'http://cellml.org/tmp-documentation'


class CellMLExporter(myokit.formats.Exporter):
    """
    This:class:`Exporter <myokit.formats.Exporter>` creates a CellML model.
    """
    def __init__(self):
        super(CellMLExporter, self).__init__()

    def custom_unit_name(self, unit):
        """
        Creates an almost readable name for a custom Myokit unit.
        """
        import myokit.formats.cellml as cellml

        # Get preferred name
        name = str(unit)[1:-1]

        # Check if that's allowed
        if cellml.is_valid_identifier(name):
            return name

        # Create custom name

        # Split unit from multiplier part
        if ' ' in name:
            name, multiplier = name.split(' ')
        else:
            name, multiplier = name, ''

        # Treat unit parts
        name = name.replace('^', '')
        name = name.replace('/', '_per_')
        name = name.replace('*', '_')
        if name[:2] == '1_':
            # E.g. [1_per_mV]
            name = name[2:]
        elif name == '1':
            # E.g. [1 (1000)]
            name = 'dimensionless'

        # Treat multiplier
        if multiplier:
            multiplier = unit.multiplier_log_10()

            # If nice round int, then use e-notation
            if myokit._feq(multiplier, int(multiplier)):
                multiplier = '1e' + str(int(multiplier))
            else:
                multiplier = str(unit.multiplier())

            # Remove characters not allowed in CellML identifiers
            multiplier = multiplier.replace('+', '')
            multiplier = multiplier.replace('-', '_minus_')
            multiplier = multiplier.replace('.', '_dot_')
            name += '_times_' + multiplier

        return name

    def info(self):
        import inspect
        return inspect.getdoc(self)

    def model(
            self, path, model, protocol=None, add_hardcoded_pacing=True,
            pretty_xml=True):
        """
        Writes a CellML model to the given filename.

        Arguments:

        ``path``
            The path/filename to write the generated code too.
        ``model``
            The model to export
        ``protocol``
            This argument will be ignored: protocols are not supported by
            CellML.
        ``add_hardcoded_pacing``
            Set this to ``True`` to add a hardcoded pacing signal to the model
            file. This requires the model to have a variable bound to `pace`.
        ``pretty_xml``
            Set this to ``True`` to write the output in formatted "pretty"
            xml.

        Notes about CellML export:

        * CellML expects a unit for every number present in the model. Since
          Myokit allows but does not enforce this, the resulting CellML file
          may only validate with unit checking disabled.
        * Files downloaded from the CellML repository typically have a pacing
          stimulus embedded in them, while Myokit views models and pacing
          protocols as separate things. To generate a model file with a simple
          embbeded protocol, add the optional argument
          ``add_hardcoded_pacing=True``.
        * Variables annotated with an ``oxmeta`` property will be annotated
          using the oxmeta namespace in the created CellML. For example, a
          variable with the meta-data ``oxmeta: time`` will be annotated as
          ``https://chaste.comlab.ox.ac.uk/cellml/ns/oxford-metadata#time`` in
          the CellML file.

        """
        import myokit.formats.cellml as cellml

        path = os.path.abspath(os.path.expanduser(path))

        # Clear log
        self.logger().clear()
        self.logger().clear_warnings()

        # Replace the pacing variable with a hardcoded stimulus protocol
        if add_hardcoded_pacing:

            # Check for pacing variable
            if model.binding('pace') is None:
                self.logger().warn(
                    'No variable bound to "pace", unable to add hardcoded'
                    ' stimulus protocol.')
            else:
                # Clone model before making changes
                model = model.clone()

                # Get pacing variable
                pace = model.binding('pace')

                # Set basic properties for pace
                pace.set_unit(myokit.units.dimensionless)
                pace.set_rhs(0)
                pace.set_binding(None)
                pace.set_label(None)    # Should already be true...

                # Get time variable of cloned model
                time = model.time()

                # Get time unit
                time_unit = time.unit(mode=myokit.UNIT_STRICT)

                # Get correction factor if using anything other than
                # milliseconds (hardcoded below)
                try:
                    time_factor = myokit.Unit.conversion_factor(
                        'ms', time_unit)
                except myokit.IncompatibleUnitError:
                    time_factor = 1

                # Create new component for the pacing variables
                component = 'stimulus'
                if model.has_component(component):
                    root = component
                    number = 1
                    while model.has_component(component):
                        number += 1
                        component = root + '_' + str(number)
                component = model.add_component(component)

                # Move pace. This will be ok any references: since pace was
                # bound it cannot be a nested variable.
                # While moving, update its name to avoid conflicts with the
                # hardcoded names.
                pace.parent().move_variable(pace, component, new_name='pace')

                # Add variables defining pacing protocol
                qperiod = myokit.Quantity('1000 [ms]')
                qoffset = myokit.Quantity('100 [ms]')
                qduration = myokit.Quantity('2 [ms]')
                period = component.add_variable('period')
                period.set_unit(time_unit)
                period.set_rhs(qperiod * time_factor)
                offset = component.add_variable('offset')
                offset.set_unit(time_unit)
                offset.set_rhs(qoffset * time_factor)
                duration = component.add_variable('duration')
                duration.set_unit(time_unit)
                duration.set_rhs(qduration * time_factor)

                # Add corrected time variable
                ctime = component.add_variable('ctime')
                ctime.set_unit(time_unit)
                ctime.set_rhs(
                    time.qname() + ' - floor(' + time.qname()
                    + ' / period) * period')

                # Remove any child variables pace might have before changing
                # its RHS (which needs to refer to them).
                pace_kids = list(pace.variables())
                for kid in pace_kids:
                    pace.remove_variable(kid, recursive=True)

                # Set new RHS for pace
                pace.set_rhs(
                    'if(ctime >= offset and ctime < offset + duration, 1, 0)')

        # Validate model
        model.validate()

        # Get time variable
        time = model.time()

        # Create model xml element
        emodel = et.Element('model')
        emodel.attrib['xmlns'] = NS_CELLML_1_0
        emodel.attrib['xmlns:cellml'] = NS_CELLML_1_0

        # Add name in 'tmp-documentation' format
        emodel.attrib['name'] = 'generated_model'
        if 'name' in model.meta:
            dtag = et.SubElement(emodel, 'documentation')
            dtag.attrib['xmlns'] = NS_TMP_DOC
            atag = et.SubElement(dtag, 'article')
            ttag = et.SubElement(atag, 'title')
            ttag.text = model.meta['name']

        # Add custom units, create unit map
        exp_si = [si_units[x] for x in myokit.Unit.list_exponents()]
        unit_map = {}   # Add si units later

        def add_unit(unit):
            """
            Checks if the given unit needs to be added to the list of custom
            units and adds it if necessary.
            """
            # Check if already defined
            if unit is None or unit in unit_map or unit in si_units:
                return

            # Create unit name
            name = self.custom_unit_name(unit)

            # Create unit tag
            utag = et.SubElement(emodel, 'units')
            utag.attrib['name'] = name

            # Add part for each of the 7 SI units
            m = unit.multiplier()
            for k, e in enumerate(unit.exponents()):
                if e != 0:
                    tag = et.SubElement(utag, 'unit')
                    tag.attrib['units'] = exp_si[k]
                    tag.attrib['exponent'] = str(e)
                    if m != 1:
                        tag.attrib['multiplier'] = str(m)
                        m = 1

            # Or... if the unit doesn't contain any of those seven, it must be
            # a dimensionless unit with a multiplier. These occur in CellML
            # definitions when unit mismatches are "resolved" by adding
            # conversion factors as units. This has no impact on the actual
            # equations...
            if m != 1:
                tag = et.SubElement(utag, 'unit')
                tag.attrib['units'] = si_units[myokit.units.dimensionless]
                tag.attrib['exponent'] = str(1)
                tag.attrib['multiplier'] = str(m)
                # m = 1

            # Add the new unit to the list
            unit_map[unit] = name

        # Sort by name
        sortkey = lambda x: x.qname()

        # Add variable and expression units
        for var in sorted(model.variables(deep=True), key=sortkey):
            add_unit(var.unit())
            for e in var.rhs().walk(myokit.Number):
                add_unit(e.unit())

        # Add si units to unit map
        for unit, name in si_units.items():
            unit_map[unit] = name

        # Add components
        # Components can correspond to Myokit components or variables with
        # children!
        ecomps = {}     # Components/Variables: elements (tags)
        cnames = {}     # Components/Variables: names (strings)
        unames = set()  # Unique name check

        def uname(name):
            # Create a unique component name
            i = 1
            r = name + '_'
            while name in unames:
                i += 1
                name = r + str(i)
            return name

        def export_nested_var(parent_tag, parent_name, var):
            # Create unique component name
            cname = uname(parent_name + '_' + var.uname())
            cnames[var] = cname
            unames.add(cname)

            # Create element
            ecomp = et.SubElement(emodel, 'component')
            ecomp.attrib['name'] = cname
            ecomps[var] = ecomp

            # Check for nested variables with children
            for kid in sorted(var.variables(), key=sortkey):
                if kid.has_variables():
                    export_nested_var(ecomp, cname, kid)

        for comp in sorted(model.components(), key=sortkey):
            # Create unique name
            cname = uname(comp.name())
            cnames[comp] = cname
            unames.add(cname)

            # Create element
            ecomp = et.SubElement(emodel, 'component')
            ecomp.attrib['name'] = cname
            ecomps[comp] = ecomp

            # Check for variables with children
            for var in sorted(comp.variables(), key=sortkey):
                if var.has_variables():
                    export_nested_var(ecomp, cname, var)

        # Collect oxmeta annotated variables
        oxmeta_vars = {}

        # Add variables
        def add_variable(eparent, var):
            evar = et.SubElement(eparent, 'variable')
            evars[var] = evar
            evar.attrib['name'] = var.uname()

            # Weblab oxmeta id given? Then add a cmeta id to reference via RDF
            # later.
            if 'oxmeta' in var.meta:
                # Ensure cmeta namespace is defined
                if 'xmlns:cmeta' not in emodel.attrib:
                    emodel.attrib['xmlns:cmeta'] = NS_CMETA

                # Add cmeta:id to variable
                cmeta_id = var.uname()
                evar.attrib['cmeta:id'] = cmeta_id

                # Store cmeta id and annotation for later
                oxmeta_vars[cmeta_id] = var.meta['oxmeta']

            # Add units
            unit = var.unit()
            unit = unit_map[unit] if unit else 'dimensionless'
            evar.attrib['units'] = unit

            # Add initial value
            init = None
            if var.is_literal():
                init = var.rhs().eval()
            elif var.is_state():
                init = var.state_value()
            if init is not None:
                evar.attrib['initial_value'] = myokit.strfloat(init)

        evars = {}
        for parent in sorted(ecomps, key=sortkey):
            eparent = ecomps[parent]
            for var in sorted(parent.variables(), key=sortkey):
                add_variable(eparent, var)

        # Add variable interfaces, connections
        deps = model.map_shallow_dependencies(
            omit_states=False, omit_constants=False)
        for var in sorted(evars, key=sortkey):
            evar = evars[var]
            # Scan all variables, iterate over the vars they depend on
            par = var.parent()
            lhs = var.lhs()
            dps = set(deps[lhs])

            # Add dependency on time for state variables
            if var.is_state():
                dps.add(time.lhs())

            for dls in sorted(dps, key=lambda x: x.var().qname()):
                dep = dls.var()
                dpa = dep.parent()
                # Parent mismatch: requires connection
                if par != dpa:
                    # Check if variable tag is present
                    epar = ecomps[par]
                    tag = epar.find('variable[@name="' + dep.uname() + '"]')
                    if tag is None:
                        # Create variable tag
                        tag = et.SubElement(epar, 'variable')
                        tag.attrib['name'] = dep.uname()

                        # Add unit
                        unit = dep.unit()
                        unit = unit_map[unit] if unit else 'dimensionless'
                        tag.attrib['units'] = unit

                        # Set interfaces
                        tag.attrib['public_interface'] = 'in'
                        edpa = ecomps[dpa]
                        tag = edpa.find(
                            'variable[@name="' + dep.uname() + '"]')
                        tag.attrib['public_interface'] = 'out'

                        # Add connection for this variable
                        comp1 = cnames[par]
                        comp2 = cnames[dpa]
                        vname = dep.uname()

                        # Sort components in connection alphabetically to
                        # ensure uniqueness
                        if comp2 < comp1:
                            comp1, comp2 = comp2, comp1

                        # Find or create connection
                        ctag = None
                        for con in emodel.findall('connection'):
                            ctag = con.find(
                                'map_components[@component_1="'
                                + comp1 + '"][@component_2="' + comp2 + '"]')
                            if ctag is not None:
                                break
                        if ctag is None:
                            con = et.SubElement(emodel, 'connection')
                            ctag = et.SubElement(con, 'map_components')
                            ctag.attrib['component_1'] = comp1
                            ctag.attrib['component_2'] = comp2
                        vtag = con.find(
                            'map_variables[@variable_1="' + vname
                            + '"][variable_2="' + vname + '"]')
                        if vtag is None:
                            vtag = et.SubElement(con, 'map_variables')
                            vtag.attrib['variable_1'] = vname
                            vtag.attrib['variable_2'] = vname

        # Add RDF for oxmeta annotated variables
        if oxmeta_vars:
            erdf = et.SubElement(emodel, 'rdf:RDF', {
                'xmlns:bqbiol': NS_BQBIOL,
                'xmlns:oxmeta': NS_OXMETA,
                'xmlns:rdf': NS_RDF,
                #'xmlns:rdfs': NS_RDFS,
            })
            for cmeta_id in sorted(oxmeta_vars):
                annotation = oxmeta_vars[cmeta_id]
                edesc = et.SubElement(erdf, 'rdf:Description')
                edesc.attrib['rdf:about'] = '#' + cmeta_id
                eis = et.SubElement(edesc, 'bqbiol:is')
                eis.attrib['rdf:resource'] = NS_OXMETA + quote(annotation)

        # Create CellMLWriter
        writer = cellml.CellMLExpressionWriter(units=unit_map)
        writer.set_element_tree_class(et)
        writer.set_time_variable(time)

        # Add equations
        def add_child_equations(parent):
            # Add the equations to a cellml component
            try:
                ecomp = ecomps[parent]
            except KeyError:
                return
            maths = et.SubElement(ecomp, 'math')
            maths.attrib['xmlns'] = NS_MATHML
            for var in sorted(parent.variables(), key=sortkey):
                # No equation for time variable
                if var == time:
                    continue
                # Literals already have an initial value
                if var.is_literal():
                    continue
                writer.eq(var.eq(), maths)
                add_child_equations(var)

        for comp in model.components():
            add_child_equations(comp)

        # Write xml to file
        doc = et.ElementTree(emodel)
        doc.write(path, encoding='utf-8', method='xml')
        if pretty_xml:
            # Create pretty XML
            import xml.dom.minidom as m
            xml = m.parse(path)
            with open(path, 'wb') as f:
                f.write(xml.toprettyxml(encoding='utf-8'))

        # Log any generated warnings
        self.logger().log_warnings()

    def supports_model(self):
        """
        Returns ``True``.
        """
        return True


si_units = {
    myokit.units.dimensionless: 'dimensionless',
    myokit.units.A: 'ampere',
    myokit.units.F: 'farad',
    myokit.units.kat: 'katal',
    myokit.units.lux: 'lux',
    myokit.units.Pa: 'pascal',
    myokit.units.T: 'tesla',
    myokit.units.Bq: 'becquerel',
    myokit.units.g: 'gram',
    myokit.units.K: 'kelvin',
    myokit.units.m: 'meter',
    myokit.units.V: 'volt',
    myokit.units.cd: 'candela',
    myokit.units.Gy: 'gray',
    myokit.units.kg: 'kilogram',
    myokit.units.m: 'metre',
    myokit.units.s: 'second',
    myokit.units.W: 'watt',
    myokit.units.C: 'celsius',
    myokit.units.H: 'henry',
    myokit.units.L: 'liter',
    myokit.units.mol: 'mole',
    #myokit.units.rad: 'radian',   # this overwrites dimensionless
}


si_exponents = {
    -24: 'yocto',
    -21: 'zepto',
    -18: 'atto',
    -15: 'femto',
    -12: 'pico',
    -9: 'nano',
    -6: 'micro',
    -3: 'milli',
    -2: 'centi',
    -1: 'deci',
    1: 'deka',
    2: 'hecto',
    3: 'kilo',
    6: 'mega',
    9: 'giga',
    12: 'tera',
    15: 'peta',
    18: 'exa',
    21: 'zetta',
    24: 'yotta',
}

