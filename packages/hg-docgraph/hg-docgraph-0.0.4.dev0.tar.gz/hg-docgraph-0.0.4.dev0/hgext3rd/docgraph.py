from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import os.path

from mercurial.i18n import _
from mercurial import (
    context,
    cmdutil,
    node as nodemod,
    registrar,
    scmutil,
    util,
    formatter,
    templatekw
)

stringify48 = True
if not util.safehasattr(cmdutil, 'rendertemplate'):
    # mercurial <= 4.7
    from mercurial import templater as tmplmodule
    stringify48 = False

import pygraphviz

__author__ = """Boris Feld (boris.feld@octobus.net)"""
testedwith = "4.6 4.7 4.8 4.9 5.0"
minimumhgversion = "4.6"

cmdtable = {}

commandfunc = registrar.command

command = commandfunc(cmdtable)

NORMAL_COLOR = "#7F7FFF"
OBSOLETE_COLOR = "#DFDFFF"
ORPHAN_COLOR = "#FF4F4F"

DEFAULT_NODE_ARGS = {
    "fixedsize": "true",
    "width": 0.5,
    "height": 0.5,
    'style': "filled",
    'fillcolor': NORMAL_COLOR,
    'shape': "pentagon",
    "pin": "true"
}

PUBLIC_NODE_ARGS = {"shape": "circle"}
DRAFT_NODE_ARGS = {"shape": "pentagon"}
SECRET_NODE_ARGS = {"shape": "square"}

OBSOLETE_NODE_ARGS = {"fillcolor": OBSOLETE_COLOR, "style": "dotted, filled"}
ORPHAN_NODE_ARGS = {"fillcolor": ORPHAN_COLOR}
PHASE_DIVERGENT_NODE_ARGS = {}
CONTENT_DIVERGENT_NODE_ARGS = ORPHAN_NODE_ARGS
EXTINCT_NODE_ARGS = OBSOLETE_NODE_ARGS

NORMAL_EDGES = {
    "penwidth": "2.0",
    }

OBSOLETE_EDGES = {
    "style": "dashed",
    "minlen": 0,
    "dir": "back",
    "arrowtail": "dot",
    "penwidth": "2.0",
}

columns = {}


@command(b'docgraph', [
        (b'', b'rankdir', b'BT', _('randir graph property'), _('DIR')),
        (b'r', b'rev', [], _('import up to source revision REV'), _('REV')),
        (b'o', b'output', b'hg.png', _('image output filename'), _('OUTPUT')),
        (b'T', b'template', b'{rev}', _('display with template'), _('TEMPLATE')),
        (b'', b'big', True, _('show big nodes')),
        (b'', b'arrowhead', b'', _('show arrow heads')),
        (b'', b'obsarrowhead', b'', _('show obsolete arrow heads')),
        (b'', b'public', b'', _('show all changesets as public')),
        (b'', b'dot-output', b'',
         _('dot source output filename'), _('DOTOUTPUT')),
        (b'', b'sphinx-directive', False,
         _('output a ".. graphviz" sphinx directive')),
     ],
     _('hg docgraph [OPTION] {REV}'))
def docgraph(ui, repo, *revs, **opts):

    # Get revset
    revs = list(revs) + opts['rev']
    if not revs:
        revs = ['.']
    revs = scmutil.revrange(repo, revs)

    # Create a graph
    graph = pygraphviz.AGraph(strict=True, directed=True, name="Mercurial graph")

    # Set the node size
    if opts['big']:
        size = 1
    else:
        size = 0.5

    DEFAULT_NODE_ARGS['width'] = size
    DEFAULT_NODE_ARGS['height'] = size

    # Order using the rankdir passed
    graph.graph_attr['rankdir'] = opts['rankdir']
    graph.graph_attr['splines'] = "polyline"

    # Remove arrow heads of the option is passed
    if not opts["arrowhead"]:
        NORMAL_EDGES["arrowhead"] = "none"

    if not opts["obsarrowhead"]:
        OBSOLETE_EDGES["arrowtail"] = "none"

    for rev in revs:
        nargs = DEFAULT_NODE_ARGS.copy()
        ctx = repo[rev]

        group = ctx.branch()

        # Phase

        # Allow forcing all nodes to public
        if opts['public'] or ctx.phasestr() == "public":
            nargs.update(PUBLIC_NODE_ARGS)
        elif ctx.phasestr() == "draft":
            nargs.update(DRAFT_NODE_ARGS)
        elif ctx.phasestr() == "secret":
            nargs.update(SECRET_NODE_ARGS)
        else:
            assert False

        # Troubles?
        if ctx.orphan():
            nargs.update(ORPHAN_NODE_ARGS)
            group = "%s_alt" % group
        elif ctx.phasedivergent():
            nargs.update(PHASE_DIVERGENT_NODE_ARGS)
            group = "%s_bumped" % group
        elif ctx.contentdivergent():
            nargs.update(CONTENT_DIVERGENT_NODE_ARGS)
            group = "%s_alt" % group
        elif ctx.extinct():
            nargs.update(EXTINCT_NODE_ARGS)
            group = "%s_extinct" % group
        elif ctx.obsolete():
            nargs.update(OBSOLETE_NODE_ARGS)
            group = "%s_alt" % group

        # Add links
        p1 = ctx.p1()
        if p1.rev() in revs:
            graph.add_edge(p1.rev(), rev, **NORMAL_EDGES)

        p2 = ctx.p2()
        if p2 and p2.rev() in revs:
            graph.add_edge(p2.rev(), rev, **NORMAL_EDGES)

        # Obs links
        for obsmakers in repo.obsstore.successors.get(ctx.node(), ()):
            successors = obsmakers[1]

            for successor in successors:
                if successor in repo:
                    successor_rev = repo[successor].rev()
                    if successor_rev in repo:
                        graph.add_edge(rev, successor_rev,
                                       **OBSOLETE_EDGES)

        # Get the position
        if group in columns:
            column = columns[group]
        else:
            max_column = max(columns.values() + [0])
            columns[group] = max_column + 1
            column = max_column + 1

        # Label
        spec = formatter.lookuptemplate(ui, "changeset", opts['template'])
        resources = {'ctx': ctx}
        props = {'ui': ui, 'ctx': ctx, 'repo': repo}
        props.update(templatekw.keywords)
        if stringify48:
            label = cmdutil.rendertemplate(ctx, spec.tmpl, props=props)
        else:
            templater = formatter.loadtemplater(ui, spec.ref, resources=resources)
            props['templ'] = templater,
            label = tmplmodule.stringify(templater(spec.ref, **props))

        nargs['label'] = label

        graph.add_node(rev, group=group, pos="%d,%d!" % (column, rev), **nargs)

    dot_output = opts['dot_output']
    if dot_output:
        dot_output = os.path.abspath(dot_output)

        graph.write(dot_output)  # write to simple.dot
        print("Wrote %s" % dot_output)

    sphinx = opts['sphinx_directive']

    if not sphinx:
        output = os.path.abspath(opts['output'])
        graph.draw(output, prog="dot")  # draw to png using dot
        print("Wrote %s" % output)

    if sphinx:
        print(".. graphviz::\n")
        for line in graph.to_string().splitlines():
            print("    " + line)
