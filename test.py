from script import parse_stylus_entry


data = """/* ==UserStyle==
@name           xillybus.com/tutorials/pci-express-tlp-pcie-primer-tutorial-guide-2 - May 2024
@namespace      github.com/openstyles/stylus
@version        1.0.0
@description    A new userstyle
@author         Me
==/UserStyle== */

@-moz-document url-prefix("https://xillybus.com/tutorials/") {
    #sidebar-primary { display: none}
    #content { width: 98.5% !important; }
    #content pre { width: 50%; margin: 0px auto; }
    #page { width: 1600px; }
}
"""


def test():
    parsed = parse_stylus_entry(data)
    assert parsed.url == "https://xillybus.com/tutorials/"
    assert parsed.match_type == "url-prefix"
    assert parsed.source == """#sidebar-primary { display: none}
#content { width: 98.5% !important; }
#content pre { width: 50%; margin: 0px auto; }
#page { width: 1600px; }"""
