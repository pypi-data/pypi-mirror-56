# -*- coding: utf-8 -*-
import unittest
from knesset_data.protocols.committee import CommitteeMeetingProtocol
import os
from knesset_data.utils.testutils import TestCaseFileAssertionsMixin
from knesset_data.non_knesset_data.open_knesset import get_all_mk_names
from knesset_data.non_knesset_data.mocks import MOCK_OPEN_KNESSET_GET_ALL_MK_NAMES_RESPONSE


class TestCommitteeMeetings(unittest.TestCase, TestCaseFileAssertionsMixin):

    maxDiff = None

    def setUp(self):
        source_doc_file_name = os.path.join(os.path.dirname(__file__), '20_ptv_317899.doc')
        self.protocol_generator = CommitteeMeetingProtocol.get_from_filename(source_doc_file_name)

    def test_text(self):
        with self.protocol_generator as protocol:
            protocol_text = protocol.text
            assert protocol.parse_method == 'antiword'
            self.assertFileContents(
                expected_file_name=os.path.join(os.path.dirname(__file__), '20_ptv_317899_processed.txt'),
                actual_content=protocol_text
            )

    def test_attending_members(self):
        with self.protocol_generator as protocol:
            self.assertEqual([u"משה גפני", u"מיקי לוי"],
                             protocol.find_attending_members([u"סתיו שפיר", u"משה גפני", u"מיקי לוי"]))

    def test_parts(self):
        with self.protocol_generator as protocol:
            parts = protocol.parts
            self.assertProtocolPartEquals(parts[0], u"", u"""הכנסת העשרים

מושב שני

פרוטוקול מס' 189

מישיבת ועדת הכספים

יום שלישי, כ"ו בכסלו התשע"ו (08 בדצמבר 2015), שעה 10:00""")
            self.assertProtocolPartEquals(parts[1],
                                          u"""סדר היום""",
                                          u"""צו תעריף המכס והפטורים ומס קנייה על טובין (הוראת שעה מס' 11), התשע"ה-2015 (ממירים – הטלת מכס על יבוא ממירים אלקטרוניים)""")
            self.assertProtocolPartEquals(parts[2],
                                          u"""נכחו""",
                                          u"""חברי הוועדה: משה גפני – היו"ר

מיקי לוי""")
            self.assertProtocolPartEquals(parts[3],
                                          u"""מוזמנים""",
                                          u"""איריס וינברגר - סגנית בכירה ליועמ"ש, משרד האוצר

גיא גולדמן - עוזר ראשי מחלקה משפטית, משרד האוצר

עמוס יוגב - מנהל תחום סיווג ארצי, משרד האוצר

קובי בוזו - מנהל תחום בכיר תכנון וכלכלה, משרד האוצר

רפאל חדד - מנהל פיתוח עסקים, משרד הכלכלה

שאול ששון - מנהל תחום תעשיות, משרד הכלכלה

גילה ורד - עו"ד, הרשות השניה לטלוויזיה ורדיו

חניתה חפץ - לוביסטית (פוליסי), מייצגת את סלקום""")
            self.assertProtocolPartEquals(parts[4], u"""ייעוץ משפטי""", u"""שלומית ארליך""")
            self.assertProtocolPartEquals(parts[5], u"""מנהל הוועדה""", u"""טמיר כהן""")
            self.assertProtocolPartEquals(parts[6], u"""רישום פרלמנטרי""", u"""הדס צנוירט

צו תעריף המכס והפטורים ומס קנייה על טובין (הוראת שעה מס' 11), התשע"ה-2015 (ממירים – הטלת מכס על יבוא ממירים אלקטרוניים)""")
            self.assertProtocolPartEquals(parts[7],
                                          u"""היו"ר משה גפני""",
                                          u"""בוקר טוב, אני מתכבד לפתוח את ישיבת ועדת הכספים. יש לנו היום צווים, תעריפי מכס. צו תעריף המכס והפטורים ומס קנייה על טובין (הוראת שעה מס' 11), התשע"ו-2015 (ממירים – הטלת מכס על יבוא ממירים אלקטרוניים). מי מציג את הצו? בבקשה.""")
            self.assertProtocolPartEquals(parts[8],
                                          u"""קובי בוזו""",
                                          u"""בוקר טוב. קובי בוזו, רשות המסים. לצדי גיא גולדמן. לפני כחצי שנה היינו בוועדת הכספים בנושא של ממירים, וביקשנו, בשיתוף עם משרד הכלכלה, להמיר את מס הקנייה בשיעור 10% על ממירים, למכס בשיעור 10% על ממירים.""")

    def test_protocol_attendenace_strange_title(self):
        source_doc_file_name = os.path.join(os.path.dirname(__file__), '20_ptv_321195.doc')
        protocol_generator = CommitteeMeetingProtocol.get_from_filename(source_doc_file_name)
        with protocol_generator as protocol:
            self.assertEqual([u"קארין אלהרר", u"דוד אמסלם", u"אוסאמה סעדי"],
                             protocol.find_attending_members([u"קארין אלהרר", u"דוד אמסלם", u"אוסאמה סעדי"]))

    def test_attending_members_invalid_data(self):
        # file does not exist
        with CommitteeMeetingProtocol.get_from_filename('/foo/bar/baz') as protocol:
            with self.assertRaises(IOError): protocol.find_attending_members([])
        # no text
        with CommitteeMeetingProtocol.get_from_text(None) as protocol:
            self.assertEqual([], protocol.find_attending_members([]))

    def test_missing_member_issue132(self):
        # TODO: switch to env_conditional_mock function when PR #9 is merged
        if os.environ.get("NO_MOCKS", "") == "1":
            all_mk_names = get_all_mk_names()
        else:
            all_mk_names = MOCK_OPEN_KNESSET_GET_ALL_MK_NAMES_RESPONSE
        mks, mk_names = all_mk_names
        with CommitteeMeetingProtocol.get_from_filename(os.path.join(os.path.dirname(__file__), '20_ptv_367393.doc')) as protocol:
            attending_members = protocol.find_attending_members(mk_names)
            self.assertEqual(attending_members, [u"אוסאמה סעדי",
                                                 u"אורי מקלב",
                                                 u"זאב בנימין בגין",
                                                 u"יוליה מלינובסקי",
                                                 # this MK has extra space which caused him not to be found
                                                 # now we search the stripped name
                                                 # but the return value still has the extra space (as provided)
                                                 u"מיכאל מלכיאלי ",
                                                 u"רויטל סויד",
                                                 u"בנימין בגין",])

    @unittest.skipIf(not os.environ.get('TIKA_SERVER_ENDPOINT'), 'docx parsing requires tika server')
    def test_docx_protocol_attendees(self):
        source_doc_file_name = os.path.join(os.path.dirname(__file__), '20_ptv_502208.doc')
        protocol_generator = CommitteeMeetingProtocol.get_from_filename(source_doc_file_name)
        with protocol_generator as protocol:
            self.assertEqual(['איתן כבל', 'יצחק וקנין', "עבד אל חכים חאג' יחיא",
                              'איתן ברושי', 'שרן השכל'],
                             protocol.find_attending_members([u"איתן כבל", u"יצחק וקנין",
                                                              u"עבד אל חכים חאג' יחיא",
                                                              u"איתן ברושי", u"שרן השכל"]))
            self.assertEqual({'mks': ['איתן ברושי', 'שרן השכל', 'איתן כבל – היו"ר',
                                      'יצחק וקנין', "עבד אל חכים חאג' יחיא"],
                              'invitees': [
                                  {'name': 'צביקה כהן', 'role': 'סמנכ"ל בכיר למימון והשקעות, משרד החקלאות ופיתוח הכפר'},
                                  {'name': 'אורי צוק-בר',
                                   'role': 'סמנכ"ל מחקר כלכלה ואסטרטגיה, משרד החקלאות ופיתוח הכפר'},
                                  {'name': 'אסף לוי', 'role': 'סמנכ"ל גורמי יצור, משרד החקלאות ופיתוח הכפר'},
                                  {'name': 'דפנה טיש'}, {'name': 'עמרי איתן בן צבי'},
                                  {'name': 'עדי טל נוסבוים'},
                                  {'name': 'ליאורה עופרי'},
                                  {'name': 'עו"ד, משרד החקלאות ופיתוח הכפר'},
                                  {'name': 'עו"ד, מח\' יעוץ וחקיקה, משרד המשפטים'},
                                  {'name': 'יועמ"ש, המשרד לביטחון פנים'},
                                  {'name': 'עו"ד, המשרד להגנת הסביבה'},
                                  {'name': 'צבי אלון', 'role': 'מנכ"ל, מועצת הצמחים'},
                                  {'name': 'אמיר שניידר'},
                                  {'name': 'ירון סולומון'},
                                  {'name': 'יועמ"ש, התאחדות האיכרים והחקלאים בישראל'},
                                  {'name': 'מנהל המחלקה להתיישבות, האיחוד החקלאי'},
                                  {'name': 'אריאל ארליך', 'role': 'ראש מחלקת ליטיגציה, פורום קהלת'},
                                  {'name': 'מיכל זליקוביץ', 'role': 'נציגה, פורום קהלת'},
                                  {'name': 'יעל שביט', 'role': 'שדלן/ית'}],
                              'legal_advisors': ['איתי עצמון'],
                              'manager': ['לאה ורון']},
                             protocol.attendees)

    @unittest.skipIf(not os.environ.get('TIKA_SERVER_ENDPOINT'), 'docx parsing requires tika server')
    def test_docx_protocol_parts(self):
        source_doc_file_name = os.path.join(os.path.dirname(__file__), '20_ptv_502208.doc')
        protocol_generator = CommitteeMeetingProtocol.get_from_filename(source_doc_file_name)
        with protocol_generator as protocol:
            self.assertProtocolPartEquals(protocol.parts[0],
                                          '',
                                          u"""פרוטוקול של ישיבת ועדה

הכנסת העשרים

הכנסת



12
ועדת הכלכלה
27/06/2018


מושב רביעי



פרוטוקול מס' 800
מישיבת ועדת הכלכלה
יום רביעי, י"ד בתמוז התשע"ח (27 ביוני 2018), שעה 9:00""")
            self.assertProtocolPartEquals(protocol.parts[1],
                                          u"""סדר היום""",
                                          u"""הצעת חוק מועצת הצמחים (ייצור ושיווק) (תיקון מס' 10), התשע"ד-2014""")
            self.assertProtocolPartEquals(protocol.parts[2],
                                          u"""נכחו""",
                                          u"""""")
            self.assertProtocolPartEquals(protocol.parts[3],
                                          u"""חברי הוועדה:""",
                                          u"""איתן כבל – היו"ר
יצחק וקנין
עבד אל חכים חאג' יחיא""")
            self.assertProtocolPartEquals(protocol.parts[4],
                                          u"""חברי הכנסת""",
                                          u"""איתן ברושי
שרן השכל""")
            self.assertProtocolPartEquals(protocol.parts[5],
                                          u"""נכחו:""",
                                          u"""""")
            self.assertProtocolPartEquals(protocol.parts[6],
                                          u"""מוזמנים:""",
                                          u"""צביקה כהן - סמנכ"ל בכיר למימון והשקעות, משרד החקלאות ופיתוח הכפר

אורי צוק-בר - סמנכ"ל מחקר כלכלה ואסטרטגיה, משרד החקלאות ופיתוח הכפר

אסף לוי - סמנכ"ל גורמי יצור, משרד החקלאות ופיתוח הכפר

דפנה טיש
עמרי איתן בן צבי
עדי טל נוסבוים
ליאורה עופרי
	–
–
–
–
	עו"ד, משרד החקלאות ופיתוח הכפר
עו"ד, מח' יעוץ וחקיקה, משרד המשפטים
יועמ"ש, המשרד לביטחון פנים
עו"ד, המשרד להגנת הסביבה

צבי אלון - מנכ"ל, מועצת הצמחים

אמיר שניידר
ירון סולומון
	–
–
	יועמ"ש, התאחדות האיכרים והחקלאים בישראל
מנהל המחלקה להתיישבות, האיחוד החקלאי

אריאל ארליך - ראש מחלקת ליטיגציה, פורום קהלת

מיכל זליקוביץ - נציגה, פורום קהלת

יעל שביט - שדלן/ית""")

    def assertProtocolPartEquals(self, part, header, body):
        try:
            self.assertEqual(part.header, header)
        except Exception as e:
            print("--expected-header=", header, "--")
            print("--actual-header=", part.header, "--")
            raise
        try:
            self.assertEqual(part.body, body)
        except Exception as e:
            print("--expected-body = ", body, "--")
            print("--actual-body = ", part.body, "--")
            raise

