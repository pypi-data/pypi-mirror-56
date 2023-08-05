#!/usr/bin/env python

import unittest
from textwrap import dedent as dd

from lark import Lark

from dummy import DummyToken, DummyRule, DummyConverter

class TestDummy(unittest.TestCase):
    def setUp(self):
        # see the full text diffs in error reporting
        self.maxDiff = None

    def test_token(self):
        """ basic token tests"""
        t0 = DummyToken("t0", "abc", False, "Comment")
        t1 = DummyToken("t1", "[123]+", True, "Comment")

        self.assertEqual(t0.name, "t0")
        self.assertEqual(t0.pattern, "abc")
        self.assertEqual(t0.regex, False)
        self.assertEqual(t0.hlgroup, "Comment")
        self.assertEqual(t0.to_string(), 
            "token t0 \"abc\" False Comment")

        self.assertEqual(t1.name, "t1")
        self.assertEqual(t1.pattern, "[123]+")
        self.assertEqual(t1.regex, True)
        self.assertEqual(t1.hlgroup, "Comment")
        self.assertEqual(t1.to_string(), 
            "token t1 \"[123]+\" True Comment")

    def test_rule(self):
        """
        this tests basic token/rule assembly and accessors. It does not
        test the logic for the machinery that does automates this 
        assembly, though.
        """
        # these only highlight the delims
        tstart0 = DummyToken("START_DELIM_LB", "{", False, "Delim")
        tend0   = DummyToken("END_DELIM_RB", "}", False, "Delim")

        # these cause the whole group to be highlighted
        tstart1 = DummyToken("START_COMMENT", "/*", False, "Comment")
        tend1   = DummyToken("END_COMMENT", "*/", False, "Comment")

        r0 = DummyRule("r0", True)
        r1 = DummyRule("r1", False)
        
        # only end-token highlighting
        r2 = DummyRule("r2", False)
        r2.append_token(tstart0)
        r2.append_subrule(r0)
        r2.append_subrule(r1)
        r2.append_token(tend0)

        # full highlighting
        r3 = DummyRule("r3", False)
        r3.append_token(tstart1)
        r3.append_subrule(r0)
        r3.append_subrule(r2)
        r3.append_token(tend1)

        # no end token
        r4 = DummyRule("r4", False)
        r4.append_token(tstart1)
        r4.append_subrule(r0)
        r4.append_token(tend1)
        r4.append_subrule(r1)

        # no start token
        r5 = DummyRule("r5", False)
        r5.append_subrule(r0)
        r5.append_token(tstart1)
        r5.append_subrule(r1)
        r5.append_token(tend1)

        r3.append_subrule(r2)
        with self.assertRaisesRegex(Exception, ".* is already a subrule"):
            r3.append_token(r2)

        with self.assertRaisesRegex(Exception, ".* is already a token"):
            r3.append_subrule(tend1)
        r3.append_token(tend1)

        self.assertEqual(r0.name, "r0")
        self.assertEqual(r0.root, True)
        self.assertIsNone(r0.start_token)
        self.assertIsNone(r0.end_token)
        self.assertIsNone(r0.hlgroup)
        self.assertEqual(len(r0.subrules), 0)
        self.assertEqual(len(r0.tokens), 0)
        self.assertEqual(len(r0.items), 0)

        self.assertEqual(r1.name, "r1")
        self.assertEqual(r1.root, False)
        self.assertIsNone(r1.start_token)
        self.assertIsNone(r1.end_token)
        self.assertIsNone(r1.hlgroup)
        self.assertEqual(len(r1.subrules), 0)
        self.assertEqual(len(r1.tokens), 0)
        self.assertEqual(len(r1.items), 0)

        self.assertEqual(r2.name, "r2")
        self.assertEqual(r2.root, False)
        self.assertEqual(r2.start_token.name, tstart0.name)
        self.assertEqual(r2.end_token.name, tend0.name)
        self.assertIsNone(r2.hlgroup)
        self.assertEqual(len(r2.subrules), 2)
        self.assertEqual(len(r2.tokens), 2)
        self.assertEqual(len(r2.items), 4)

        self.assertEqual(r3.name, "r3")
        self.assertEqual(r3.root, False)
        self.assertEqual(r3.start_token.name, tstart1.name)
        self.assertEqual(r3.end_token.name, tend1.name)
        self.assertEqual(r3.hlgroup, "Comment")
        self.assertEqual(len(r3.subrules), 2)
        self.assertEqual(len(r3.tokens), 2)
        self.assertEqual(len(r3.items), 6)

        self.assertEqual(r4.name, "r4")
        self.assertEqual(r4.root, False)
        self.assertEqual(r4.start_token.name, tstart1.name)
        self.assertIsNone(r4.end_token)
        self.assertIsNone(r4.hlgroup)
        self.assertEqual(len(r4.subrules), 2)
        self.assertEqual(len(r4.tokens), 2)
        self.assertEqual(len(r4.items), 4)

        self.assertEqual(r5.name, "r5")
        self.assertEqual(r5.root, False)
        self.assertIsNone(r5.start_token)
        self.assertEqual(r5.end_token.name, tend1.name)
        self.assertIsNone(r5.hlgroup)
        self.assertEqual(len(r5.subrules), 2)
        self.assertEqual(len(r5.tokens), 2)
        self.assertEqual(len(r5.items), 4)

    def test_simple_nocycle(self):
        """single simple, no cycle"""
        grammar = dd("""
            start: a b c d e f
            a: DUMMY
            b: DUMMY2
            c: YUMMY1
            d: DUMMY YUMMY1
            e: e2
            e2: DUMMY2
            f: f2
            f2: YUMMY1

            DUMMY: "abc"
            YUMMY1: "abc"
            DUMMY2: /abc/
            """)
        self.assertEqual(DummyConverter(grammar).to_string(), dd("""
            token DUMMY "abc" False dummy
            token DUMMY2 "abc" True dummy
            rule a False None None None {
              DUMMY
            }
            rule b False None None None {
              DUMMY2
            }
            rule d False None None None {
              DUMMY
            }
            rule e False None None None {
              DUMMY1
              e2
            }
            """))

    def test_single_nocycle_branch(self):
        """single root node, no cycles, test branching/alias"""
        grammar = dd("""
            // rules with multi-branch
            // -----------------------
            // - a rule with one branch
            // - a rule with one branch and an alias
            // - a rule with multiple branches
            // - a rule with multiple branches and multiple aliases
            start: (br0 | br0alias)+ | (br3 | br3alias)+
            br0: DUMMY YUMMY1 DUMMY3 | (DUMMY2 DUMMY3 YUMMY1)+
            br0alias: DUMMY YUMMY1              -> br0alias_name
            br3: YUMMY1 YUMMY1 YUMMY1
                | YUMMY1 YUMMY1
                | ((DUMMY2 | DUMMY3) ~ 2)
            br3alias: DUMMY                     -> br3alias0
                | DUMMY DUMMY                   -> br3alias1
                | DUMMY DUMMY DUMMY             -> br3alias2

            DUMMY: "abc"
            YUMMY1: "abc"
            DUMMY2: /abc/
            DUMMY3: "abc"
            """)
        #self.assertEqual(DummyConverter(grammar).to_string(), dd("""
       #     syntax:
       #     - token DUMMY "abc" False dummy
       #     - token DUMMY2 "abc" True dummy
       #     - token DUMMY3 "abc" False dummy
       # """))

        # YUMMY1 is not preserved
#        self.assertEqual(len(dc.tokens), 3)
#        self.assertEqual(dc.token("DUMMY").hlgroup, "dummy")
#        self.assertEqual(dc.token("DUMMY2").hlgroup, "dummy")
#        self.assertEqual(dc.token("DUMMY3").hlgroup, "dummy")
#
#        # rules: 5
#        # branches: start=12, br0=3, br0alias=1, br3=4, br3alias=3
#        self.assertEqual(len(dc.rule("start").items), 2)
#        self.assertEqual(len(dc.rule("start").subrules), 2)
#        self.assertEqual(len(dc.rule("start").tokens), 0)
#
#        self.assertEqual(len(dc.rule("br0").items), 2)
#        self.assertEqual(len(dc.rule("br0").subrules), 2)
#        self.assertEqual(len(dc.rule("br0").tokens), 0)
#
#        self.assertEqual(len(dc.rule("br0alias_name").items), 1)
#        self.assertEqual(len(dc.rule("br0alias_name").subrules), 0)
#        self.assertEqual(len(dc.rule("br0alias_name").tokens), 1)
#
#        self.assertEqual(len(dc.rule("br3").items), 3)
#        self.assertEqual(len(dc.rule("br3").subrules), 3)
#        self.assertEqual(len(dc.rule("br3").tokens), 0)
#
#        self.assertEqual(len(dc.rule("br3alias").items), 3)
#        self.assertEqual(len(dc.rule("br3alias").subrules), 3)
#        self.assertEqual(len(dc.rule("br3alias").tokens), 0)
#
#        self.assertEqual(len(dc.rule("br3alias0").items), 1)
#        self.assertEqual(len(dc.rule("br3alias0").subrules), 0)
#        self.assertEqual(len(dc.rule("br3alias0").tokens), 1)
#
#        self.assertEqual(len(dc.rule("br3alias1").items), 2)
#        self.assertEqual(len(dc.rule("br3alias1").subrules), 0)
#        self.assertEqual(len(dc.rule("br3alias1").tokens), 1)
#
#        self.assertEqual(len(dc.rule("br3alias2").items), 3)
#        self.assertEqual(len(dc.rule("br3alias2").subrules), 0)
#        self.assertEqual(len(dc.rule("br3alias2").tokens), 1)

    def test_single_noncycle_hl(self):
        """single root node, no cycles, test branching/alias"""
        grammar = dd("""
            // direct token highlighting
            // -------------------------
            // - a rule that contains all non-hl tokens
            // - a rule that contains all hl tokens
            // - a rule that contains mixed hl tokens
            direct: nonhl | allhl | mixhl
            nonhl: (NOHL | NOHL2 | NOHL3)+
            allhl: YESHL YESHL2
            mixhl: NOHL YESHL

            // transitive syntax highlighting
            // ------------------------------
            // - a rule that contains all non-hl tokens and non-hl rule
            // - a rule that contains all non-hl tokens and hl rule
            // - a rule that contains all hl tokens and non-hl rule
            // - a rule that contains all hl tokens and hl rule
            // - a rule that contains mixed hl tokens and non-hl rule
            // - a rule that contains mixed hl tokens and hl rule
            // - a rule that contains non-hl rules 
            // - a rule that contains hl rules 
            // - a rule that contains non-hl and hl rules 
            trans:    (notok_norul | notok_rul)
                    | (tok_norul | tok_rul)
                    | (mixtok_norul | mixtok_rul)
                    | (

            // ignore non-hl tokens
            // -----------------------------
            // - leaf tokens without a match
            // - leaf tokens wit a match

            // start/end/group highlighting
            // ----------------------------
            // - no start and no end tokens in group
            // - start but no end tokens in group
            // - no start but no end tokens in group
            // - start and end tokens in a group (matching, with hlgroup)
            // - start and end tokens in a group (matching, without hlgroup)
            // - start and end tokens in a group (non-matching)
        """)

if __name__ == "__main__":
    unittest.main()

