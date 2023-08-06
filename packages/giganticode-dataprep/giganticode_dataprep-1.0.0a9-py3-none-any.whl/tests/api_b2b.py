import sys
import unittest

import dataprep.api.text as api
from dataprep.parse.model.metadata import PreprocessingMetadata
from dataprep.parse.model.placeholders import placeholders

cap = placeholders['capital']
caps = placeholders['capitals']
ws = placeholders['word_start']
we = placeholders['word_end']
cwe = placeholders['compound_word_end']
ce = placeholders['olc_end']
ne = placeholders['non_eng']
st = placeholders['string_literal']
com = placeholders['comment']

input_text='''void test_WordUeberraschungPrinter() {
    if (eps >= 0.345e+4) { // FIXME 10L
        printWord("     ...     Überraschung 0x12");
    }
}'''


class CliTest(unittest.TestCase):
    def test_empty_without_metadata(self):
        self.assertEqual([], api.nosplit(''))
        self.assertEqual([], api.basic(''))
        self.assertEqual([], api.chars(''))
        self.assertEqual([], api.bpe('', '1k'))

    def test_create_prep_config_0c1010(self):
        actual, metadata = api.nosplit(input_text, "java", no_spaces=True, return_metadata=True)

        expected = ['void', 'test_WordUeberraschungPrinter', '(', ')', '{',
                    'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', '/', '/', 'FIXME', '10l', ce,
                    'printWord', '(', '"', '.', '.', '.', 'Überraschung', '0x12', '"', ')', ';',
                    '}',
                    '}'
        ]

        expected_metadata = PreprocessingMetadata(
            nonprocessable_tokens={'void', '(', ')', '{', 'if', '>', '=', '/', '"', '.', '}', ';'},
            word_boundaries=list(range(len(expected)+1)))

        self.assertEqual(expected, actual)
        self.assertEqual(expected_metadata, metadata)

    def test_create_prep_config_xxQ0xx(self):
        actual, metadata = api.nosplit(input_text, "java", no_spaces=True, return_metadata=True, max_str_length=26)

        expected = ['void', 'test_WordUeberraschungPrinter', '(', ')', '{',
                    'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', '/', '/', 'FIXME', '10l', ce,
                    'printWord', '(', '"', '"', ')', ';',
                    '}',
                    '}'
        ]

        expected_metadata = PreprocessingMetadata(
            nonprocessable_tokens={'void', '(', ')', '{', 'if', '>', '=', '/', '"', '}', ';'},
            word_boundaries=list(range(len(expected)+1)))

        self.assertEqual(expected, actual)
        self.assertEqual(expected_metadata, metadata)

    def test_create_prep_config_xxW0xx(self):
        actual, metadata = api.nosplit(input_text, "java", no_spaces=True, return_metadata=True, max_str_length=32)

        expected = ['void', 'test_WordUeberraschungPrinter', '(', ')', '{',
                    'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', '/', '/', 'FIXME', '10l', ce,
                    'printWord', '(', '"', '.', '.', '.', 'Überraschung', '0x12', '"', ')', ';',
                    '}',
                    '}'
        ]

        expected_metadata = PreprocessingMetadata(
            nonprocessable_tokens={'void', '(', ')', '{', 'if', '>', '=', '/', '"', '.', '}', ';'},
            word_boundaries=list(range(len(expected)+1)))

        self.assertEqual(expected, actual)
        self.assertEqual(expected_metadata, metadata)

    def test_create_prep_config_xx10xx_max_str_length_500(self):
        actual, metadata = api.nosplit(input_text, "java", no_spaces=True, return_metadata=True, max_str_length=500)

        expected = ['void', 'test_WordUeberraschungPrinter', '(', ')', '{',
                    'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', '/', '/', 'FIXME', '10l', ce,
                    'printWord', '(', '"', '.', '.', '.', 'Überraschung', '0x12', '"', ')', ';',
                    '}',
                    '}'
        ]

        expected_metadata = PreprocessingMetadata(
            nonprocessable_tokens={'void', '(', ')', '{', 'if', '>', '=', '/', '"', '.', '}', ';'},
            word_boundaries=list(range(len(expected)+1)))

        self.assertEqual(expected, actual)
        self.assertEqual(expected_metadata, metadata)

    def test_create_prep_config_3xx0xx(self):
        actual = api.nosplit(input_text, "java", no_spaces=True, no_unicode=True)

        expected = ['void', 'test_WordUeberraschungPrinter', '(', ')', '{',
                    'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', '/', '/', 'FIXME', '10l', ce,
                    'printWord', '(', '"', '.', '.', '.', ne, '0x12', '"', ')', ';',
                    '}',
                    '}'
        ]

        self.assertEqual(expected, actual)

    def test_create_prep_config_x000xx(self):
        actual, metadata = api.nosplit(input_text, "java", no_spaces=True, no_com=True, no_str=True,
                                       return_metadata=True)

        expected = ['void', 'test_WordUeberraschungPrinter', '(', ')', '{',
                    'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', com,
                    'printWord', '(', st, ')', ';',
                    '}',
                    '}'
        ]

        expected_metadata = PreprocessingMetadata(
            nonprocessable_tokens={'void', '(', ')', '{', 'if', '>', '=', '}', ';'},
            word_boundaries=list(range(len(expected)+1)))

        self.assertEqual(expected, actual)
        self.assertEqual(expected_metadata, metadata)

    def test_create_prep_config_xxx00x(self):
        actual, metadata = api.nosplit(input_text, "java", return_metadata=True)

        expected = ['void', 'test_WordUeberraschungPrinter', '(', ')', '{', '\n',
                    '\t', 'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', '/', '/', 'FIXME', '10l', '\n', ce,
                    '\t', '\t', 'printWord', '(', '"', '.', '.', '.', 'Überraschung', '0x12', '"', ')', ';', '\n',
                    '\t', '}', '\n',
                    '}'
        ]

        expected_metadata = PreprocessingMetadata(
            nonprocessable_tokens={'void', '(', ')', '{', 'if', '>', '=', '/', '"', '.', '}', ';', '\n', '\t'},
            word_boundaries=list(range(len(expected)+1)))

        self.assertEqual(expected, actual)
        self.assertEqual(expected_metadata, metadata)

    def test_create_prep_config_xxx0x1(self):
        with self.assertRaises(TypeError) as context:
            api.nosplit(input_text, "java", no_spaces=True, no_case=True)

    def test_create_prep_config_xx1Fxx(self):
        actual, metadata = api.nosplit(input_text, "java", no_spaces=True, return_metadata=True, full_strings=True)

        expected = ['void', 'test_WordUeberraschungPrinter', '(', ')', '{',
                    'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', '/', '/', 'FIXME', '10l', ce,
                    'printWord', '(', '"\xa0\xa0\xa0\xa0\xa0...\xa0\xa0\xa0\xa0\xa0Überraschung\xa00x12"', ')', ';',
                    '}',
                    '}'
        ]

        expected_metadata = PreprocessingMetadata(
            nonprocessable_tokens={'void', '(', ')', '{', 'if', '>', '=', '/', '}', ';'},
            word_boundaries=list(range(len(expected)+1)))

        self.assertEqual(expected, actual)
        self.assertEqual(expected_metadata, metadata)

    def test_create_prep_config_xx0Fxx(self):
        actual, metadata = api.nosplit(input_text, "java", no_spaces=True, return_metadata=True, full_strings=True, no_str=True)

        expected = ['void', 'test_WordUeberraschungPrinter', '(', ')', '{',
                    'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', '/', '/', 'FIXME', '10l', ce,
                    'printWord', '(', st, ')', ';',
                    '}',
                    '}'
        ]

        expected_metadata = PreprocessingMetadata(
            nonprocessable_tokens={'void', '(', ')', '{', 'if', '>', '=', '/', '}', ';'},
            word_boundaries=list(range(len(expected)+1)))

        self.assertEqual(expected, actual)
        self.assertEqual(expected_metadata, metadata)

    def test_create_prep_config_xxVFxx(self):
        actual, metadata = api.nosplit(input_text, "java", no_spaces=True, return_metadata=True,
                                       full_strings=True, max_str_length=31)

        expected = ['void', 'test_WordUeberraschungPrinter', '(', ')', '{',
                    'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', '/', '/', 'FIXME', '10l', ce,
                    'printWord', '(', '""', ')', ';',
                    '}',
                    '}'
        ]

        expected_metadata = PreprocessingMetadata(
            nonprocessable_tokens={'void', '(', ')', '{', 'if', '>', '=', '/', '}', ';', '"'},
            word_boundaries=list(range(len(expected)+1)))

        self.assertEqual(expected, actual)
        self.assertEqual(expected_metadata, metadata)

    def test_create_prep_config_xxWFxx(self):
        actual, metadata = api.nosplit(input_text, "java", no_spaces=True, return_metadata=True,
                                       full_strings=True, max_str_length=32)

        expected = ['void', 'test_WordUeberraschungPrinter', '(', ')', '{',
                    'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', '/', '/', 'FIXME', '10l', ce,
                    'printWord', '(', '"\xa0\xa0\xa0\xa0\xa0...\xa0\xa0\xa0\xa0\xa0Überraschung\xa00x12"', ')', ';',
                    '}',
                    '}'
        ]

        expected_metadata = PreprocessingMetadata(
            nonprocessable_tokens={'void', '(', ')', '{', 'if', '>', '=', '/', '}', ';'},
            word_boundaries=list(range(len(expected)+1)))

        self.assertEqual(expected, actual)
        self.assertEqual(expected_metadata, metadata)

    def test_create_prep_config_xx1Fxx_500(self):
        actual, metadata = api.nosplit(input_text, "java", no_spaces=True, return_metadata=True,
                                       full_strings=True, max_str_length=500)

        expected = ['void', 'test_WordUeberraschungPrinter', '(', ')', '{',
                    'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', '/', '/', 'FIXME', '10l', ce,
                    'printWord', '(', '"\xa0\xa0\xa0\xa0\xa0...\xa0\xa0\xa0\xa0\xa0Überraschung\xa00x12"', ')', ';',
                    '}',
                    '}'
        ]

        expected_metadata = PreprocessingMetadata(
            nonprocessable_tokens={'void', '(', ')', '{', 'if', '>', '=', '/', '}', ';'},
            word_boundaries=list(range(len(expected)+1)))

        self.assertEqual(expected, actual)
        self.assertEqual(expected_metadata, metadata)

    def test_create_prep_config_0c1111(self):
        actual, metadata = api.basic(input_text, "java", no_spaces=True, no_case=True,
                                     return_metadata=True)

        expected = ['void', ws, 'test', '_', cap, 'word', cap, 'ueberraschung', cap, 'printer', we, '(', ')', '{',
                    'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', '/', '/', caps, 'fixme', '10l', ce,
                    ws, 'print', cap, 'word', we, '(', '"', '.', '.', '.', cap, 'überraschung', '0x12', '"', ')', ';',
                    '}',
                    '}'
        ]

        expected_metadata = PreprocessingMetadata(
            nonprocessable_tokens={'void', '(', ')', '{', 'if', '>', '=', '/', '"', '.', '}', ';'},
            word_boundaries=[0, 1, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27,
                             28, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 44, 45, 46])

        self.assertEqual(expected, actual)
        self.assertEqual(expected_metadata, metadata)

    def test_create_prep_config_3xx1xx(self):
        actual = api.basic(input_text, "java", no_spaces=True, no_unicode=True, no_case=True)

        expected = ['void', ws, 'test', '_', cap, 'word', cap, 'ueberraschung', cap, 'printer', we, '(', ')', '{',
                    'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', '/', '/', caps, 'fixme', '10l', ce,
                    ws, 'print', cap, 'word', we, '(', '"', '.', '.', '.', ne, '0x12', '"', ')', ';',
                    '}',
                    '}'
        ]

        self.assertEqual(expected, actual)

    def test_create_prep_config_xc01xx(self):
        actual = api.basic(input_text, "java", no_spaces=True, no_case=True, no_str=True)

        expected = ['void', ws, 'test', '_', cap, 'word', cap, 'ueberraschung', cap, 'printer', we, '(', ')', '{',
                    'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', '/', '/', caps, 'fixme', '10l', ce,
                    ws, 'print', cap, 'word', we, '(', st, ')', ';',
                    '}',
                    '}'
        ]

        self.assertEqual(expected, actual)

    def test_create_prep_config_x001xx(self):
        actual = api.basic(input_text, "java", no_spaces=True, no_case=True, no_com=True, no_str=True)

        expected = ['void', ws, 'test', '_', cap, 'word', cap, 'ueberraschung', cap, 'printer', we, '(', ')', '{',
                    'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', com,
                    ws, 'print', cap, 'word', we, '(', st, ')', ';',
                    '}',
                    '}',
        ]

        self.assertEqual(expected, actual)

    def test_create_prep_config_x011xx(self):
        actual = api.basic(input_text, "java", no_spaces=True, no_case=True, no_com=True)

        expected = ['void', ws, 'test', '_', cap, 'word', cap, 'ueberraschung', cap, 'printer', we, '(', ')', '{',
                    'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', com,
                    ws, 'print', cap, 'word', we, '(', '"', '.', '.', '.', cap,  'überraschung', '0x12', '"', ')', ';',
                    '}',
                    '}'
        ]

        self.assertEqual(expected, actual)

    def test_create_prep_config_0c12xx(self):
        actual = api.basic(input_text, "java", split_numbers=True, no_spaces=True, no_case=True)

        expected = ['void', ws, 'test', '_', cap, 'word', cap, 'ueberraschung', cap, 'printer', we, '(', ')', '{',
                    'if', '(', 'eps', '>', '=', ws, '0',  '.', '3', '4', '5', 'e', '+', '4', we, ')',
                    '{', '/', '/', caps, 'fixme', ws, '1', '0', 'l', we, ce,
                    ws, 'print', cap, 'word', we, '(', '"', '.', '.', '.', cap,  'überraschung', ws, '0', 'x', '1', '2', we, '"', ')', ';',
                    '}',
                    '}'
        ]

        self.assertEqual(expected, actual)

    def test_create_prep_config_0c1sxu(self):
        actual = api.basic(input_text, "java", stem=True, no_spaces=True)

        expected = ['void', ws, 'test', '_', 'Word', 'Ueberraschung', 'Printer', we, '(', ')', '{',
                    'if', '(', 'ep', '>', '=', ws, '0',  '.', '3', '4', '5', 'e', '+', '4', we, ')', '{', '/', '/',
                    ws, 'FIX', 'ME', we, ws, '1', '0', 'l', we, ce,
                    ws, 'print', 'Word', we, '(', '"', '.', '.', '.', 'Überraschung', ws, '0', 'x', '1', '2', we, '"', ')', ';',
                    '}',
                    '}'
        ]

        self.assertEqual(expected, actual)

    def test_create_prep_config_0c1sxl(self):
        actual = api.basic(input_text, "java", stem=True, no_case=True, no_spaces=True)

        expected = ['void', ws, 'test', '_', cap, 'word', cap, 'ueberraschung', cap, 'printer', we, '(', ')', '{',
                    'if', '(', 'ep', '>', '=', ws, '0',  '.', '3', '4', '5', 'e', '+', '4', we, ')', '{', '/', '/',
                    ws, caps, 'fix', 'me', we, ws, '1', '0', 'l', we, ce,
                    ws, 'print', cap, 'word', we, '(', '"', '.', '.', '.', cap,  'überraschung', ws, '0', 'x', '1', '2', we, '"', ')', ';',
                    '}',
                    '}'
        ]

        self.assertEqual(expected, actual)

    def test_create_prep_config_0c14xx(self):
        actual = api.bpe(input_text, '5k', "java", no_spaces=True)

        expected = ['void' + cwe, 'test', '_', 'Wor', 'd', 'U', 'eb', 'err', 'as', 'ch', 'un', 'g', 'Print', 'er' + cwe, '(' + cwe, ')' + cwe, '{' + cwe,
                    'if' + cwe, '(' + cwe, 'e', 'ps' + cwe, '>' + cwe, '=' + cwe, '0.', '34', '5', 'e+', '4' + cwe, ')' + cwe, '{' + cwe, '/' + cwe, '/' + cwe, 'FI', 'X', 'M', 'E' + cwe, '10', 'l' + cwe, ce,
                    'print', 'Wor', 'd' + cwe, '(' + cwe, '"\xa0', '\xa0\xa0', '\xa0\xa0', '.', '.', '.', '\xa0\xa0', '\xa0\xa0', '\xa0', 'Ü', 'b', 'err', 'as', 'ch', 'un', 'g', '\xa0', '0x', '12', '"' + cwe, ')' + cwe, ';' + cwe,
                    '}' + cwe,
                    '}' + cwe
        ]

        self.assertEqual(expected, actual)

    def test_create_prep_config_0c15xx(self):
        actual = api.bpe(input_text, '1k', "java", no_spaces=True)

        expected = ['void' + cwe, 'test', '_', 'Wor', 'd', 'U', 'eb', 'err', 'as', 'ch', 'un', 'g', 'P', 'r', 'int', 'er' + cwe, '(' + cwe, ')' + cwe, '{' + cwe,
                    'if' + cwe, '(' + cwe, 'e', 'p', 's' + cwe, '>' + cwe, '=' + cwe, '0.', '3', '4', '5', 'e', '+', '4' + cwe, ')' + cwe, '{' + cwe, '/' + cwe, '/' + cwe, 'FI', 'X', 'M', 'E' + cwe, '1', '0', 'l' + cwe, ce,
                    'print', 'Wor', 'd' + cwe, '(' + cwe, '"\xa0', '\xa0', '\xa0', '\xa0', '\xa0', '.', '.', '.', '\xa0', '\xa0', '\xa0', '\xa0', '\xa0','Ü', 'b', 'err', 'as', 'ch', 'un', 'g', '\xa0', '0x', '1', '2', '"' + cwe, ')' + cwe, ';' + cwe,
                    '}' + cwe,
                    '}' + cwe
        ]

        self.assertEqual(expected, actual)

    def test_create_prep_config_xxx6xx(self):
        actual = api.bpe(input_text, '10k', "java", no_spaces=True)

        expected = ['void' + cwe, 'test_', 'Word', 'U', 'eb', 'err', 'as', 'ch', 'un', 'g', 'Print', 'er' + cwe, '(' + cwe, ')' + cwe, '{' + cwe,
                    'if' + cwe, '(' + cwe, 'e', 'ps' + cwe, '>' + cwe, '=' + cwe, '0.', '34', '5', 'e+', '4' + cwe, ')' + cwe, '{' + cwe, '/' + cwe, '/' + cwe, 'FIX', 'M', 'E' + cwe, '10', 'l' + cwe, ce,
                    'print', 'Word' + cwe, '(' + cwe, '"\xa0\xa0\xa0', '\xa0\xa0', '..', '.', '\xa0\xa0', '\xa0\xa0', '\xa0', 'Ü', 'b', 'err', 'as', 'ch', 'un', 'g', '\xa0', '0x', '12', '"' + cwe, ')' + cwe, ';' + cwe,
                    '}' + cwe,
                    '}' + cwe
        ]

        self.assertEqual(expected, actual)

    def test_create_prep_config_xxx8xx(self):
        actual, metadata = api.chars(input_text, "java", no_spaces=True, return_metadata=True)

        expected = ['void' + cwe, 't', 'e', 's', 't', '_', 'W', 'o', 'r', 'd', 'U', 'e', 'b', 'e', 'r', 'r', 'a', 's', 'c', 'h', 'u', 'n', 'g', 'P', 'r', 'i', 'n', 't', 'e', 'r', cwe, '(' + cwe, ')' + cwe, '{' + cwe,
                    'if' + cwe, '(' + cwe, 'e', 'p', 's', cwe, '>' + cwe,'=' + cwe, '0', '.', '3', '4', '5', 'e', '+', '4', cwe, ')' + cwe, '{' + cwe, '/' + cwe, '/' + cwe, 'F', 'I', 'X', 'M', 'E', cwe, '1', '0', 'l', cwe, ce,
                    'p', 'r', 'i', 'n', 't', 'W', 'o', 'r', 'd', cwe, '(' + cwe, '"', 
                    '\xa0', '\xa0', '\xa0', '\xa0', '\xa0', '.', '.', '.', 
                    '\xa0', '\xa0', '\xa0', '\xa0', '\xa0', 'Ü', 'b', 'e', 'r', 'r', 'a', 's', 'c', 'h', 'u', 'n', 'g', '\xa0', '0', 'x', '1', '2', '"', cwe, ')' + cwe, ';' + cwe,
                    '}' + cwe,
                    '}' + cwe
        ]

        expected_metadata = PreprocessingMetadata(
            nonprocessable_tokens={'void', '(', ')', '{', 'if', '>', '=', '/', '}', ';'},
            word_boundaries=[0, 1, 31, 32, 33, 34, 35, 36, 40, 41, 42, 51, 52, 53, 54, 55, 61, 65, 66, 76, 77, 110, 111, 112, 113, 114])

        self.assertEqual(expected, actual)
        print(expected_metadata)
        print(metadata)
        self.assertEqual(expected_metadata, metadata)

    def test_create_prep_config_xxx10x(self):
        actual = api.basic(input_text, "java", no_case=True)

        expected = ['void', ws, 'test', '_', cap, 'word', cap, 'ueberraschung', cap, 'printer', we, '(', ')', '{', '\n',
                    '\t', 'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', '/', '/', caps, 'fixme', '10l', '\n', ce,
                    '\t', '\t', ws, 'print', cap, 'word', we, '(', '"', '.', '.', '.', cap, 'überraschung', '0x12', '"', ')', ';', '\n',
                    '\t', '}', '\n'
                    , '}'
        ]

        self.assertEqual(expected, actual)

    def test_create_prep_config_xxx1x1(self):
        actual = api.basic(input_text, "java", no_spaces=True)

        expected = ['void', ws, 'test', '_', 'Word', 'Ueberraschung', 'Printer', we, '(', ')', '{',
                    'if', '(', 'eps', '>', '=', '0.345e+4', ')', '{', '/', '/', 'FIXME', '10l', ce,
                    ws, 'print', 'Word', we, '(', '"', '.', '.', '.', 'Überraschung', '0x12', '"', ')', ';',
                    '}',
                    '}'
        ]

        self.assertEqual(expected, actual)

    def test_create_prep_config_0c1300(self):
        actual = api.basic(input_text, "java", split_numbers=True, ronin=True)

        expected = ['void', ws, 'test', '_', 'Word', 'Ueberraschung', 'Printer', we, '(', ')', '{',  '\n',
                    '\t', 'if', '(', 'eps', '>', '=', ws ,'0', '.', '3', '4', '5', 'e', '+', '4', we, ')', '{', '/', '/', ws, 'FIX', 'ME', we, ws, '1', '0', 'l', we, '\n', ce,
                    '\t', '\t', ws, 'print', 'Word', we, '(', '"', '.', '.', '.', 'Überraschung', ws, '0', 'x', '1', '2', we, '"', ')', ';', '\n',
                    '\t', '}', '\n',
                    '}'
        ]

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
