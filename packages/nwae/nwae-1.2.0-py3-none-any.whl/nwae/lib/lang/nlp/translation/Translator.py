# -*- coding: utf-8 -*-

import nwae.utils.Log as lg
from inspect import getframeinfo, currentframe
import nwae.lib.lang.LangFeatures as lf
import nwae.utils.Profiling as prf


class Translator:

    def __init__(
            self,
            # Default destination language
            dest_lang,
            nlp_download_dir = None
    ):
        try:
            import nltk
            import googletrans

            # Default destination language
            self.dest_lang = lf.LangFeatures.map_to_correct_lang_code(dest_lang)
            # The model data required for translation
            nltk.download('punkt', download_dir=nlp_download_dir)
            # Need to add path otherwise nltk will not find it
            nltk.data.path.append(nlp_download_dir)

            self.translator = googletrans.Translator()
        except Exception as ex:
            errmsg =\
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)\
                + ': Exception instantiating Translator object for destination language "'\
                + str(self.dest_lang) + '": ' + str(ex) + '.'
            lg.Log.error(errmsg)
            raise Exception(errmsg)

    def detect(
            self,
            sentence
    ):
        start_time = prf.Profiling.start()
        det = self.translator.detect(
                text = sentence
            )
        lg.Log.debug(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Lang detection of "' + str(sentence) + '" took '
            + str(prf.Profiling.get_time_dif_str(start_time, prf.Profiling.stop()))
        )
        return det.lang

    def translate(
            self,
            sentence,
            # If no destination language is given, we use default
            des_lang = None,
            src_lang = None
    ):
        try:
            start_time = prf.Profiling.start()
            from nltk import sent_tokenize
            token = sent_tokenize(sentence)

            if des_lang is None:
                # Use default destination language
                des_lang = self.dest_lang

            lg.Log.debug(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Source language "' + str(src_lang) + '", destination lang "' + str(des_lang) + '".'
            )

            s = ''
            for tt in token:
                if src_lang is not None:
                    translatedText = self.translator.translate(
                        tt,
                        dest = des_lang,
                        src  = src_lang
                    )
                else:
                    translatedText = self.translator.translate(
                        tt,
                        dest = des_lang
                    )
                s = s + str(translatedText.text)
            lg.Log.debug(
                'Lang translation of "' + str(sentence) + '" to "' + str(s) + '" took '
                + str(prf.Profiling.get_time_dif_str(start_time, prf.Profiling.stop()))
            )
            return s
        except Exception as ex:
            errmsg =\
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)\
                + ': Exception translating sentence "' + str(sentence) + '": ' + str(ex) + '.'
            lg.Log.error(errmsg)
            raise Exception(errmsg)


if __name__ == '__main__':
    tl = Translator(
        dest_lang = lf.LangFeatures.LANG_CN
    )

    # src = 'Today is a rainy day'
    src = '오늘은 비가 와'
    src_lang = tl.detect(sentence=src)

    print(src_lang)
    s = tl.translate(
        sentence = src
    )
    print(s)

    s_reverse = tl.translate(
        sentence = s,
        des_lang = src_lang
    )
    print(s_reverse)
