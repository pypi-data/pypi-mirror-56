""" Inject SVG content into existing SVG files.

Relies on `xml.etree.ElementTree` (in short `ET`)
for SVG/XML element representation.
"""

import xml.etree.ElementTree as ET

import svgpipe

INJ_POS_BEFORE = 1
INJ_POS_AFTER = 2

class SVGDocInj(svgpipe.SVGDoc):
    """ Inject graphical content into an existing SVG document.

    An `InjectPoint` can be obtained via `*_injectpoint`
    methods. Multiple injectpoints can be used simultaneously.
    """

    def get_layer_injectpoint(self, id, hrange, vrange,
                              group=None, **delta_hv):
        """ Get a `ScaledInjectPoint` for injecting content.

            The element for injection will be the SVG `g`
            element representing the layer with the given `id`.

            Transformation parameters will be based on the
            document's top-level element's `viewBox` and the
            given ranges.

            `hrange`, `vrange`, `delta_h`, `delta_v`:
            cf. WorldDocTrafo.
            """
        target_el = self.get_layer(id)
        if not target_el:
            raise NotFoundError("No Layer with id=%s" % id)
        ### if group element is given, insert it as inj. target
        if group is not None:
            g = ET.fromstring(group)
            target_el.append(g)
            target_el = g
        return ScaledInjectPoint(target_el,
                                 self.get_viewbox(),
                                 hrange, vrange,
                                 **delta_hv)

    def get_poly_injectpoint(self, tag, id):
        """ An `InjectPoint` for polygon/polyline with given `id`."""
        poly = self.get_svg_element(tag, id)
        return InjectPoint(poly)

    def trafo_from_rect(self, id, hrange, vrange,
                        flip_y=False, **delta_hv):
        """ Transformation: World coords into a document area.

        The geometry of the SVG rect with `id` defines the
        target area in the document, into which the visible
        area in the world  (given by `hrange` and `vrange`)
        gets projected.

        `hrange`, `vrange`, `flip_y`, `delta_h`, `delta_v`:
        cf. WorldDocTrafo.
        """
        target_el = self.get_svg_element('rect', id)
        if target_el is None:
            raise NotFoundError("No `rect` element with id=%s" % id)
        vbox = list(map(float, (target_el.attrib['x'],
                                target_el.attrib['y'],
                                target_el.attrib['width'],
                                target_el.attrib['height'])))
        return WorldDocTrafo(vbox, hrange, vrange,
                             flip_y, **delta_hv)


    def get_rect_injectpoint(self, id, hrange, vrange, **delta_hv):
        def _rect2group(svgelement, newattribs):
            # FIXME:
            # To just rename the tag rather than cleanly create
            # a new element is certainly not polite towards
            # the ethos of engineering.
            # However, it avoids finding parents and indices,
            # which is not straightforward in ElementTree.
            svgelement.tag = svgelement.tag.replace('rect','g')
            svgelement.attrib = newattribs
            return svgelement

        target_el = self.get_svg_element('rect', id)
        if target_el is None:
            raise NotFoundError("No `rect` element with id=%s" % id)
        vbox = list(map(float, (target_el.attrib['x'],
                                target_el.attrib['y'],
                                target_el.attrib['width'],
                                target_el.attrib['height'])))
        injectrect_copy = ET.fromstring(ET.tostring(target_el))
        injectrect_copy.attrib['opacity'] = "0.452"
        target_el = _rect2group(target_el,
                                {'id': "INJ_%s" % id})
        target_el.append(injectrect_copy)
        return ScaledInjectPoint(target_el, vbox,
                                 hrange, vrange, **delta_hv)

    def save(self, file):
        self.tree.write(file, encoding="utf8")

class WorldDocTrafo(object):
    """ Transform world coords into document coordinates.

    Convention:

    `h`, `v`: horizontal and vertical coords in some
        world/source/data/user-chosen coordinate system
        Horizontal and vertical world coords can have
        different (physical) units; which corresponds to s
        eparate scale factors for each dimension.
        World coordinates have to be numbers without unit.

    `x`, `y`: document coordinates as they will
        appear in the final SVG document. The default unit of the
        document is assumed to be pixels.

    `__init__` dynamically creates the tranformation functions
        `h2x` and `v2y` as instance properties (not methods!).
        Alternative delta calculation functions can be defined.
        """

    def __init__(self, viewbox, hrange, vrange,
                 flip_y=False, delta_h=None, delta_v=None):
        """ Initialize scale factors and transformation functions.

        `viewbox`:  SVG canonical form `(x,y,width,height)`
            but with x, y, width, and height being `float`.

        `hrange`, `vrange`:
            A 'view' on the data (world coords).

        `delta_h`, `delta_v` (optional): If defined they
            override the canonical difference operation `-` for
            delta calculation on world coordinates.
            This can be useful for cases where the built-in `-`
            is not suitable such as for non-trivial numeric
            representations with, say, python's `datetime` and
            `timedelta` which needs conversion for further
            calculations.
            """
        ### Define the View on the data: horizontal, vertical
        self.h1, self.h2 = hrange
        self.v1, self.v2 = vrange
        ### document dimensions: x, y
        self.x1, self.y1, width, height = viewbox
        ### init scale factors and transformation functions
        if delta_h is not None:
            # non-trivial delta calculation function
            self.hx_factor = width / delta_h(self.h1, self.h2)
            self.h2x = lambda h,                 \
                              h1=self.h1,        \
                              x1=self.x1,        \
                              sc=self.hx_factor, \
                              d=delta_h : d(h1,h)*sc + x1
        else:
            # use simple and fast `-`
            self.hx_factor = width / (self.h2-self.h1)
            self.h2x = lambda h,           \
                              h1=self.h1,  \
                              x1=self.x1,  \
                              sc=self.hx_factor : (h-h1)*sc + x1

        if flip_y:
            self.y1 += height
            flipfactor_y = -1
        else:
            flipfactor_y = 1
        if delta_v is not None:
            # non-trivial delta calculation function
            self.vy_factor = heigth / delta_v(self.v1, self.v2)
            self.v2y = lambda v,                              \
                              v1=self.v1,                     \
                              y1=self.y1,                     \
                              sc=self.vy_factor*flipfactor_y, \
                              d=delta_v : d(v1,v)*sc + y1
        else:
            # use simple and fast `-`
            self.vy_factor = height / (self.v2-self.v1)
            self.v2y = lambda v,                              \
                              v1=self.v1,                     \
                              y1=self.y1,                     \
                              sc=self.vy_factor*flipfactor_y  \
                              : (v-v1)*sc + y1

    def h2x(h):
        """ Horizontal world coords `h` --> document x-coordinates.

        This stub will be replaced by __init__.
        """
        raise Exception("Internal error: h2x was not initialized properly. Please contact the administrator ,-)")

    def v2y(v):
        """ Vertical world coords `v` --> document y-coordinates.

        This stub will be replaced by __init__.
        """
        raise Exception("Internal error: h2x was not initialized properly. Please contact the administrator ,-)")


class InjectPoint:
    """Inject content into an _target_ element."""

    def __init__(self, target_element):
        """ `target_element`: An SVG element defining
            the point where new conted will get injected."""
        self.target = target_element

    def inject(self, content):
        """Inject SVG content provided as `str` or `ET.Element`."""
        if isinstance(content, ET.Element):
            self.target.append(inj)
        else:
            try:
                self.target.append(ET.fromstring(content))
            except (ET.ParseError, TypeError) as e:
                raise ParseError("Invalid type or syntax for content %s" % content)

    def _fmtpts(pts):
        ### FIXME: A non-float argument should fail!
        ### Should be ok
        # fmtpts = " ".join(["{:f},{:f}".format(x,y)
        #                    for x,y in pts])
        #
        # but format weirdly accepts datetime for {:g}
        #
        # >>> import datetime as DT
        # >>> DT.datetime(2017,4,6)
        # datetime.datetime(2017, 4, 6, 0, 0)
        # >>> "{:.9g}".format(DT.datetime(2017,4,6))
        # '.9g'
        #
        # Workaround 1:
        #
        # for x,y, in pts:
        #     if type(x) is not in  [int, float]:
        #         raise TypeError("There should not be %s in %s"
        #                         % (DT.datetime, pts))
        #     if type(x) is not in  [int, float]:
        #         raise TypeError("There should not be %s in %s"
        #                         % (DT.datetime, pts))

        # Workaround 2, use old-fashioned formatting:
        return " ".join([('%f' % x).rstrip('0').rstrip('.')
                         + "," +
                         ('%f' % y).rstrip('0').rstrip('.')
                         for x,y in pts])

    def inject_points(self, pts, pos=INJ_POS_AFTER, trafo=None):
        """ Inject points into an existing polygon or polyline.

        `pts`: a list of points [(x1,y1), (x2,y2), ...]

        `pos` (optional): Where to insert the new points?
            `INJ_POS_BEFORE`: before or ...
            `INJ_POS_AFTER`: ... after the exisiting point data

        `trafo` (optional): Transform point coordinates according
            to a given `WorldDocTrafo`.
        """
        if trafo is not None:
            pts = [(trafo.h2x(h),trafo.v2y(v))
                   for (h,v) in pts]
        if 'points' in self.target.attrib:
            if pos == INJ_POS_BEFORE:
                self.target.attrib['points'] = (
                        InjectPoint._fmtpts(pts) + " "
                        + self.target.attrib['points'])
            elif pos == INJ_POS_AFTER:
                self.target.attrib['points'] += (
                        " " + InjectPoint._fmtpts(pts))
            else:
                raise NotImplementedError("inject_points does not handle this position: %s" % pos)
        else:
            self.target.attrib['points'] = InjectPoint._fmtpts(pts)

    def inject_points_at(self, pts, index=-1, trafo=None):
        """ Less efficient than `inject_points`, more flexible positioning.

        `idx`: Insert position, cf. `index` in pythons `list.insert`.
        """
        if trafo is not None:
            pts = [(trafo.h2x(h),trafo.v2y(v))
                   for (h,v) in pts]
        existpts = self.target.attrib['points'].split()
        existpts.insert(index, InjectPoint._fmtpts(pts))
        self.target.attrib['points'] = " ".join(existpts)

    def replace_point_at(self, p, index=-1, trafo=None):
        """ Replace an existing point by a given point `p`.

        `idx`: Position of the point being replaced
            (cf. `index` in pythons `list.insert`).
        """
        if trafo is not None:
            h, v = p
            p = trafo.h2x(h), trafo.v2y(v)
        existpts = self.target.attrib['points'].split()
        existpts[index] = InjectPoint._fmtpts([p])
        self.target.attrib['points'] = " ".join(existpts)

    def replace_all_points(self, pts, trafo=None):
        """ Replace all points of an existing polygon or polyline.

        `pts`: list of new points [(x1,y1), (x2,y2), ...]

        `trafo` (optional): Transform point coordinates according
            to a given `WorldDocTrafo`.
        """
        if trafo is not None:
            pts = [(trafo.h2x(h),trafo.v2y(v))
                   for (h,v) in pts]
        self.target.attrib['points'] = InjectPoint._fmtpts(pts)

class ScaledInjectPoint(InjectPoint, WorldDocTrafo):
    """ Scale and inject SVG content into a target area/element.

        `ScaledInjectPoint` is derived from `WorldDocTrafo`
        and combines a target SVG element with specific scaling
        parameters for injecting content into a rectangular
        target area (e.g. derived from the geometry of the `rect`
        element or its `viewBox`).
        """

    def __init__(self, target_element, viewBox, hrange, vrange,
                 **delta_hv):
        """ Initialises both superclasses."""
        InjectPoint.__init__(self, target_element)
        WorldDocTrafo.__init__(self, viewBox, hrange, vrange, **delta_hv)
