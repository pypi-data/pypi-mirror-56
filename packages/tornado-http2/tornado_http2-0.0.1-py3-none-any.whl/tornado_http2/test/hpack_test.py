import binascii
import unittest

from tornado_http2.constants import HeaderIndexMode
from tornado_http2.hpack import HpackDecoder, HpackEncoder

test_data = [
    # Test cases from
    # http://tools.ietf.org/html/draft-ietf-httpbis-header-compression-12#appendix-C.2
    ('C.2.1', 256, False,
     [('400a 6375 7374 6f6d 2d6b 6579 0d63 7573'
       '746f 6d2d 6865 6164 6572',
       [(b'custom-key', b'custom-header', HeaderIndexMode.YES)],
       55, [(b'custom-key', b'custom-header')]),
      ]),
    ('C.2.2', 256, False,
     [('040c 2f73 616d 706c 652f 7061 7468',
       [(b':path', b'/sample/path', HeaderIndexMode.NO)],
       0, []),
      ]),
    ('C.2.3', 256, False,
     [('1008 7061 7373 776f 7264 0673 6563 7265'
       '74',
       [(b'password', b'secret', HeaderIndexMode.NEVER)],
       0, []),
      ]),
    ('C.2.4', 256, False,
     [('82',
       [(b':method', b'GET', HeaderIndexMode.YES)],
       0, []),
      ]),
    ('C.3', 256, False,
     [('8286 8441 0f77 7777 2e65 7861 6d70 6c65'
       '2e63 6f6d',
       [(b':method', b'GET', HeaderIndexMode.YES),
        (b':scheme', b'http', HeaderIndexMode.YES),
        (b':path', b'/', HeaderIndexMode.YES),
        (b':authority', b'www.example.com', HeaderIndexMode.YES)],
       57, [(b':authority', b'www.example.com')]),
      ('8286 84be 5808 6e6f 2d63 6163 6865',
       [(b':method', b'GET', HeaderIndexMode.YES),
        (b':scheme', b'http', HeaderIndexMode.YES),
        (b':path', b'/', HeaderIndexMode.YES),
        (b':authority', b'www.example.com', HeaderIndexMode.YES),
        (b'cache-control', b'no-cache', HeaderIndexMode.YES)],
       110, [(b'cache-control', b'no-cache'),
             (b':authority', b'www.example.com')]),
      ('8287 85bf 400a 6375 7374 6f6d 2d6b 6579'
       '0c63 7573 746f 6d2d 7661 6c75 65',
       [(b':method', b'GET', HeaderIndexMode.YES),
        (b':scheme', b'https', HeaderIndexMode.YES),
        (b':path', b'/index.html', HeaderIndexMode.YES),
        (b':authority', b'www.example.com', HeaderIndexMode.YES),
        (b'custom-key', b'custom-value', HeaderIndexMode.YES)],
       164, [(b'custom-key', b'custom-value'),
             (b'cache-control', b'no-cache'),
             (b':authority', b'www.example.com')]),
      ]),
    # C.4 encodes the same headers as C.3 but with huffman encoding.
    ('C.4', 256, True,
     [('8286 8441 8cf1 e3c2 e5f2 3a6b a0ab 90f4'
       'ff',
       [(b':method', b'GET', HeaderIndexMode.YES),
        (b':scheme', b'http', HeaderIndexMode.YES),
        (b':path', b'/', HeaderIndexMode.YES),
        (b':authority', b'www.example.com', HeaderIndexMode.YES)],
       57, [(b':authority', b'www.example.com')]),
      ('8286 84be 5886 a8eb 1064 9cbf',
       [(b':method', b'GET', HeaderIndexMode.YES),
        (b':scheme', b'http', HeaderIndexMode.YES),
        (b':path', b'/', HeaderIndexMode.YES),
        (b':authority', b'www.example.com', HeaderIndexMode.YES),
        (b'cache-control', b'no-cache', HeaderIndexMode.YES)],
       110, [(b'cache-control', b'no-cache'),
             (b':authority', b'www.example.com')]),
      ('8287 85bf 4088 25a8 49e9 5ba9 7d7f 8925'
       'a849 e95b b8e8 b4bf',
       [(b':method', b'GET', HeaderIndexMode.YES),
        (b':scheme', b'https', HeaderIndexMode.YES),
        (b':path', b'/index.html', HeaderIndexMode.YES),
        (b':authority', b'www.example.com', HeaderIndexMode.YES),
        (b'custom-key', b'custom-value', HeaderIndexMode.YES)],
       164, [(b'custom-key', b'custom-value'),
             (b'cache-control', b'no-cache'),
             (b':authority', b'www.example.com')]),
      ]),
    ('C.5', 256, False,
     [('4803 3330 3258 0770 7269 7661 7465 611d'
       '4d6f 6e2c 2032 3120 4f63 7420 3230 3133'
       '2032 303a 3133 3a32 3120 474d 546e 1768'
       '7474 7073 3a2f 2f77 7777 2e65 7861 6d70'
       '6c65 2e63 6f6d',
       [(b':status', b'302', HeaderIndexMode.YES),
        (b'cache-control', b'private', HeaderIndexMode.YES),
        (b'date', b'Mon, 21 Oct 2013 20:13:21 GMT', HeaderIndexMode.YES),
        (b'location', b'https://www.example.com', HeaderIndexMode.YES)],
       222, [(b'location', b'https://www.example.com'),
             (b'date', b'Mon, 21 Oct 2013 20:13:21 GMT'),
             (b'cache-control', b'private'),
             (b':status', b'302')]),
      ('4803 3330 37c1 c0bf',
       [(b':status', b'307', HeaderIndexMode.YES),
        (b'cache-control', b'private', HeaderIndexMode.YES),
        (b'date', b'Mon, 21 Oct 2013 20:13:21 GMT', HeaderIndexMode.YES),
        (b'location', b'https://www.example.com', HeaderIndexMode.YES)],
       222, [(b':status', b'307'),
             (b'location', b'https://www.example.com'),
             (b'date', b'Mon, 21 Oct 2013 20:13:21 GMT'),
             (b'cache-control', b'private')]),
      ('88c1 611d 4d6f 6e2c 2032 3120 4f63 7420'
       '3230 3133 2032 303a 3133 3a32 3220 474d'
       '54c0 5a04 677a 6970 7738 666f 6f3d 4153'
       '444a 4b48 514b 425a 584f 5157 454f 5049'
       '5541 5851 5745 4f49 553b 206d 6178 2d61'
       '6765 3d33 3630 303b 2076 6572 7369 6f6e'
       '3d31',
       [(b':status', b'200', HeaderIndexMode.YES),
        (b'cache-control', b'private', HeaderIndexMode.YES),
        (b'date', b'Mon, 21 Oct 2013 20:13:22 GMT', HeaderIndexMode.YES),
        (b'location', b'https://www.example.com', HeaderIndexMode.YES),
        (b'content-encoding', b'gzip', HeaderIndexMode.YES),
        (b'set-cookie', b'foo=ASDJKHQKBZXOQWEOPIUAXQWEOIU; max-age=3600; version=1', HeaderIndexMode.YES)],
       215, [(b'set-cookie', b'foo=ASDJKHQKBZXOQWEOPIUAXQWEOIU; max-age=3600; version=1'),
             (b'content-encoding', b'gzip'),
             (b'date', b'Mon, 21 Oct 2013 20:13:22 GMT')]),
      ]),
    # C.6 encodes the same headers as C.5 but with huffman encoding.
    ('C.6', 256, True,
     [('4882 6402 5885 aec3 771a 4b61 96d0 7abe'
       '9410 54d4 44a8 2005 9504 0b81 66e0 82a6'
       '2d1b ff6e 919d 29ad 1718 63c7 8f0b 97c8'
       'e9ae 82ae 43d3',
       [(b':status', b'302', HeaderIndexMode.YES),
        (b'cache-control', b'private', HeaderIndexMode.YES),
        (b'date', b'Mon, 21 Oct 2013 20:13:21 GMT', HeaderIndexMode.YES),
        (b'location', b'https://www.example.com', HeaderIndexMode.YES)],
       222, [(b'location', b'https://www.example.com'),
             (b'date', b'Mon, 21 Oct 2013 20:13:21 GMT'),
             (b'cache-control', b'private'),
             (b':status', b'302')]),
      ('4883 640e ffc1 c0bf',
       [(b':status', b'307', HeaderIndexMode.YES),
        (b'cache-control', b'private', HeaderIndexMode.YES),
        (b'date', b'Mon, 21 Oct 2013 20:13:21 GMT', HeaderIndexMode.YES),
        (b'location', b'https://www.example.com', HeaderIndexMode.YES)],
       222, [(b':status', b'307'),
             (b'location', b'https://www.example.com'),
             (b'date', b'Mon, 21 Oct 2013 20:13:21 GMT'),
             (b'cache-control', b'private')]),
      ('88c1 6196 d07a be94 1054 d444 a820 0595'
       '040b 8166 e084 a62d 1bff c05a 839b d9ab'
       '77ad 94e7 821d d7f2 e6c7 b335 dfdf cd5b'
       '3960 d5af 2708 7f36 72c1 ab27 0fb5 291f'
       '9587 3160 65c0 03ed 4ee5 b106 3d50 07',
       [(b':status', b'200', HeaderIndexMode.YES),
        (b'cache-control', b'private', HeaderIndexMode.YES),
        (b'date', b'Mon, 21 Oct 2013 20:13:22 GMT', HeaderIndexMode.YES),
        (b'location', b'https://www.example.com', HeaderIndexMode.YES),
        (b'content-encoding', b'gzip', HeaderIndexMode.YES),
        (b'set-cookie', b'foo=ASDJKHQKBZXOQWEOPIUAXQWEOIU; max-age=3600; version=1', HeaderIndexMode.YES)],
       215, [(b'set-cookie', b'foo=ASDJKHQKBZXOQWEOPIUAXQWEOIU; max-age=3600; version=1'),
             (b'content-encoding', b'gzip'),
             (b'date', b'Mon, 21 Oct 2013 20:13:22 GMT')]),
      ]),
]


def unhex_test_data(data):
    return bytearray(binascii.a2b_hex(''.join(data.split())))


class HpackDecoderTest(unittest.TestCase):
    def test_hpack_decoder(self):
        for name, dynamic_table_limit, encode_huffman, requests in test_data:
            decoder = HpackDecoder(dynamic_table_limit)
            for i, (data, expected, expected_dynamic_table_size,
                    expected_dynamic_table) in enumerate(requests):
                try:
                    result = decoder.decode(unhex_test_data(data))
                    self.assertEqual(result, expected)
                    if expected_dynamic_table_size is not None:
                        self.assertEqual(decoder._dynamic_table_size,
                                         expected_dynamic_table_size)
                    if expected_dynamic_table is not None:
                        self.assertEqual(list(decoder._dynamic_table),
                                         expected_dynamic_table)
                except Exception:
                    print('error in test case %s, request %d' % (name, i))
                    raise


class HpackEncoderTest(unittest.TestCase):
    def test_hpack_encoder(self):
        for name, dynamic_table_limit, encode_huffman, requests in test_data:
            encoder = HpackEncoder(dynamic_table_limit, encode_huffman)
            for i, (data, headers, expected_dynamic_table_size,
                    expected_dynamic_table) in enumerate(requests):
                try:
                    result = encoder.encode(headers)
                    self.assertEqual(result, unhex_test_data(data))
                except Exception:
                    print('error in test case %s, request %d' % (name, i))
                    raise
