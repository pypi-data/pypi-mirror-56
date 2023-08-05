# -*- coding: utf-8 -*-

import nwae.utils.Log as lg
from inspect import getframeinfo, currentframe
import mex.MatchExpression as mexpr


class UnitTest:

    TESTS = [
        {
            # Trailing '/' in '...вес / 重 /' should be removed automatically
            'mex': 'm, float, mass / 무게 / вес / 重 / ;  d, datetime, ',
            'lang': None,
            'sentences': [
                ('My mass is 68.5kg on 2019-09-08', {'m': 68.5, 'd': '2019-09-08'}),
                # float type should also work if entered integer
                ('My mass is 68kg on 2019-09-08', {'m': 68.0, 'd': '2019-09-08'}),
            ]
        },
        {
            # Trailing '/' in '...вес / 重 /' should be removed automatically
            'mex': 'm, float, dollar / dollars / $ / ^  ;   y, int, year / yr / - / ',
            'lang': None,
            'sentences': [
                # Common dollar sign '$' should be correctly bracketed in our regex
                ('My salary in year 2019 is $8888.99.', {'m': 8888.99, 'y': 2019}),
                # Common dollar sign '$' should be correctly bracketed in our regex
                ('My salary in year 2019 is $8888.99 man...', {'m': 8888.99, 'y': 2019}),
                # Another special character '^' should be correctly bracketed in our regex
                ('My salary in year 2019 is ^ 8888.99 man...', {'m': 8888.99, 'y': 2019}),
                # Another special character '-' should be correctly work also
                ('My salary in - 2019 is $ 8888.99 man...', {'m': 8888.99, 'y': 2019})
            ]
        },
        {
            # We also use the words 'test&escape' and ';' (clashes with var separator
            # but works because we escape the word using '\\;')
            # to detect diameter.
            # Need to escape special mex characters like ; if used as expression
            'mex': 'r, float, radius & r  ;'
                   + 'd, float, diameter / d / test\\/escape / \\; / + / * /\\/ / \\&   ;   ',
            'lang': 'en',
            # Sentence & Expected Result
            'sentences': [
                ('What is the volume of a sphere of radius 5.88?', {'r': 5.88, 'd': None}),
                # Ending '.' should not affect result
                ('What is the volume of a sphere of radius 5.88.', {'r': 5.88, 'd': None}),
                ('What is the volume of a sphere of radius 5.88 and 4.9 diameter?', {'r': 5.88, 'd': 4.9}),
                ('What is the volume of a sphere of radius 5.88 and 33.88 test&escape?', {'r': 5.88, 'd': 33.88}),
                ('What is the volume of a sphere of radius 5.88, 33.88;?', {'r': 5.88, 'd': 33.88}),
                # When stupid user uses '+' to detect a param, should also work, but not recommended
                ('What is the volume of a sphere of radius 5.88, +33.88?', {'r': 5.88, 'd': 33.88}),
                # Using '*' to detect diameter
                ('What is the volume of a sphere of radius 5.88, 33.88*?', {'r': 5.88, 'd': 33.88}),
                # Using '/' to detect diameter
                ('What is the volume of a sphere of radius 5.88, 33.88/?', {'r': 5.88, 'd': 33.88}),
                # Should not detect diameter because we say to look for 'd', not any word ending 'd'
                # But because we have to handle languages like Chinese/Thai where there is no word
                # separator, we allow this and the diameter will be detected
                ('What is the volume of a sphere of radius 5.88 and 33.88?', {'r': 5.88, 'd': 33.88}),
                # Should not be able to detect now diameter, return d=5.88 due to left priority
                ('What is the volume of a sphere of radius 5.88 / 33.88?', {'r': 5.88, 'd': 5.88}),
                # Test the unusual keyword 'test/escape'
                ('What is the volume of a sphere of radius 5.88, test/escape 33.88?', {'r': 5.88, 'd': 33.88}),
                # Test the unusual keyword '&'
                ('What is the volume of a sphere of radius 5.88, & 33.88?', {'r': 5.88, 'd': 33.88})
            ]
        },
        {
            'mex': 'dt,datetime,   ;   email,email,   ;   inc, float, inc / inch / inches',
            'lang': 'en',
            'sentences': [
                ('What is -2.6 inches? 20190322 05:15 send to me@abc.com.',
                 {'dt': '20190322 05:15', 'email': 'me@abc.com', 'inc': -2.6}),
                ('What is +1.2 inches? 2019-03-22 05:15 you@email.ua ?',
                 {'dt': '2019-03-22 05:15', 'email': 'you@email.ua', 'inc': 1.2}),
                ('2019-03-22: u_ser-name.me@gmail.com is my email',
                 {'dt': '2019-03-22', 'email': 'u_ser-name.me@gmail.com', 'inc': None}),
                ('이멜은u_ser-name.me@gmail.com',
                 {'dt': None, 'email': 'u_ser-name.me@gmail.com', 'inc': None} ),
                ('u_ser-name.me@gmail.invalid is my email',
                 {'dt': None, 'email': 'u_ser-name.me@gmail.invalid', 'inc': None})
            ]
        },
        {
            'mex': 'dt, datetime,   ;   acc, number, 계정 / 번호   ;   '
                   + 'm, int, 월   ;   d, int, 일   ;   t, time, 에   ;'
                   + 'am, float, 원   ;   bl, float, 잔액   ;'
                   + 'name, str-zh-cn, 】 ',
            'lang': 'ko',
            'sentences': [
                ('2020-01-01: 번호 0011 계정은 9 월 23 일 10:12 에 1305.67 원, 잔액 9999.77.',
                 {'dt': '2020-01-01', 'acc': '0011', 'm': 9, 'd': 23, 't': '10:12', 'am': 1305.67, 'bl': 9999.77, 'name': None}),
                ('20200101 xxx: 번호 0011 계정은 8 월 24 일 10:12 에 원 1305.67, 9999.77 잔액.',
                 {'dt': '20200101', 'acc': '0011', 'm': 8, 'd': 24, 't': '10:12', 'am': 1305.67, 'bl': 9999.77, 'name': None}),
                ('AAA 2020-01-01 11:52:22: 번호 0022 계정은 7 월 25 일 10:15:55 에 1405.78 원, 잔액 8888.77.',
                 {'dt': '2020-01-01 11:52:22', 'acc': '0022', 'm': 7, 'd': 25, 't': '10:15:55', 'am': 1405.78, 'bl': 8888.77, 'name': None}),
                ('2020-01-01: 번호 0033 계정은 6 월 26 일 完成23:24 에 1505.89 원, 잔액 7777.77.',
                 {'dt': '2020-01-01', 'acc': '0033', 'm': 6, 'd': 26, 't': '23:24', 'am': 1505.89, 'bl': 7777.77, 'name': None}),
                ('2020-01-01: 번호 0044 계정은 5 월 27 일 完成23:24:55 에 5501.99 원, 잔액 6666.77.',
                 {'dt': '2020-01-01', 'acc': '0044', 'm': 5, 'd': 27, 't': '23:24:55', 'am': 5501.99, 'bl': 6666.77, 'name': None}),
                ('2020-01-01: 번호0055계정은4월28일11:37에1111.22원，잔액5555.77.',
                 {'dt': '2020-01-01', 'acc': '0055', 'm': 4, 'd': 28, 't': '11:37', 'am': 1111.22, 'bl': 5555.77, 'name': None}),
                ('2020-01-01: 번호0066계정은3월29일11:37:55에2222.33원，잔액4444.77',
                 {'dt': '2020-01-01', 'acc': '0066', 'm': 3, 'd': 29, 't': '11:37:55', 'am': 2222.33, 'bl': 4444.77, 'name': None}),
                ('2020-01-01: 번호0777계정은30일 11:38:55에3333.44원',
                 {'dt': '2020-01-01', 'acc': '0777', 'm': None, 'd': 30, 't': '11:38:55', 'am': 3333.44, 'bl': None, 'name': None}),
                ('【은행】 陈豪贤于.',
                 {'dt': None, 'acc': None, 'm': None, 'd': None, 't': None, 'am': None, 'bl': None, 'name': '陈豪贤于'}),
                ('xxx 陈豪贤 】 于.',
                 {'dt': None, 'acc': None, 'm': None, 'd': None, 't': None, 'am': None, 'bl': None, 'name': '陈豪贤'}),
                ('陈豪贤 】 于.',
                 {'dt': None, 'acc': None, 'm': None, 'd': None, 't': None, 'am': None, 'bl': None, 'name': '陈豪贤'}),
            ]
        },
        {
            # Longer names come first
            # If we had put instead "이름 / 이름은", instead of detecting "김미소", it would return "은" instead
            # But because we do internal sorting already, this won't happen
            'mex': 'kotext, str-ko, 이름 / 이름은   ;'
                   + 'thtext, str-th, ชื่อ   ;'
                   + 'vitext, str-vi, tên   ;'
                   + 'cntext, str-zh-cn, 名字 / 名 / 叫 / 我叫, right',
            'lang': None,
            'sentences': [
                ('이름은 김미소 ชื่อ กุ้ง tên yêu ... 我叫是习近平。',
                 {'kotext': '김미소', 'thtext': 'กุ้ง', 'vitext': 'yêu', 'cntext': '习近平'} )
            ],
            'priority_direction': [
                'right'
            ]
        }
    ]

    @staticmethod
    def run_tests():
        lg.Log.DEBUG_PRINT_ALL_TO_SCREEN = True
        lg.Log.LOGLEVEL = lg.Log.LOG_LEVEL_IMPORTANT

        import nwae.utils.Profiling as prf

        n_pass = 0
        n_fail = 0
        total_time = 0

        for test in UnitTest.TESTS:
            pattern = test['mex']
            lang = test['lang']
            sentences = test['sentences']
            return_value_priorities = [mexpr.MatchExpression.TERM_LEFT] * len(sentences)
            if 'priority_direction' in test.keys():
                return_value_priority = test['priority_direction']

            for i in range(len(sentences)):
                sent = sentences[i][0]
                expected_result = None
                if len(sentences[i]) > 1:
                    expected_result = sentences[i][1]

                a = prf.Profiling.start()
                cmobj = mexpr.MatchExpression(
                    pattern=pattern,
                    lang=lang
                )
                # a = prf.Profiling.start()
                params = cmobj.get_params(
                    sentence=sent,
                    return_one_value=True
                )
                if not params == expected_result:
                    n_fail += 1
                    print('ERROR sentence "' + str(sent) + '", expect ' + str(expected_result) + ', got ' + str(params))
                else:
                    n_pass += 1
                    print('TEST OK ' + str(params))
                interval_secs = prf.Profiling.get_time_dif(start=a, stop=prf.Profiling.stop(), decimals=5)
                total_time += interval_secs
                print('Took ' + str(interval_secs))
        print('')
        print('*** TEST PASS ' + str(n_pass) + ', FAIL ' + str(n_fail) + ' ***')
        rps = round((n_pass+n_fail)/total_time, 2)
        time_per_request = round(1000/rps, 2)
        print('Result: ' + str(rps) + ' rps (requests per second), or ' + str(time_per_request) + 'ms per request')

    def __init__(self):
        raise Exception('Instantiation not supported.')


if __name__ == '__main__':
    UnitTest.run_tests()

    exit (0)
    lg.Log.LOGLEVEL = lg.Log.LOG_LEVEL_DEBUG_2
    print(mexpr.MatchExpression(
        pattern = 'm, float, ma-ss / 무게 / вес / 重 / ;  d, datetime, '
    ).get_params(
        sentence = 'My ma-ss is 68.5kg on 2019-09-08',
        return_one_value = True
    ))

